# AI Tutor Agent

An interactive multi-agent tutoring system powered by Google Gemini API, built with Flask. It routes user queries to specialized sub-agents (Math, Physics, Chemistry, Biology) which utilize tools and LLM integration.

---

## 🏠 Project Overview

**AI Tutor Agent** helps students ask questions in Math, Physics, Chemistry, and Biology. It features:

* **TutorAgent**: orchestrator routing queries based on subject.
* **MathAgent**: solves arithmetic, algebra, calculus (uses SymPy and Gemini).
* **PhysicsAgent**: answers physics questions (uses constant lookup and Gemini).
* **ChemistryAgent**: answers chemistry queries (uses Gemini).
* **BiologyAgent**: answers biology questions (uses terminology, diagrams, and Gemini).
* **MemoryBuffer**: retains conversation context for follow-up questions.
* **Flask Web UI**: modern, user-friendly web interface with session-based persistence and subject badges.

---

## 📁 Repository Structure

```
ai-tutor-agent-main/
├── agents/
│   ├── tutor_agent.py
│   ├── math_agent.py
│   ├── physics_agent.py
│   ├── chemistry_agent.py
│   └── biology_agent.py
├── tools/
│   ├── calculator.py
│   └── constants_lookup.py
├── utils/
│   ├── classifier.py
│   ├── memory.py
│   └── llm.py
├── templates/
│   └── index.html
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

1. **Clone the repo**

   ```bash
   git clone <your-github-url>
   cd ai-tutor-agent-main
   ```
2. **Create virtual environment**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Configure API Key**

   * Create a `.env` file at project root:

     ```env
     GEMINI_API_KEY=your_api_key_here
     ```
5. **Run the app**

   ```bash
   python main.py
   ```

Open [http://localhost:5000](http://localhost:5000) in your browser and start asking questions!

---

## 📡 Deployment

### Railway

1. Push to GitHub.
2. Create a Railway project and link your GitHub repo.
3. Set the environment variable `GEMINI_API_KEY` in Railway.
4. The included `Procfile` will run the app with Gunicorn.
5. Deploy and access the public URL.

---

## 📦 Agents & Tools

### Agents

* **TutorAgent**: routes queries + manages memory.
* **MathAgent**: uses `tools/calculator.py` (SymPy) and `utils/llm.py`.
* **PhysicsAgent**: uses `tools/constants_lookup.py` and memory-based reminders.
* **ChemistryAgent**: uses `utils/llm.py`.
* **BiologyAgent**: uses terminology, diagrams, and Gemini LLM.

### Tools

* **calculator.py**: robust math expression parser and solver.
* **constants_lookup.py**: dictionary of physics constants.

---

## ⭐ Features

* **Subject detection**: Every question is automatically labeled as Biology, Physics, Math, Chemistry, or Other.
* **Color-coded badges**: Each subject has a unique badge color in the UI.
* **Collapsible answers**: Click to expand/collapse answers for easy navigation.
* **Edit previous questions**: Update your questions and get new answers instantly.
* **Session-based history**: Your Q&A history is stored for the session.
* **Modern Flask UI**: Responsive, user-friendly, and deployable anywhere.

---

## 🔧 Future Improvements

* Add more sub-agents (e.g., Coding agent).
* Advanced tool integration (graphing, unit conversions).
* User authentication and personalized sessions.
* Enhanced diagram generation and interactive features.

---

## 📝 .gitignore

A `.gitignore` is included to exclude virtual environments, `.env`, cache, and other common files from version control.

---

