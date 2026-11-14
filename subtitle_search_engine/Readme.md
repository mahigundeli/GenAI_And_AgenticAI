# AI-Driven Subtitle Search Engine

An advanced Python-based processing pipeline designed to ingest raw subtitle files (SRT, VTT, etc.), apply semantic text splitting, generate highly accurate vector embeddings, and enable automated contextual search over video/show transcripts through an intuitive web dashboard.

---

## 🚀 Features

* **Interactive Streamlit Interface:** A user-friendly web app allowing users to input search terms, scan through loaded subtitle collections, and view results instantly.
* **Semantic Subtitle Chunking:** Uses intelligent text splitters to slice continuous dialog streams into distinct, context-retaining scenes.
* **Vector Retrieval Infrastructure:** Backed by OpenAI Embeddings to translate conversational scripts into queryable dense vectors.
* **Context Optimization:** Engineered to minimize retrieval noise and accurately extract target dialogue segments from large text blocks.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.10+
* **User Interface:** `streamlit`
* **LLM & Embeddings Framework:** `langchain-openai`
* **Data Processing & Splitters:** `langchain-text-splitters`

---

## 📂 Project Structure

```text
├── data/
|   ├── eng_subtitles_database.db
├── models/
│   ├── subtitle_match_result.py
├── services/
│   ├── subtitle_analyzer_service.py
│   ├── subtitle_db_service.py
│   ├── vector_storage_service.py
├── ui/
│   ├── streamlit_ui.py
├── app.py                 # Main Streamlit web application entry point
├── controller.py          
├── README.md              # Project documentation
└── requirements.txt       # List of python dependencies