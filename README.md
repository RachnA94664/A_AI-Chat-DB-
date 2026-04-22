🧠 AI Chat DB – Intelligent SQL Chat Agent

AI Chat DB is a full-stack AI-powered application that allows users to interact with a SQL database using natural language. It combines a LangChain + LangGraph backend with a modern frontend UI, enabling seamless chat-based data exploration.

🚀 Features
💬 Chat with your database using natural language
🗄️ Automatic SQL query generation & execution
🧠 Context-aware memory with conversation persistence
✂️ Smart summarization to avoid token overflow
⚡ Async processing for fast responses
🌐 Frontend UI with interactive design
🔌 Multi-LLM support (Groq, OpenAI)
📁 Project Structure
ai_chat_db/
│
├── data/
│   └── demo.db                 # Sample SQLite database
│
├── frontend/                  # Frontend UI
│   ├── index.html
│   └── static/
│       ├── css/
│       ├── fonts/
│       ├── images/
│       └── js/
│
├── chat_logic.py              # Core chat & agent logic
├── main.py                    # Entry point for backend execution
├── DS.ipynb                   # Data Science experiments
├── test.ipynb                 # Testing notebook
│
├── Dockerfile                 # Containerization setup
├── requirements.txt           # Dependencies
│
├── venv/                      # Virtual environment (ignored in Git)
├── __pycache__/               # Compiled Python files
└── .git/                      # Git repository
⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/your-username/ai_chat_db.git
cd ai_chat_db
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
🔑 Environment Setup

Set your API keys:

export OPENAI_API_KEY="your_openai_key"
export GROQ_API_KEY="your_groq_key"

Windows:

setx OPENAI_API_KEY "your_openai_key"
setx GROQ_API_KEY "your_groq_key"
🗄️ Database Configuration

Default database:

data/demo.db

You can replace it with any SQLAlchemy-supported database:

db_uri = "sqlite:///data/demo.db"
▶️ Running the Application
🔹 Run Backend (Python)
python main.py

Or using async function:

import asyncio
from main import run_chat

asyncio.run(run_chat(
    model_name="llama-3.1-8b-instant",
    provider="groq",
    api_key="YOUR_API_KEY",
    db_uri="sqlite:///data/demo.db",
    user_query="Show all students"
))
🌐 Run Frontend

Simply open:

frontend/index.html

Or serve locally:

cd frontend
python -m http.server 8000

Then visit:

http://localhost:8000
🧠 How It Works
User sends a query via UI or backend
Agent checks database schema
Generates SQL query
Executes query using tools
Returns results in Markdown/table format
🧩 Tech Stack
🔹 Backend
Python
LangChain
LangGraph
SQLAlchemy
🔹 AI Models
Groq (LLaMA models)
OpenAI (GPT models)
🔹 Frontend
HTML, CSS, JavaScript
Bootstrap
jQuery
GSAP animations
🐳 Docker Support

Build image:

docker build -t ai-chat-db .

Run container:

docker run -p 8000:8000 ai-chat-db
📊 Example Output
| id | name   | marks |
|----|--------|-------|
| 1  | Rachna | 85    |
| 2  | Aman   | 92    |
🔮 Future Enhancements
📊 Data visualization (charts & graphs)
📁 CSV / Excel upload support
🔐 Authentication system
⚡ FastAPI backend deployment
☁️ Cloud deployment (AWS/GCP)
⚠️ Notes
Do NOT push:
venv/
__pycache__/
.git/

Add to .gitignore:

venv/
__pycache__/
*.pyc
.env
🤝 Contributing
fork → clone → create branch → commit → push → pull request
👩‍💻 Author

Rachna Verma
Data Science Enthusiast 🚀