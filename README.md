

# 🧠 AI-Powered Virtual Development Pod

## 📌 Overview

This project simulates a real-world IT development team using a **multi-agent AI system**. It automates key stages of the software development lifecycle — from requirement analysis to code generation and testing.

The system is built using agent orchestration frameworks like **CrewAI** and **LangChain**, with local LLM integration via Ollama.

---

## 🚀 Features

* 📄 **Business Analyst Agent** → Generates user stories from high-level requirements
* 🧩 **Design Agent** → Produces system design based on user stories
* 💻 **Developer Agent** → Generates code from design and requirements
* 🧪 **Testing Agent** → Creates and executes test cases
* 🔄 **Sequential Agent Pipeline** (BA → Design → Dev → Test)
* 🖥️ Basic UI built with Streamlit

---

## 🏗️ Architecture

```
User Input
   ↓
Business Analyst Agent
   ↓
Design Agent
   ↓
Developer Agent
   ↓
Testing Agent
   ↓
Final Output
```

👉 Note:
Currently, agents execute **sequentially**, not in parallel.

---

## 🛠️ Tech Stack

* Python
* Streamlit
* CrewAI
* LangChain
* Ollama (Local LLM)
* ChromaDB / Pinecone (for vector storage)

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/kb-111/College-project
cd College-project

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

---

## ⚠️ Challenges Faced

* High latency due to local LLM (Ollama)
* Difficulty in integrating real-time chatbot functionality
* Managing coordination between multiple agents
* Limited access to paid APIs (e.g., OpenAI)

---

## 📉 Limitations

* Chatbot interface is **not fully implemented**
* Agents do not run in parallel (sequential execution only)
* Performance is slower due to local model usage

---

## 📈 Future Improvements

* Add fully functional chatbot interface
* Enable parallel execution of agents
* Integrate faster cloud-based LLM APIs
* Improve UI/UX for better interaction

---

## 👨‍💻 My Contribution

* Designed and implemented the **core multi-agent workflow**
* Integrated CrewAI and LangChain for agent orchestration
* Built Streamlit interface for interaction
* Handled LLM integration using Ollama

---

## 👥 Team

* Team of 4 (6th Semester Project)

---

## 📸 Screenshots

<img width="1916" height="943" alt="Screenshot 2025-04-13 180859" src="https://github.com/user-attachments/assets/e4f10bce-273f-4af3-a56f-ace46cc4d9ca" />
<img width="1876" height="870" alt="Screenshot 2025-04-13 185007" src="https://github.com/user-attachments/assets/d7d85db7-2bf1-4611-bf98-bb3049f898ce" />
<img width="1891" height="848" alt="Screenshot 2025-04-13 185026" src="https://github.com/user-attachments/assets/8fe4adea-1831-4922-95aa-03ae67a580c0" />
<img width="1208" height="781" alt="Screenshot 2025-04-14 001249" src="https://github.com/user-attachments/assets/aad20c5f-a905-4bf7-ae86-a89b10c9166e" />
<img width="1831" height="804" alt="Screenshot 2025-04-14 011112" src="https://github.com/user-attachments/assets/2ad8ff26-1153-4dc2-a95f-f93e77fe4299" />
<img width="1914" height="873" alt="Screenshot 2025-04-14 000953" src="https://github.com/user-attachments/assets/eafb3c70-8e24-4549-a6ff-5549c15a852a" />



---

## 📌 Note

This project was developed as a **learning-focused implementation of multi-agent AI systems** and is not production-ready.

