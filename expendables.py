import json
from fasthtml.common import * 

bootstraplink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css", integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC", crossorigin="anonymous")
fontlink = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.1/font/bootstrap-icons.min.css")
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
#chat {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow-y: hidden;
}
#chat-messages {
    flex-grow: 1;
    overflow-y: auto;
    padding: 10px;
}
#chat-input {
    padding: 10px;
    border-top: 1px solid #e9ecef;
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

app = FastHTML(hdrs=(title,bootstraplink, fontlink,css))

data = json.dumps([
                        {
                            "Persona": {
                                "agentname": "dinkan-1",
                                "metaprompt": "you are a helpful assistant",
                                "prefill": "helps me with financial Reconciliation",
                                "tooluse": "true",
                                "filesearch": "true",
                                "codeinterpreter": "true"
                            },
                            "Plans": [
                                { "name": "askquestion", "createon": "06/8/2024", "tokencount": "2048" }
                            ],
                            "Documents": [
                                { "file": "./reconciliation.txt", "createon": "06/8/2024", "size": "30,079", "Access": "private", "progress": "success" },
                                { "file": "./design.pdf", "createon": "07/8/2024", "size": "30,079", "Access": "public", "progress": "error" }
                            ],
                            "Chat": [
                                {"role": "system", "content":"Hello, thank you for democratizing AI's productivity benefits with open source! How can I help you today?"},
                                { "role": "assistant", "content": "what is the capital of India" },
                                { "role": "user", "content": "New Delhi is the capital of India" }
                            ]
                        },
                        {
                            "Persona": {
                                "agentname": "dinkan-2",
                                "metaprompt": "you are a helpful assistant",
                                "prefill": "helps me with financial Reconciliation",
                                "tooluse": "true",
                                "filesearch": "false",
                                "codeinterpreter": "false"
                            },
                            "Plans": [
                                { "name": "calculate", "createon": "07/8/2024", "tokencount": "1024" }
                            ],
                            "Documents": [
                                { "file": "./design.txt", "createon": "08/8/2024", "size": "30,079", "Access": "private", "progress": "success" },
                                { "file": "./design.pdf", "createon": "09/8/2024", "size": "30,079", "Access": "public", "progress": "error" }
                            ],
                            "Chat": [
                                {"role": "system", "content":"Hello, thank you for democratizing AI's productivity benefits with open source! How can I help you today?"},
                                { "role": "assistant", "content": "what is the capital of Kerala" },
                                { "role": "user", "content": "Trivandrum is the capital of India" }
                            ]
                        }
                    ])


@app.route("/")
def get():
  page =      (Div(
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
                                A("Plans", cls="nav-link",  data_bs_toggle="tab", href="#plansTab")
                            , cls="nav-item"),
                            Li(
                                A("Personas", cls="nav-link", data_bs_toggle="tab", href="#personasTab")
                            , cls="nav-item")
                        , cls="nav nav-tabs"),
                        Div(
                            Div(
                                Div(
                                    Div(
                                        Strong("Copilot"),
                                        P("Hello, thank you for democratizing AI's productivity benefits with open source! How can I help you today?")
                                        , cls="chat-message"),
                                    Div(
                                        Strong("MB"),
                                        P("Can you tell me a story about a prince in a paragraph?")
                                       , cls="chat-message"),
                                    Div(
                                        Input(type="text", cls="form-control me-2", placeholder="Type a message...", id="messageInput"),
                                        Button("Send", cls="btn btn-primary", id="sendBtn")
                                        , id="chat-input", cls="d-flex")
                                    , id="chat-messages")
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

              Script(src="https://code.jquery.com/jquery-3.6.0.min.js"),
              Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js", integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p",crossorigin="anonymous"),
              Script(f"let agents = {data};"),
              Script(""" 
                    let selectedAgentIndex = -1;

                    function populateTabs() {
                    if (selectedAgentIndex >= 0) {
                        const selectedAgent = agents[selectedAgentIndex];

                        // Populate Personas tab
                        const agentNameInput = document.getElementById('agentNameInput');
                        const metaPromptInput = document.getElementById('metaPromptInput');
                        const prefillInput = document.getElementById('prefillInput');

                        agentNameInput.value = agents[selectedAgentIndex].Persona.agentname;
                        metaPromptInput.value = agents[selectedAgentIndex].Persona.metaprompt;
                        prefillInput.value = agents[selectedAgentIndex].Persona.prefill;

                        // Populate Plans tab
                        // Clear and repopulate the plans table or list with selectedAgent.Plans
                        const planTable = document.getElementById('planTable');
                        planTable.innerHTML = '';
                        agents[selectedAgentIndex].Plans.forEach(plan => {
                            const newRow = `<tr>
                                <td>${plan.name}</td>
                                <td>${plan.createon}</td>
                                <td>${plan.tokencount}</td>
                            </tr>`;
                            planTable.insertAdjacentHTML('beforeend', newRow);
                        });
                        // Populate Documents tab
                        // Clear and repopulate the documents table with selectedAgent.Documents
                        const fileTable = document.getElementById('fileTable');
                        fileTable.innerHTML = '';
                        agents[selectedAgentIndex].Documents.forEach(doc => {
                            const newRow = `<tr>
                                <td><i class="bi bi-file-earmark-text file-icon"></i> ${doc.file}</td>
                                <td>${doc.createon}</td>
                                <td>${doc.size}</td>
                                <td>${doc.Access}</td>
                                <td><div class="progress"><div class="progress-bar"></div></div></td>
                            </tr>`;
                            fileTable.insertAdjacentHTML('beforeend', newRow);
                        });
                        // Display initial messages
                        //displayMessages();
                    }
                    }

                    function renderChatList() {
                    const chatList = document.getElementById('chatList');
                    chatList.innerHTML = ''; // Clear the existing list

                    agents.forEach((agent, index) => {
                        const newItem = document.createElement('li');
                        newItem.className = 'list-group-item';
                        newItem.innerHTML = `<div class="d-flex justify-content-between">
                                                <span>${agent.Persona.agentname}</span>
                                                <small>${new Date().toLocaleTimeString()}</small>
                                            </div>`;
                        newItem.setAttribute('data-index', index);
                        newItem.setAttribute('data-messages', JSON.stringify(agent.Chat));
                        newItem.addEventListener('click', function() {
                            selectedAgentIndex = parseInt(this.getAttribute('data-index'));
                            displayMessages();
                            populateTabs();
                        });
                        newItem.addEventListener('contextmenu', function(e) {
                            e.preventDefault();
                            showContextMenu(e, newItem, index);
                        });
                        chatList.appendChild(newItem);
                    });
                    }
                    // Event listener for add chat button - Sidebar
                    document.getElementById('addChatBtn').addEventListener('click', function() {
                    var chatList = document.getElementById('chatList');
                    var newItem = document.createElement('li');
                    newItem.className = 'list-group-item';
                    newItem.innerHTML = `<div class="d-flex justify-content-between">
                                        <span>New Agent</span>
                                        <small>${new Date().toLocaleTimeString()}</small>
                                    </div>`;
                    newItem.setAttribute('data-messages', JSON.stringify([]));
                    chatList.appendChild(newItem);

                    // Add new agent to agents array
                    var newAgent = {
                    "Persona": {
                        "agentname": `agent-${Date.now()}`,
                        "metaprompt": "you are a helpful assistant",
                        "prefill": "helps me with financial Reconciliation",
                        "tooluse": "true",
                        "filesearch": "false",
                        "codeinterpreter": "false"
                    },
                    "Plans": [],
                    "Documents": [],
                    "Chat": []
                    };
                    agents.push(newAgent);
                    renderChatList();
                    });

                    // Show context menu
                    function showContextMenu(event, listItem) {
                    var contextMenu = document.getElementById('contextMenu');
                    contextMenu.style.display = 'block';
                    contextMenu.style.left = event.pageX + 'px';
                    contextMenu.style.top = event.pageY + 'px';

                    document.getElementById('renameItem').onclick = function() {
                        var newName = prompt("Enter new name:", listItem.querySelector('span').textContent);
                        if (newName) {
                            listItem.querySelector('span').textContent = newName;
                            //write a code to update the agent name in agents array
                            agents[selectedAgentIndex].Persona.agentname = newName;
                        }
                        contextMenu.style.display = 'none';
                    };

                    document.addEventListener('click', function() {
                        contextMenu.style.display = 'none';
                    }, { once: true });
                    }

                    // Event listener for existing items
                    document.querySelectorAll('#chatList .list-group-item').forEach(item => {
                    item.addEventListener('contextmenu', function(e) {
                        e.preventDefault();
                        showContextMenu(e, item);
                    });
                    });
                    // Function to display messages
                    function displayMessages() {
                    const chatMessages = document.getElementById('chat-messages');
                    chatMessages.innerHTML = '';
                    agents[selectedAgentIndex].Chat.forEach(msg => {
                        const messageElement = document.createElement('div');
                        messageElement.classList.add('chat-message');
                        messageElement.innerHTML = `<strong>${msg.role}</strong><p>${msg.content}</p>`;
                        chatMessages.appendChild(messageElement);
                    });
                    }

                    // Event listener for sidebar items
                    document.querySelectorAll('#chatList .list-group-item').forEach(item => {
                    item.addEventListener('click', function() {
                        const newMessages = JSON.parse(this.getAttribute('data-messages'));
                        messages = [...newMessages];
                        displayMessages();
                    });
                    });

                    // Event listener for send button
                    document.getElementById('sendBtn').addEventListener('click', function() {
                    const input = document.getElementById('messageInput');
                    const userMessage = input.value;
                    if (userMessage) {
                        agents[selectedAgentIndex].Chat.push({ role: 'MB', content: userMessage });
                        if (userMessage.toLowerCase() === 'what is the capital of india') {
                            agents[0].Chat.push({ role: 'Copilot', content: 'New Delhi is the capital of India' });
                        }
                        displayMessages();
                        input.value = '';
                    }
                    });

                    // Event listener for upload button
                    document.getElementById('uploadBtn').addEventListener('click', function() {
                    document.getElementById('fileInput').click();
                    });

                    // Event listener for file input - Documents Tab
                    document.getElementById('fileInput').addEventListener('change', function(event) {
                    const file = event.target.files[0];
                    if (file) {
                        const newRow = `<tr>
                            <td><i class="bi bi-file-earmark-text file-icon"></i> ${file.name}</td>
                            <td>${new Date().toLocaleTimeString()}</td>
                            <td>${file.size}</td>
                            <td>This chat</td>
                            <td><div class="progress"><div class="progress-bar"></div></div></td>
                        </tr>`;
                        document.getElementById('fileTable').insertAdjacentHTML('beforeend', newRow);
                    }
                    });

                    // Event listener for save button - Personas Tab
                    document.getElementById('savePlanBtn').addEventListener('click', function() {
                    const agentname = document.getElementById('agentNameInput').value;
                    const metaprompt = document.getElementById('metaPromptInput').value;
                    const prefill = document.getElementById('prefillInput').value;

                    const plan = {
                        agentname,
                        metaprompt,
                        prefill
                    };

                    const savedPlansList = document.getElementById('savedPlansList');
                    const planItem = document.createElement('li');
                    planItem.classList.add('list-group-item');
                    planItem.textContent = `Agent Name: ${agentname}`;
                    planItem.addEventListener('click', function() {
                        alert(`Meta Prompt: ${plan.metaprompt}\nPrefill: ${plan.prefill}`);
                    });

                    savedPlansList.appendChild(planItem);

                    // Clear the inputs after saving
                    document.getElementById('agentNameInput').value = '';
                    document.getElementById('metaPromptInput').value = '';
                    document.getElementById('prefillInput').value = '';
                    });



                    // Initial rendering of the chat list
                    renderChatList();

                    // Populate tabs initially (if needed)
                    populateTabs();
                        """))
  return page

serve()

