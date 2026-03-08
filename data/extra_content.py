"""
Extra planets: Saturn (APIs & FastAPI) and Neptune (Advanced AI/RAG/LangGraph)
"""

EXTRA_PLANETS = {
    "saturn": {
        "id": "saturn",
        "name": "Saturn",
        "subtitle": "API & Backend Engineering",
        "icon": "🪐",
        "color": "#C084FC",
        "glow": "#E9D5FF",
        "xp_required": 4000,
        "description": "Build production REST APIs with FastAPI. Deploy backends. Work with databases.",
        "atmosphere": "api_streams",
        "missions": [
            {
                "id": "sat_001",
                "title": "Galactic REST API",
                "story": "🪐 ARIA: *'Commander! Every great app needs an API. Saturn engineers build the backends that power the galaxy!'*",
                "concept": "FastAPI Fundamentals",
                "xp": 800,
                "energy": 5,
                "difficulty": "⭐⭐⭐⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": """**ARIA:** *'FastAPI is Python's fastest web framework for building APIs!'*

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Galaxy API", version="1.0")

# Data model with automatic validation
class Planet(BaseModel):
    name: str
    size: int
    has_water: bool = False
    temp: Optional[float] = None

# In-memory database
planets_db = {}
next_id = 1

@app.get("/")
def root():
    return {"message": "🚀 Galaxy API is live!"}

@app.post("/planets/", response_model=dict)
def create_planet(planet: Planet):
    global next_id
    planets_db[next_id] = {"id": next_id, **planet.dict()}
    next_id += 1
    return planets_db[next_id - 1]

@app.get("/planets/{planet_id}")
def get_planet(planet_id: int):
    if planet_id not in planets_db:
        raise HTTPException(status_code=404, detail="Planet not found")
    return planets_db[planet_id]

@app.get("/planets/")
def list_planets():
    return list(planets_db.values())

@app.delete("/planets/{planet_id}")
def delete_planet(planet_id: int):
    if planet_id not in planets_db:
        raise HTTPException(status_code=404, detail="Planet not found")
    return planets_db.pop(planet_id)

# Run: uvicorn main:app --reload
# Docs: http://localhost:8000/docs  ← AUTO GENERATED!
```

**FastAPI superpowers:**
- ⚡ Auto-generates `/docs` interactive API docs
- ✅ Automatic data validation with Pydantic
- 🚀 Async support built-in
- 📝 Type hints = less bugs"""
                    },
                    {
                        "type": "visual",
                        "content": "fastapi_visual",
                        "caption": "FastAPI: Request → Validate → Process → Response"
                    },
                    {
                        "type": "quiz",
                        "question": "In FastAPI, what does `raise HTTPException(status_code=404)` do?",
                        "options": ["Crashes the server", "Returns a 404 Not Found error response", "Deletes the route", "Logs an error"],
                        "answer": 1,
                        "explanation": "HTTPException sends proper HTTP error responses to the client with the right status code!"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Build a complete CRUD API for a 'Spaceship' resource. Model: name(str), speed(int), fuel(float), active(bool=True). Implement: POST /ships/, GET /ships/, GET /ships/{id}, DELETE /ships/{id}",
                        "starter": """from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Fleet API")

class Spaceship(BaseModel):
    name: str
    speed: int
    fuel: float
    active: bool = True

ships_db = {}
next_id = 1

# Implement your CRUD endpoints below
@app.post("/ships/")
def create_ship(ship: Spaceship):
    pass  # TODO

@app.get("/ships/")
def list_ships():
    pass  # TODO

@app.get("/ships/{ship_id}")
def get_ship(ship_id: int):
    pass  # TODO

@app.delete("/ships/{ship_id}")
def delete_ship(ship_id: int):
    pass  # TODO
""",
                        "solution": """from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Fleet API")

class Spaceship(BaseModel):
    name: str
    speed: int
    fuel: float
    active: bool = True

ships_db = {}
next_id = 1

@app.post("/ships/")
def create_ship(ship: Spaceship):
    global next_id
    ships_db[next_id] = {"id": next_id, **ship.dict()}
    next_id += 1
    return ships_db[next_id - 1]

@app.get("/ships/")
def list_ships():
    return list(ships_db.values())

@app.get("/ships/{ship_id}")
def get_ship(ship_id: int):
    if ship_id not in ships_db:
        raise HTTPException(status_code=404, detail="Ship not found")
    return ships_db[ship_id]

@app.delete("/ships/{ship_id}")
def delete_ship(ship_id: int):
    if ship_id not in ships_db:
        raise HTTPException(status_code=404, detail="Ship not found")
    return ships_db.pop(ship_id)

print("Fleet API ready! 4 endpoints implemented.")""",
                        "check": ["404", "Ship"],
                        "hints": [
                            "Use `global next_id` at top of create function",
                            "ships_db[next_id] = {'id': next_id, **ship.dict()}",
                            "raise HTTPException(status_code=404) for missing ships"
                        ]
                    }
                ],
                "reward": {"xp": 800, "badge": "🪐 API Architect", "unlock": "sat_002"}
            },
            {
                "id": "sat_002",
                "title": "Database Warp Core",
                "story": "💾 ARIA: *'Commander, our API needs persistent storage! SQLite + SQLAlchemy = data that survives reboot!'*",
                "concept": "Databases with SQLAlchemy",
                "xp": 900,
                "energy": 5,
                "difficulty": "⭐⭐⭐⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": """**ARIA:** *'SQLAlchemy is Python's most powerful ORM — maps Python classes to database tables!'*

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create database
DATABASE_URL = "sqlite:///./galaxy.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define table as Python class
class Planet(Base):
    __tablename__ = "planets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    size = Column(Integer)
    temp = Column(Float)
    habitable = Column(Boolean, default=False)

# Create tables
Base.metadata.create_all(bind=engine)

# CRUD operations
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# With FastAPI:
from fastapi import Depends
from sqlalchemy.orm import Session

@app.post("/planets/")
def create_planet(planet: PlanetCreate, db: Session = Depends(get_db)):
    db_planet = Planet(**planet.dict())
    db.add(db_planet)
    db.commit()
    db.refresh(db_planet)
    return db_planet
```"""
                    },
                    {
                        "type": "quiz",
                        "question": "What does `db.commit()` do in SQLAlchemy?",
                        "options": ["Closes the database", "Saves changes permanently to the database", "Starts a transaction", "Deletes all records"],
                        "answer": 1,
                        "explanation": "db.commit() permanently saves your changes. Without it, changes are lost when the session closes!"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Create a SQLAlchemy model for 'Mission' table: id, title(str), planet(str), xp_reward(int), completed(bool=False). Create the table and insert 3 missions, then query all completed=False ones.",
                        "starter": """from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./missions.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define Mission model
class Mission(Base):
    __tablename__ = "missions"
    # Add columns here

# Create tables
Base.metadata.create_all(bind=engine)

# Insert 3 missions and query incomplete ones
db = SessionLocal()
# Add your code here
""",
                        "solution": """from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./missions.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    planet = Column(String)
    xp_reward = Column(Integer)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)
db = SessionLocal()

missions = [
    Mission(title="First Contact", planet="Mercury", xp_reward=50),
    Mission(title="Data Crystals", planet="Mercury", xp_reward=75, completed=True),
    Mission(title="Warp Engine", planet="Mercury", xp_reward=200),
]
db.add_all(missions)
db.commit()

incomplete = db.query(Mission).filter(Mission.completed == False).all()
print(f"Incomplete missions: {len(incomplete)}")
for m in incomplete:
    print(f"  - {m.title} ({m.planet}) +{m.xp_reward} XP")
db.close()""",
                        "check": ["Incomplete missions"],
                        "hints": [
                            "id = Column(Integer, primary_key=True)",
                            "db.add_all(list_of_objects) adds multiple at once",
                            "db.query(Mission).filter(Mission.completed == False).all()"
                        ]
                    }
                ],
                "reward": {"xp": 900, "badge": "💾 Database Commander", "unlock": None}
            }
        ]
    },

    "neptune": {
        "id": "neptune",
        "name": "Neptune",
        "subtitle": "Advanced AI — RAG & Multi-Agent",
        "icon": "🔵",
        "color": "#06B6D4",
        "glow": "#67E8F9",
        "xp_required": 5500,
        "description": "Master RAG systems, vector databases, and multi-agent AI workflows. The frontier of AI engineering.",
        "atmosphere": "quantum",
        "missions": [
            {
                "id": "nep_001",
                "title": "The Knowledge Matrix",
                "story": "🧠 ARIA: *'Commander! RAG — Retrieval Augmented Generation — gives AI access to YOUR documents. No more hallucinations!'*",
                "concept": "RAG with LangChain",
                "xp": 1000,
                "energy": 5,
                "difficulty": "⭐⭐⭐⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": """**ARIA:** *'RAG = find relevant docs → feed to LLM → get accurate answers!'*

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_anthropic import ChatAnthropic, AnthropicEmbeddings
from langchain.chains import RetrievalQA

# 1. Load documents
loader = TextLoader("galaxy_manual.txt")
docs = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(docs)

# 3. Create embeddings & vector store
embeddings = AnthropicEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# 4. Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 5. Build QA chain
llm = ChatAnthropic(model="claude-sonnet-4-20250514")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# 6. Ask questions — AI answers from YOUR docs!
result = qa_chain.invoke("What is the warp speed limit?")
print(result["result"])
print("Sources:", result["source_documents"])
```

**RAG Pipeline:**
📄 Documents → ✂️ Chunks → 🔢 Embeddings → 🗄️ Vector DB → 🔍 Retrieve → 🤖 Generate"""
                    },
                    {
                        "type": "visual",
                        "content": "rag_visual",
                        "caption": "RAG: Your docs + AI = accurate, sourced answers"
                    },
                    {
                        "type": "quiz",
                        "question": "Why do we split documents into chunks for RAG?",
                        "options": [
                            "To save storage space",
                            "LLMs have token limits — smaller chunks fit in context window",
                            "To make it faster to type",
                            "Python requires it"
                        ],
                        "answer": 1,
                        "explanation": "LLMs have limited context windows. Chunking lets us retrieve only the RELEVANT pieces, not entire documents!"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Build a simple RAG system: create a text about space, split it, store in FAISS (with fake embeddings for demo), then implement a search function that finds relevant chunks for a query.",
                        "starter": """from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Space knowledge base
space_text = \"\"\"
Mercury is the closest planet to the Sun. Its surface temperature varies from -180°C to 430°C.
Venus is the hottest planet with temperatures reaching 465°C due to greenhouse effect.
Earth is the only known planet with life, covered 71% by water.
Mars has the largest volcano in the solar system: Olympus Mons at 22km high.
Jupiter is the largest planet, with the Great Red Spot storm lasting 400 years.
Saturn has beautiful rings made of ice and rock particles.
Neptune has winds reaching 2100 km/h, the fastest in the solar system.
\"\"\"

# 1. Create Document object
docs = [Document(page_content=space_text)]

# 2. Split into chunks (chunk_size=100, overlap=20)

# 3. Print number of chunks and first chunk content

# 4. Simple keyword search function
def search_knowledge(query, chunks, top_k=2):
    # Find chunks containing query keywords
    query_words = query.lower().split()
    scored = []
    for chunk in chunks:
        score = sum(1 for word in query_words if word in chunk.page_content.lower())
        if score > 0:
            scored.append((score, chunk))
    scored.sort(reverse=True)
    return [c for _, c in scored[:top_k]]

# Test search
results = search_knowledge("hottest planet temperature", chunks)
for r in results:
    print(r.page_content[:100])
""",
                        "solution": """from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

space_text = \"\"\"
Mercury is the closest planet to the Sun. Its surface temperature varies from -180°C to 430°C.
Venus is the hottest planet with temperatures reaching 465°C due to greenhouse effect.
Earth is the only known planet with life, covered 71% by water.
Mars has the largest volcano in the solar system: Olympus Mons at 22km high.
Jupiter is the largest planet, with the Great Red Spot storm lasting 400 years.
Saturn has beautiful rings made of ice and rock particles.
Neptune has winds reaching 2100 km/h, the fastest in the solar system.
\"\"\"

docs = [Document(page_content=space_text)]
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_documents(docs)
print(f"Created {len(chunks)} chunks")
print(f"First chunk: {chunks[0].page_content[:80]}...")

def search_knowledge(query, chunks, top_k=2):
    query_words = query.lower().split()
    scored = []
    for chunk in chunks:
        score = sum(1 for word in query_words if word in chunk.page_content.lower())
        if score > 0:
            scored.append((score, chunk))
    scored.sort(reverse=True)
    return [c for _, c in scored[:top_k]]

results = search_knowledge("hottest planet temperature", chunks)
print(f"\\nFound {len(results)} relevant chunks:")
for r in results:
    print(f"  → {r.page_content[:100]}")""",
                        "check": ["chunks", "chunk"],
                        "hints": [
                            "splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)",
                            "chunks = splitter.split_documents(docs)",
                            "Loop through chunks and score by keyword matches"
                        ]
                    }
                ],
                "reward": {"xp": 1000, "badge": "🧠 RAG Engineer", "unlock": "nep_002"}
            },
            {
                "id": "nep_002",
                "title": "Multi-Agent Command Center",
                "story": "🕸️ ARIA: *'The ultimate mission! Build a multi-agent system where specialized AI agents collaborate to solve complex problems!'*",
                "concept": "Multi-Agent LangGraph",
                "xp": 1500,
                "energy": 5,
                "difficulty": "⭐⭐⭐⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": """**ARIA:** *'Multi-agent: multiple specialized AIs collaborating like a team!'*

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Literal
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-20250514")

class TeamState(TypedDict):
    task: str
    research: str
    code: str
    review: str
    final: str
    next_agent: str

def researcher_agent(state: TeamState) -> TeamState:
    \"\"\"Researches the topic\"\"\"
    response = llm.invoke(
        f"Research this topic in 2 sentences: {state['task']}"
    )
    return {"research": response.content, "next_agent": "coder"}

def coder_agent(state: TeamState) -> TeamState:
    \"\"\"Writes code based on research\"\"\"
    response = llm.invoke(
        f"Write Python code for: {state['task']}\\nContext: {state['research']}"
    )
    return {"code": response.content, "next_agent": "reviewer"}

def reviewer_agent(state: TeamState) -> TeamState:
    \"\"\"Reviews and finalizes\"\"\"
    response = llm.invoke(
        f"Review this code and give a brief quality assessment:\\n{state['code']}"
    )
    return {"review": response.content, "final": state['code'], "next_agent": "done"}

def route_agent(state: TeamState) -> Literal["researcher", "coder", "reviewer", "__end__"]:
    agent = state.get("next_agent", "researcher")
    if agent == "done": return END
    return agent

# Build multi-agent graph
workflow = StateGraph(TeamState)
workflow.add_node("researcher", researcher_agent)
workflow.add_node("coder", coder_agent)
workflow.add_node("reviewer", reviewer_agent)
workflow.set_entry_point("researcher")
workflow.add_conditional_edges("researcher", route_agent)
workflow.add_conditional_edges("coder", route_agent)
workflow.add_conditional_edges("reviewer", route_agent)

team = workflow.compile()
result = team.invoke({
    "task": "Create a function to calculate fibonacci numbers",
    "research": "", "code": "", "review": "", "final": "", "next_agent": ""
})
print(result["final"])
```"""
                    },
                    {
                        "type": "visual",
                        "content": "multiagent_visual",
                        "caption": "Multi-Agent: Each agent specializes → together they solve complex tasks"
                    },
                    {
                        "type": "quiz",
                        "question": "What is the main advantage of multi-agent systems over single agents?",
                        "options": [
                            "They're always faster",
                            "Specialization — each agent excels at one task, better results overall",
                            "They use less API calls",
                            "They don't need LangGraph"
                        ],
                        "answer": 1,
                        "explanation": "Like a team — a researcher, coder, and reviewer each do what they're best at. Much better than one agent doing everything!"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Build a 3-agent pipeline: planner → writer → editor. Each adds to a 'content' field. Test with task='Write a Python tutorial intro'. Use simple string manipulation (no API needed for this exercise).",
                        "starter": """from langgraph.graph import StateGraph, END
from typing import TypedDict

class ContentState(TypedDict):
    task: str
    plan: str
    draft: str
    final_content: str

def planner(state: ContentState) -> ContentState:
    # Create a plan based on task
    plan = f"Plan for '{state['task']}':\\n1. Introduction\\n2. Core concepts\\n3. Example\\n4. Summary"
    return {"plan": plan}

def writer(state: ContentState) -> ContentState:
    # Write draft based on plan
    # Add your code here
    pass

def editor(state: ContentState) -> ContentState:
    # Polish the draft into final content
    # Add your code here
    pass

# Build the graph
wf = StateGraph(ContentState)
# Add nodes and edges here

# Compile and run
app = wf.compile()
result = app.invoke({
    "task": "Write a Python tutorial intro",
    "plan": "", "draft": "", "final_content": ""
})
print(result["final_content"])
""",
                        "solution": """from langgraph.graph import StateGraph, END
from typing import TypedDict

class ContentState(TypedDict):
    task: str
    plan: str
    draft: str
    final_content: str

def planner(state):
    plan = f"Plan for '{state['task']}':\\n1. Introduction\\n2. Core concepts\\n3. Example\\n4. Summary"
    return {"plan": plan}

def writer(state):
    draft = f"# {state['task']}\\n\\nWelcome to Python!\\n\\nBased on plan:\\n{state['plan']}\\n\\nPython is simple, powerful, and used everywhere from web to AI."
    return {"draft": draft}

def editor(state):
    final = state['draft'].replace("simple", "elegant").strip()
    final += "\\n\\n✅ Reviewed and approved by Editor Agent."
    return {"final_content": final}

wf = StateGraph(ContentState)
wf.add_node("planner", planner)
wf.add_node("writer", writer)
wf.add_node("editor", editor)
wf.set_entry_point("planner")
wf.add_edge("planner", "writer")
wf.add_edge("writer", "editor")
wf.add_edge("editor", END)
app = wf.compile()
result = app.invoke({"task": "Write a Python tutorial intro", "plan": "", "draft": "", "final_content": ""})
print(result["final_content"])""",
                        "check": ["Editor Agent"],
                        "hints": [
                            "writer returns {'draft': some_text}",
                            "editor returns {'final_content': polished_text}",
                            "wf.add_edge connects nodes sequentially"
                        ]
                    }
                ],
                "reward": {"xp": 1500, "badge": "👑 Galaxy Hero", "unlock": None}
            }
        ]
    }
}

# ── Portfolio Projects ──────────────────────────────────────────────────────

PORTFOLIO_PROJECTS = [
    {
        "id": "proj_001",
        "title": "🤖 AI Chatbot with Memory",
        "difficulty": "Intermediate",
        "xp": 500,
        "time": "2-3 hours",
        "tech": ["Python", "LangChain", "Anthropic API", "Streamlit"],
        "description": "Build a context-aware chatbot that remembers conversation history. Users can set a persona and the bot maintains context across turns.",
        "what_you_learn": ["LangChain memory", "Conversation chains", "Streamlit chat UI", "API integration"],
        "github_topics": ["chatbot", "langchain", "anthropic", "streamlit"],
        "steps": [
            "Set up Streamlit chat interface with message history",
            "Integrate Claude API via LangChain",
            "Add ConversationBufferMemory for context",
            "Add system prompt / persona selector",
            "Deploy to Streamlit Cloud"
        ],
        "starter_code": '''import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

st.title("🤖 AI Chatbot with Memory")

# Initialize
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()
if "messages" not in st.session_state:
    st.session_state.messages = []

llm = ChatAnthropic(model="claude-sonnet-4-20250514")
chain = ConversationChain(llm=llm, memory=st.session_state.memory)

# TODO: Add chat UI, handle input, display messages
# HINT: Use st.chat_input() and st.chat_message()
''',
        "color": "#A78BFA"
    },
    {
        "id": "proj_002",
        "title": "📊 Data Dashboard",
        "difficulty": "Intermediate",
        "xp": 600,
        "time": "3-4 hours",
        "tech": ["Python", "Pandas", "Plotly", "Streamlit"],
        "description": "Upload any CSV and get instant AI-powered analysis with interactive charts, statistics, and natural language insights.",
        "what_you_learn": ["Pandas data analysis", "Plotly visualizations", "File upload in Streamlit", "AI data insights"],
        "github_topics": ["data-analysis", "pandas", "plotly", "streamlit"],
        "steps": [
            "CSV file upload with Streamlit file_uploader",
            "Auto-detect column types (numeric vs categorical)",
            "Generate charts: histogram, scatter, correlation matrix",
            "Add AI insights using Claude API",
            "Export analysis as PDF report"
        ],
        "starter_code": '''import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 AI Data Dashboard")

uploaded = st.file_uploader("Upload CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    st.write(f"Shape: {df.shape}")
    st.dataframe(df.head())
    
    # TODO: Add column selector, chart type picker
    # TODO: Generate plotly charts
    # TODO: Add AI insights button
    col = st.selectbox("Column to analyze:", df.columns)
    if df[col].dtype in ["int64", "float64"]:
        fig = px.histogram(df, x=col)
        st.plotly_chart(fig)
''',
        "color": "#34D399"
    },
    {
        "id": "proj_003",
        "title": "🔍 Document Q&A (RAG)",
        "difficulty": "Advanced",
        "xp": 800,
        "time": "4-5 hours",
        "tech": ["Python", "LangChain", "FAISS", "Anthropic", "Streamlit"],
        "description": "Upload PDFs and chat with them! Ask questions, get accurate answers with source citations. A real enterprise RAG system.",
        "what_you_learn": ["RAG architecture", "Vector embeddings", "FAISS vector store", "PDF processing", "Source attribution"],
        "github_topics": ["rag", "langchain", "pdf-chatbot", "vector-database"],
        "steps": [
            "PDF upload and text extraction with PyPDF2",
            "Chunk documents with RecursiveCharacterTextSplitter",
            "Create embeddings and store in FAISS",
            "Build retrieval chain with source citations",
            "Add chat UI with source display"
        ],
        "starter_code": '''import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_anthropic import ChatAnthropic
from langchain.chains import RetrievalQA
import tempfile, os

st.title("🔍 Chat with Your Documents")

uploaded = st.file_uploader("Upload PDF", type="pdf")
if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(uploaded.read())
        tmp_path = f.name
    
    # TODO: Load, split, embed, store
    # TODO: Build QA chain
    # TODO: Chat interface
    st.info("PDF loaded! Build the RAG pipeline...")
''',
        "color": "#38BDF8"
    },
    {
        "id": "proj_004",
        "title": "🕸️ Autonomous Research Agent",
        "difficulty": "Expert",
        "xp": 1200,
        "time": "5-7 hours",
        "tech": ["Python", "LangGraph", "LangChain", "Anthropic", "Tavily Search"],
        "description": "Build an AI agent that autonomously researches topics, writes reports, fact-checks itself, and produces cited documents. Real agentic AI.",
        "what_you_learn": ["LangGraph stateful agents", "Tool use", "Web search integration", "Self-reflection loops", "Report generation"],
        "github_topics": ["langgraph", "ai-agent", "research-agent", "autonomous-ai"],
        "steps": [
            "Define agent state with TypedDict",
            "Implement researcher node (web search + summarize)",
            "Implement writer node (structured report)",
            "Implement fact-checker node (verify claims)",
            "Add conditional edges for revision loop",
            "Export final report as Markdown"
        ],
        "starter_code": '''from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from typing import TypedDict, List

llm = ChatAnthropic(model="claude-sonnet-4-20250514")

class ResearchState(TypedDict):
    topic: str
    search_results: List[str]
    draft_report: str
    fact_check_notes: str
    final_report: str
    revision_count: int
    approved: bool

def researcher(state: ResearchState) -> ResearchState:
    # TODO: Search web for topic, collect results
    pass

def writer(state: ResearchState) -> ResearchState:
    # TODO: Write structured report from search results
    pass

def fact_checker(state: ResearchState) -> ResearchState:
    # TODO: Check facts, decide if revision needed
    pass

def should_revise(state: ResearchState) -> str:
    # TODO: Return "writer" to revise or END to finish
    pass

# TODO: Build and compile the graph
''',
        "color": "#FBBF24"
    },
    {
        "id": "proj_005",
        "title": "🌐 Full-Stack Web App",
        "difficulty": "Expert",
        "xp": 1500,
        "time": "8-10 hours",
        "tech": ["Python", "FastAPI", "SQLAlchemy", "React/HTML", "Docker"],
        "description": "Build and deploy a complete full-stack application: FastAPI backend, SQLite database, HTML/CSS/JS frontend, and Docker containerization.",
        "what_you_learn": ["REST API design", "Database ORM", "Frontend integration", "CORS", "Docker basics", "Deployment"],
        "github_topics": ["fastapi", "full-stack", "sqlalchemy", "docker"],
        "steps": [
            "Design database schema with SQLAlchemy models",
            "Build FastAPI CRUD endpoints with Pydantic validation",
            "Create HTML/CSS/JS frontend that calls the API",
            "Add authentication with JWT tokens",
            "Write Dockerfile and docker-compose.yml",
            "Deploy to Railway or Render"
        ],
        "starter_code": '''# main.py — FastAPI Backend
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], 
                   allow_methods=["*"], allow_headers=["*"])

# TODO: Set up database
# TODO: Create models
# TODO: CRUD endpoints
# TODO: Add to index.html frontend

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''',
        "color": "#FB923C"
    }
]

# Additional battle questions for new planets
EXTRA_BATTLE_QUESTIONS = {
    "api_expert": [
        {"q": "What HTTP method is used to CREATE a resource in REST?", "options": ["GET","POST","PUT","DELETE"], "answer": 1, "topic": "REST API"},
        {"q": "What status code means 'Not Found'?", "options": ["200","201","404","500"], "answer": 2, "topic": "HTTP"},
        {"q": "In FastAPI, what does `Depends()` do?", "options": ["Imports a module","Dependency injection","Deletes a route","Adds middleware"], "answer": 1, "topic": "FastAPI"},
        {"q": "What is Pydantic used for in FastAPI?", "options": ["Database ORM","Data validation and serialization","Routing","Authentication"], "answer": 1, "topic": "FastAPI"},
        {"q": "Which SQL command retrieves data?", "options": ["INSERT","UPDATE","SELECT","DELETE"], "answer": 2, "topic": "SQL"},
        {"q": "What does `db.commit()` do in SQLAlchemy?", "options": ["Connects to DB","Saves changes permanently","Closes connection","Rolls back"], "answer": 1, "topic": "SQLAlchemy"},
        {"q": "What is CORS?", "options": ["A database type","Cross-Origin Resource Sharing — controls API access","A Python library","An HTTP method"], "answer": 1, "topic": "Web"},
        {"q": "Docker containerizes apps to ensure they run...", "options": ["Faster","The same everywhere","With less code","Only on Linux"], "answer": 1, "topic": "DevOps"},
    ]
}

# New certificates for new planets
EXTRA_CERTIFICATES = [
    {
        "id": "cert_backend",
        "title": "Backend Engineering",
        "subtitle": "API & Database Master",
        "planet": "saturn",
        "required_missions": ["sat_001", "sat_002"],
        "color": "#C084FC",
        "icon": "🪐"
    },
    {
        "id": "cert_ai_advanced",
        "title": "Advanced AI Engineer",
        "subtitle": "RAG & Multi-Agent Master",
        "planet": "neptune",
        "required_missions": ["nep_001", "nep_002"],
        "color": "#06B6D4",
        "icon": "🧠"
    }
]
