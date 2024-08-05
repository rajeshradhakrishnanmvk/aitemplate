


__all__ = []


from .core import *
from fastcore.utils import *
from fastcore.meta import delegates

# from anthropic.types import TextBlock, Message, ToolUseBlock


@patch
@delegates(Chat.__call__)
def toolloop(self:Chat,
             pr, # Prompt to pass to Groq
             max_steps=10, # Maximum number of tool requests to loop through
             trace_func:Optional[callable]=None, # Function to trace tool use steps (e.g `print`)
             cont_func:Optional[callable]=noop, # Function that stops loop if returns False
             **kwargs):
    "Add prompt `pr` to dialog and get a response from Groq, automatically following up with `tool_use` messages"
    r = self(pr, **kwargs)
    for i in range(max_steps):
        if r.stop_reason!='tool_use': break
        if trace_func: trace_func(r)
        r = self(**kwargs)
        if not (cont_func or noop)(self.h[-2]): break
    if trace_func: trace_func(r)
    return r