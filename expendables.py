import json
from groq import Groq
from fasthtml.common import * 
from dotenv import load_dotenv, find_dotenv


bootstraplink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css", integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC", crossorigin="anonymous")
fontlink = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.1/font/bootstrap-icons.min.css")
favicon = Link(rel="icon", type="image/x-icon", href="https://raw.githubusercontent.com/rajeshradhakrishnanmvk/aitemplate/main/favicon.ico")

title = Title("Groqlet Expendables")
css = Style("""body {
    display: flex;
    height: 100vh;
    overflow: hidden;
}
#sidebar {
    background-color: #f8f9fa;
    padding: 10px;
    overflow-y: auto;
    height: 100vh;
}
.chat-wrapper {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.chat-container {
    width: 100%;
    height: calc(100vh - 150px); /* Adjust based on other elements like header/footer */
    overflow-y: auto;
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 15px;
    background-color: #f8f9fa; /* Optional for better visibility */
}
.chat-message {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}
.chat-message img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    
}
.chat-message.user {
    flex-direction: row;
}
.chat-message.assistant {
    flex-direction: row-reverse;
}
.bubble {
    position: relative;
    padding: 10px;
    border-radius: 10px;
    color: white;
}
.bubble::after {
    content: '';
    position: absolute;
    width: 0;
    height: 0;
    border-style: solid;
}
.chat-message.user .bubble {
    background-color: #007bff;
    margin-left: 10px;
}
.chat-message.user .bubble::after {
    border-width: 10px 10px 10px 0;
    border-color: transparent #007bff transparent transparent;
    left: -10px;
    top: 10px;
}
.chat-message.assistant .bubble {
    background-color: #28a745;
    margin-right: 10px;
}
.chat-message.assistant .bubble::after {
    border-width: 10px 0 10px 10px;
    border-color: transparent transparent transparent #28a745;
    right: -10px;
    top: 10px;
}
#documentsTab {
      padding: 20px;
  }
  .file-upload {
      display: none;
  }
  .file-icon {
      width: 20px;
      height: 20px;
  }
  .progress-bar {
      width: 100%;
      height: 100%;
      background-color: #4caf50;
  }
  .container-fluid {
  overflow-y: auto;
  }
  .form-label {
      font-weight: bold;
  }
  .list-group-item {
      cursor: pointer;
  }""")
load_dotenv(find_dotenv()) #os.environ["GROQ_API_KEY"]
client = Groq()

app = FastHTML(hdrs=(title,favicon,bootstraplink, fontlink,css))
sp = """You are a helpful and concise assistant."""
messages = []
messages.append({"role":"system", "content":sp})
persona = []
documents =[]
tools = []

# Chat message component, polling if message is still being generated
def ChatMessage(msg_idx):
    msg = messages[msg_idx]

    text = "..." if msg['content'] == "" else msg['content']
    generating = 'generating' in messages[msg_idx] and messages[msg_idx]['generating']
    
    userImage = 'https://gramener.com/comicgen/v1/comic?name=dee&angle=side&emotion=happy&pose=explaining&box=&boxcolor=%23000000&boxgap=&mirror='
    assistantImage = 'https://gramener.com/comicgen/v1/comic?name=ava&emotion=angry&pose=angry&shirt=%23b1dbf2&box=&boxcolor=%23000000&boxgap=&mirror='

    img_role = userImage if msg['role'] == "user" else assistantImage
    chat_class = f"chat-message {'user' if msg['role'] == 'user' else 'assistant'}"
    

    stream_args = {"hx_trigger":"every 0.1s", "hx_swap":"outerHTML", "hx_get":f"/chat_message/{msg_idx}"}
    return Div(
               Img(src=img_role),
               Div(
                    P(text)
                  , cls="bubble")
               , cls=f"{chat_class}", id=f"chat-message-{msg_idx}", 
               **stream_args if generating else {})

# Route that gets polled while streaming
@app.get("/chat_message/{msg_idx}")
def get_chat_message(msg_idx:int):
    if msg_idx >= len(messages): return ""
    return ChatMessage(msg_idx)
   
# The input field for the user message. Also used to clear the 
# input field after sending a message via an OOB swap
def ChatInput():
    return Input(_required=1,type="text", name='msg', id='msg-input', 
                 placeholder="Type a message", 
                 cls="form-control", hx_swap_oob='true',
                 aria_label="Type your message here", aria_describedby="sendButton")

@app.route("/")
def get():
  page =    (Div(
                Nav(
                    Div(
                        A("Groqlet Expendables", cls="navbar-brand", href="#"),
                            Div(
                                A(
                                    I(cls="bi bi-plug"),
                                    "Plugins", cls="nav-link text-white", href="#", style="margin-right: 10px;"),
                                A(
                                     I(cls="bi bi-gear"),
                                    "Settings", cls="nav-link text-white", href="#", style="margin-right: 10px;"),
                                   
                                Img(cls="rounded-circle", src="https://media.licdn.com/dms/image/C4D03AQHwjVMduekRjw/profile-displayphoto-shrink_100_100/0/1516794061157?e=1728518400&v=beta&t=JwjApmMV83LH01mtr8jUhh5wayHWFqPEhneLEU10HRI", alt="User Icon", style="width: 30px; height: 30px;")
                                ,cls="d-flex align-items-center")
                                    ,cls="container-fluid")
                                        ,cls="navbar navbar-expand-lg navbar-dark",style="background-color: #800080;"),
                Div(
                    Div(
                        Div(
                            H4("Agents"),
                            Button("+", cls="btn btn-primary btn-sm", id="addChatBtn")
                        , cls="d-flex justify-content-between align-items-center mb-2"),
                        Ul(
                            Li(
                                Div(
                                    Span("Can you tell me a story?"),
                                    Small("11:10 PM")
                                    , cls="d-flex justify-content-between")
                            , cls="list-group-item")
                        , cls="list-group", id="chatList")
                    , cls="col-12 col-md-3", id="sidebar"),
                    Div(
                        A("Rename", cls="dropdown-item", href="#", id="renameItem")
                    ,id="contextMenu", cls="dropdown-menu", style="display:none; position:absolute;"),
                    Div(
                        Ul(
                            Li(
                                A("Chat", cls="nav-link active", data_bs_toggle="tab", href="#chatTab")
                            , cls="nav-item"),
                            Li(
                                A("Documents", cls="nav-link", data_bs_toggle="tab", href="#documentsTab")
                            , cls="nav-item"),
                            Li(
                                A("Tools", cls="nav-link",  data_bs_toggle="tab", href="#plansTab")
                            , cls="nav-item"),
                            Li(
                                A("Personas", cls="nav-link", data_bs_toggle="tab", href="#personasTab")
                            , cls="nav-item")
                        , cls="nav nav-tabs"),
                        Div(
                            Div( #chat tab
                                Div(
                                    Div(
                                        Div(
                                            Div(
                                                Div(*[ChatMessage(msgidx) for msgidx, msg in enumerate(messages)],cls="chat-container", id="chatview"),
                                                Div(
                                                    id="chatMessages", cls="chat-box h-[73vh] overflow-y-auto"),
                                                    Form(
                                                        Group(ChatInput(), Button("Send", cls="btn btn-primary", id="sendBtn", aria_label="Send", aria_describedby="msg-input")
                                                        , cls="input-group"),
                                                        hx_post="/", hx_target="#chatview", hx_swap="beforeend",
                                                        
                                                    )
                                                )
                                        ,cls='row w-100')
                                        ,cls='container-fluid chat-wrapper'),
                                    )
                                    , cls="tab-pane fade show active", id="chatTab"),
                            Div(
                                Div(
                                    H4("Documents"),
                                    Button("Upload", cls="btn btn-primary btn-sm", id="uploadBtn"),
                                    Input(type="file", id="fileInput", cls="file-upload")
                                , cls="d-flex justify-content-between align-items-center mb-2"),
                                Div(
                                    Div(
                                        Input(cls="form-check-input", type="radio", name="vectorDatabase", id="volatile", value="volatile"),
                                        Label("Volatile", cls="form-check-label", _for="volatile")
                                        ,  cls="form-check me-3"),
                                    Div(
                                        Input(cls="form-check-input", type="radio", name="vectorDatabase", id="textFile", value="textFile", checked=1),
                                        Label("TextFile", cls="form-check-label", _for="textFile")
                                        ,  cls="form-check me-3"),
                                    Div(
                                        Input(cls="form-check-input", type="radio", name="vectorDatabase", id="qdrant", value="qdrant"),
                                        Label( "Qdrant", cls="form-check-label", _for="qdrant")
                                        ,  cls="form-check me-3"),
                                    Div(
                                        Input(cls="form-check-input", type="radio", name="vectorDatabase", id="llamaindexSearch", value="llamaindexSearch"),
                                        Label("llamaindex Search", cls="form-check-label", _for="llamaindexSearch")
                                        ,  cls="form-check me-3")
                                ,cls="d-flex mb-2"),
                                Table(
                                    Thead(),
                                        Tr(
                                            Th("Name"),
                                            Th("Created on"),
                                            Th("Size (bytes)"),
                                            Th("Access"),
                                            Th("Progress")),
                                    Tbody(
                                        Tr(
                                            Td(I(cls="bi bi-file-earmark-text file-icon"), " reconciliation.txt"),
                                            Td("9:38 am"),
                                            Td("30,079"),
                                            Td("This chat"),
                                            Td(Div(cls="progress"),Div(cls="progress-bar"))),id="fileTable"),cls="table")
                            ,cls="tab-pane fade", id="documentsTab"),
                            Div(
                                Table(
                                    Thead(),
                                        Tr(
                                            Th("Goal"),
                                            Th("Created on"),
                                            Th("Token Count")),
                                    Tbody(id="planTable"),
                                        Tr(
                                            Td("askQuestions"),
                                            Td("9:38 am"),
                                            Td("30,079")),cls="table")
                            , cls="tab-pane fade", id="plansTab"),
                            Div(
                                Div(
                                    H4("Persona"),
                                    Div(
                                        Label("Agent Name", cls="form-label", _for="agentNameInput"),
                                        Input(type="text", cls="form-control", id="agentNameInput", placeholder="Enter your agent's name...")
                                    , cls="mb-3"),
                                    Div(
                                        Label("Meta Prompt", cls="form-label", _for="metaPromptInput"),
                                        Textarea(cls="form-control", id="metaPromptInput", rows="3", placeholder="Enter your Meta Prompt...")
                                    , cls="mb-3"),
                                    Div(
                                        Label("Prefill", cls="form-label", _for="prefillInput"),
                                        Textarea(cls="form-control", id="prefillInput", rows="3", placeholder="Enter agent's prefill...")
                                    , cls="mb-3"),
                                    Div(
                                        Button("Save", cls="btn btn-primary", id="savePlanBtn")
                                        , cls="d-flex justify-content-end"),
                                    Hr(),
                                    H5("Saved Plans"),
                                    Ul(cls="list-group", id="savedPlansList")
                                , cls="container-fluid p-3")
                            , cls="tab-pane fade", id="personasTab")
                               
                        , cls="tab-content flex-grow-1")
                    , cls="col-12 col-md-9 d-flex flex-column", id="chat")
                , cls="row")
            ,cls="container-fluid"),
            Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js", integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p",crossorigin="anonymous"),
            )
  return page

# Run the chat model in a separate thread
@threaded
def get_response(r, idx): #.choices[0].delta.content
    for chunk in r: 
        if chunk.choices[0].delta.content is not None:
            messages[idx]["content"] += chunk.choices[0].delta.content
    messages[idx]["generating"] = False

# Handle the form submission
@app.post("/")
def post(msg:str):
    idx = len(messages)
    messages.append({"role":"user", "content":msg})
    for entry in messages:
        if 'generating' in entry:
            del entry['generating']
    stream  = client.chat.completions.create(
                                            messages=messages,
                                            model="llama3-8b-8192",
                                            temperature=0.5,
                                            max_tokens=1024,
                                            top_p=1,
                                            stop=None,
                                            stream=True,
                                                )
    messages.append({"role":"assistant", "generating":True, "content":""}) # Response initially blank
    get_response(stream, idx+1) # Start a new thread to fill in content
    return (ChatMessage(idx), # The user's message
            ChatMessage(idx+1), # The chatbot's response
            ChatInput()) # And clear the input field via an OOB swap

serve()

