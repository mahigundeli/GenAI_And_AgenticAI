# 💬 An AI Code Reviewer

This is a simple tool built with Streamlit and LangChain that automatically reviews your Python code using Google's Gemini 2.5 Flash model. It checks your code against professional engineering rules and shows you a clean report in just one fast step.

---

## 📋 What the AI Checks For

The AI looks at your Python code and grades it based on 8 simple points:

1.  **Naming:** Are variables, functions, and classes named clearly so you know what they do?
2.  **Simplicity:** Is the code clean and easy to read? Can a junior developer understand it without getting confused?
3.  **Single Responsibility & DRY:** Does each function do just one job? Did you avoid copying and pasting the same logic?
4.  **Reusability:** Did you use Python’s built-in features instead of writing custom code from scratch?
5.  **Data Validation:** Are user inputs checked properly to protect the app from attacks?
6.  **Security:** Are passwords, tokens, or secret keys hidden safely in environment variables instead of hardcoded in the file?
7.  **Test Coverage:** Are there enough unit or integration tests to check your new features?
8.  **Test Quality:** Are the tests reliable, easy to read, and capable of checking both success and failure cases?

---

## 🛠️ Project Structure

```text
├── app.py                  # The main entry point that runs the app
├── controller.py           # Handles the app state (Login, Logout, Reviews)
├── config/
│   └── settings.py         # Stores the AI model name and system prompts
├── models/
│   └── response_models.py  # Structure for the AI's review answers
├── services/
│   └── review_service.py   # Connects to Gemini and runs the code checks
├── ui/
│   └── streamlit_ui.py     # Controls how the app looks on your screen
└── requirements.txt        # List of Python packages required to run the app