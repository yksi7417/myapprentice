import streamlit as st


st.markdown("# Introduction ")

st.markdown("""
**Conversational Automation Assistant**

"My Apprentice" is a chat-driven automation framework designed to streamline both web and desktop tasks using natural language commands and AI-powered agents.
""")

st.header("Key Features")
st.markdown("""
- **Interactive Chat Interface**
Semi-transparent, always-on-top window with system tray integration for seamless user interaction.

- **Plugin-Based Agent System**
Modular agents handle specific tasks (e.g., window control, browser automation, learner agent).

- **Browser Automation with Playwright**
Launch, navigate, interact with web pages, fill forms, and handle multi-tab workflows.

- **AI-Powered DOM Analysis**
Use specialized models (MarkupLM, instruction-tuned LLMs) to dynamically identify form fields and generate CSS selectors.

- **Learner Agent**
Show-and-tell approach: record user interactions, summarize steps, replay tasks, and iterate based on feedback.
""")

st.header("Enable GPU Support")
st.markdown("""
            CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
            """)

st.header("Roadmap")
st.markdown("""
| Milestone	| Status|
|:------------------|:------------------|
| Chat UI & Onboarding	| 🛠 In Work |
| Browser Automation Agent	|✅ Planned |
| Plugin/Agent Registry	| ✅ Planned |
| DOM Pruning & AI Integration |	⏳ Upcoming |
| Learner Agent Implementation|⏳ Upcoming |
""")
