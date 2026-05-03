# 🚀 CodePilotCLI

⚡ Built for developers who want AI assistance directly in the terminal.

CodePilotCLI is a local AI-powered developer assistant that runs in your terminal.  
It helps you understand code, generate git commit messages, and summarize entire projects using a local LLM (Ollama).

No API keys. No cloud. Fully local.

---

## ✨ Features

- 📄 Explain any Python file in simple English  
- 🧾 Generate clean, professional git commit messages  
- 🧠 Summarize entire codebases instantly  
- ⚡ Fully local AI (via Ollama)

---

## ⚙️ Installation

Run:

    pip install -e .

---

## 🧠 Requirements

Make sure you have:

- Python 3.10+
- Ollama installed → https://ollama.com

### Pull and run the model:

    ollama run mistral

Keep Ollama running in the background.

---

## 🚀 Usage

### Explain code

    codepilot explain test.py

### Generate git commit message

    codepilot commit

### Summarize project

    codepilot summarize

---

## 💡 Example

Input:

    codepilot explain test.py

Output:

    This code defines a function that prints messages to the console in sequence.

---

## 🧠 How it works

CodePilotCLI sends your code to a local AI model (Mistral via Ollama) and returns:
- explanations
- git commit messages
- project summaries

Everything runs locally — no external APIs.

---

## 🎯 Why this exists

Developers often waste time on:

- Understanding unfamiliar code
- Writing commit messages
- Getting up to speed on projects

CodePilotCLI automates these tasks.

---

## 🛠 Tech Stack

- Python
- Requests
- Ollama
- Mistral LLM

---

## 📦 Project Structure

codepilotcli/
│
├── codepilotcli/
│   ├── cli.py
│   └── __init__.py
│
├── setup.py
├── README.md
└── test.py

---

## 📜 License

MIT