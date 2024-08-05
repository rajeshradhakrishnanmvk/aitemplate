from fasthtml.common import *
from groq import Groq
from dotenv import load_dotenv, find_dotenv

# Set up the app, including daisyui and tailwind for the chat component
tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
app = FastHTML(hdrs=(tlink, dlink, picolink))

load_dotenv(find_dotenv()) #os.environ["GROQ_API_KEY"]
client = Groq()
sp = """You are a helpful and concise assistant."""
messages = []


# Chat message component (renders a chat bubble)
def ChatMessage(msg):
    bubble_class = f"chat-bubble-{'primary' if msg['role'] == 'user' else 'secondary'}"
    chat_class = f"chat-{'end' if msg['role'] == 'user' else 'start'}"
    return Div(Div(msg['role'], cls="chat-header"),
               Div(msg['content'], cls=f"chat-bubble {bubble_class}"),
               cls=f"chat {chat_class}")

# The input field for the user message. Also used to clear the 
# input field after sending a message via an OOB swap
def ChatInput():
    return Input(type="text", name='msg', id='msg-input', 
                 placeholder="Type a message", 
                 cls="input input-bordered w-full", hx_swap_oob='true')

# The main screen
@app.route("/")
def get():
    page = Body(H1('Agentic Bot 1001'),
                Div(*[ChatMessage(msg) for msg in messages],
                    id="chatlist", cls="chat-box h-[73vh] overflow-y-auto"),
                Form(Group(ChatInput(), Button("Send", cls="btn btn-primary")),
                    hx_post="/", hx_target="#chatlist", hx_swap="beforeend",
                    cls="flex space-x-2 mt-2",
                ), cls="p-4 max-w-lg mx-auto")
    return Title('Agentic Bot 1001'), page

# Handle the form submission
@app.post("/")
def post(msg:str):
    messages.append({"role":"system", "content":sp})
    messages.append({"role":"user", "content":msg})
    #r = cli(messages, sp=sp) # get response from chat model
    chat_completion = client.chat.completions.create(
                                                        messages=messages,
                                                        model="llama3-8b-8192",
                                                        temperature=0.5,
                                                        max_tokens=1024,
                                                        top_p=1,
                                                        stop=None,
                                                        stream=False,
                                                    )
    messages.append({"role":"assistant", "content":chat_completion.choices[0].message.content})
    return (ChatMessage(messages[-2]), # The user's message
            ChatMessage(messages[-1]), # The chatbot's response
            ChatInput()) # And clear the input field via an OOB swap


if __name__ == '__main__': uvicorn.run("simple:app", host='0.0.0.0', port=8000, reload=True)