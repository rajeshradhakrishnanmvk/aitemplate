
__all__ = ['empty', 'models',  'find_block', 'contents', 'usage', 'mk_msgs', 'Client',
           'mk_tool_choice', 'call_func', 'mk_funcres', 'mk_toolres', 'Chat', 'img_msg', 'text_msg', 'mk_msg']

import inspect, typing, mimetypes, base64, json
from collections import abc
try: from IPython import display
except: display=None

# from anthropic import Anthropic, AnthropicBedrock, AnthropicVertex
# from anthropic.types import Usage, TextBlock, Message, ToolUseBlock
# from anthropic.resources import messages

import toolslm
from toolslm.funccall import *

from fastcore import imghdr
from fastcore.meta import delegates
from fastcore.utils import *


empty = inspect.Parameter.empty

#  https://console.groq.com/docs/models
models = 'llama3-8b-8192','mixtral-8x7b-32768',' gemma-7b-it'


def find_block(r:abc.Mapping, # The message to look in
               blk_type:type=TextBlock  # The type of block to find
              ):
    "Find the first block of type `blk_type` in `r.content`."
    return first(o for o in r.content if isinstance(o,blk_type))


def contents(r):
    "Helper to get the contents from Groq response `r`."
    blk = find_block(r)
    if not blk and r.content: blk = r.content[0]
    return blk.text.strip() if hasattr(blk,'text') else blk


@patch
def _repr_markdown_(self:(Message)):
    det = '\n- '.join(f'{k}: {v}' for k,v in self.model_dump().items())
    return f"""{contents(self)}

<details>

- {det}

</details>"""


def usage(inp=0, # Number of input tokens
          out=0  # Number of output tokens
         ):
    "Slightly more concise version of `Usage`."
    return Usage(input_tokens=inp, output_tokens=out)


@patch(as_prop=True)
def total(self:Usage): return self.input_tokens+self.output_tokens


@patch
def __repr__(self:Usage): return f'In: {self.input_tokens}; Out: {self.output_tokens}; Total: {self.total}'


@patch
def __add__(self:Usage, b):
    "Add together each of `input_tokens` and `output_tokens`"
    return usage(self.input_tokens+b.input_tokens, self.output_tokens+b.output_tokens)


def mk_msgs(msgs:list, **kw):
    "Helper to set 'assistant' role on alternate messages."
    if isinstance(msgs,str): msgs=[msgs]
    return [mk_msg(o, ('user','assistant')[i%2], **kw) for i,o in enumerate(msgs)]


class Client:
    def __init__(self, model, cli=None):
        "Basic Groq messages client."
        self.model,self.use = model,usage()
        self.c = (cli or Groq())


@patch
def _r(self:Client, r:Message, prefill=''):
    "Store the result of the message and accrue total usage."
    if prefill:
        blk = find_block(r)
        blk.text = prefill + (blk.text or '')
    self.result = r.choices[0].message.content #chat_completion.choices[0].message.content
    # self.use += r.usage
    # self.stop_reason = r.stop_reason
    # self.stop_sequence = r.stop_sequence
    return r


@patch
def _stream(self:Client, msgs:list, prefill='', stop, **kwargs):
    with self.c.chat.completions.create(model=self.model, messages=mk_msgs(msgs), stop, stream=True) as s:
        if prefill: yield(prefill)
        yield from s.choices[0].delta.content #chunk.choices[0].delta.content
        self._r(s.get_final_message(), prefill)


@patch
@delegates(messages.Messages.create)
def __call__(self:Client,
             msgs:list, # List of messages in the dialog
             sp='', # The system prompt
             temp=0, # Temperature
             maxtok=4096, # Maximum tokens
             prefill='', # Optional prefill to pass to Groq as start of its response
             stream:bool=False, # Stream response?
             stop=None, # Stop sequence
             **kwargs):
    "Make a call to Groq."
    pref = [prefill.strip()] if prefill else []
    if not isinstance(msgs,list): msgs = [msgs]
    if stop is not None:
        if not isinstance(stop, (list)): stop = [stop]
        kwargs["stop_sequences"] = stop
    msgs = mk_msgs(msgs+pref)
    if stream: return self._stream(msgs, prefill=prefill, max_tokens=maxtok, system=sp, temperature=temp, stop,**kwargs)
    msgs = mk_msgs(msgs+sp)
    res = self.c.chat.completions.create(
        model=self.model, messages=msgs, max_tokens=maxtok, temperature=temp, stop=stop)
    self._r(res, prefill)
    return self.result


def mk_tool_choice(choose:Union[str,bool,None])->dict:
    "Create a `tool_choice` dict that's 'auto' if `choose` is `None`, 'any' if it is True, or 'tool' otherwise"
    return {"type": "tool", "name": choose} if isinstance(choose,str) else {'type':'any'} if choose else {'type':'auto'}


def _mk_ns(*funcs:list[callable]) -> dict[str,callable]:
    "Create a `dict` of name to function in `funcs`, to use as a namespace"
    return {f.__name__:f for f in funcs}


def call_func(fc:ToolUseBlock, # Tool use block from Groq's message
              ns:Optional[abc.Mapping]=None, # Namespace to search for tools, defaults to `globals()`
              obj:Optional=None # Object to search for tools
             ):
    "Call the function in the tool response `tr`, using namespace `ns`."
    if ns is None: ns=globals()
    if not isinstance(ns, abc.Mapping): ns = _mk_ns(*ns)
    func = getattr(obj, fc.name, None)
    if not func: func = ns[fc.name]
    res = func(**fc.input)
    return res

def mk_funcres(tuid, res):
    "Given tool use id and the tool result, create a tool_result response."
    return dict(type="tool_result", tool_use_id=tuid, content=str(res))


def mk_toolres(
    r:abc.Mapping, # Tool use request response from Groq
    ns:Optional[abc.Mapping]=None, # Namespace to search for tools
    obj:Optional=None # Class to search for tools
    ):
    "Create a `tool_result` message from response `r`."
    cts = getattr(r, 'content', [])
    res = [mk_msg(r)]
    tcs = [mk_funcres(o.id, call_func(o, ns=ns, obj=obj)) for o in cts if isinstance(o,ToolUseBlock)]
    if tcs: res.append(mk_msg(tcs))
    return res


class Chat:
    def __init__(self,
                 model:Optional[str]=None, # Model to use (leave empty if passing `cli`)
                 cli:Optional[Client]=None, # Client to use (leave empty if passing `model`)
                 sp='', # Optional system prompt
                 tools:Optional[list]=None, # List of tools to make available to Groq
                 cont_pr:Optional[str]=None, # User prompt to continue an assistant response: assistant,[user:"..."],assistant
                 tool_choice:Optional[dict]=None): # Optionally force use of some tool
        "Groq chat client."
        assert model or cli
        assert cont_pr != "", "cont_pr may not be an empty string"
        self.c = (cli or Client(model))
        self.h,self.sp,self.tools,self.cont_pr,self.tool_choice = [],sp,tools,cont_pr,tool_choice

    @property
    def use(self): return self.c.use


@patch
def _stream(self:Chat, res):
    yield from res
    self.h += mk_toolres(self.c.result, ns=self.tools, obj=self)


@patch
def _append_pr(self:Chat,
               pr=None,  # Prompt / message
              ):
    prev_role = nested_idx(self.h, -1, 'role') if self.h else 'assistant' # First message should be 'user' if no history
    if pr and prev_role == 'user':
        self() # There's already a user request pending, so complete it
    elif pr is None and prev_role == 'assistant':
        if self.cont_pr is None:
            raise ValueError("User prompt must be given after an assistant completion, or `self.cont_pr` must be specified.")
        pr = self.cont_pr # No user prompt, keep the `assistant,[user:cont_pr],assistant` chain
    if pr: self.h.append(mk_msg(pr))

@patch
def __call__(self:Chat,
             pr=None,  # Prompt / message
             temp=0, # Temperature
             maxtok=4096, # Maximum tokens
             stream=False, # Stream response?
             prefill='', # Optional prefill to pass to Groq as start of its response
             **kw):
    self._append_pr(pr)
    if self.tools: kw['tools'] = [get_schema(o) for o in self.tools]
    if self.tool_choice: kw['tool_choice'] = mk_tool_choice(self.tool_choice)
    res = self.c(self.h, stream=stream, prefill=prefill, sp=self.sp, temp=temp, maxtok=maxtok, **kw)
    if stream: return self._stream(res)
    self.h += mk_toolres(self.c.result, ns=self.tools, obj=self)
    return res


def img_msg(data:bytes)->dict:
    "Convert image `data` into an encoded `dict`"
    img = base64.b64encode(data).decode("utf-8")
    mtype = mimetypes.types_map['.'+imghdr.what(None, h=data)]
    r = dict(type="base64", media_type=mtype, data=img)
    return {"type": "image", "source": r}


def text_msg(s:str)->dict:
    "Convert `s` to a text message"
    return {"type": "text", "text": s}


def _mk_content(src):
    "Create appropriate content data structure based on type of content"
    if isinstance(src,str): return text_msg(src)
    if isinstance(src,bytes): return img_msg(src)
    return src


def mk_msg(content, # A string, list, or dict containing the contents of the message
           role='user', # Must be 'user' or 'assistant'
           **kw):
    "Helper to create a `dict` appropriate for a Groq message. `kw` are added as key/value pairs to the message"
    if hasattr(content, 'content'): content,role = content.content,content.role
    if isinstance(content, abc.Mapping): content=content['content']
    if not isinstance(content, list): content=[content]
    content = [_mk_content(o) for o in content] if content else '.'
    return dict(role=role, content=content, **kw)
