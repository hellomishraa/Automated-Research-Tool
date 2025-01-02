# Automated Scheme Research Tool

This project is a web-based application designed to automate research on various schemes by processing articles from provided URLs. It allows users to ask questions about the schemes and receive concise, relevant answers, along with the source content. 

---

## Features

- **Load URLs:** Accepts one or more URLs of scheme-related articles as input.
- **Text Processing:** Fetches content from URLs, splits it into manageable chunks, and creates embeddings for semantic search.
- **Interactive Q&A:** Users can ask questions, and the system retrieves answers based on the indexed content.
- **Storage:** The FAISS index is stored locally in a pickle file for reuse.

---

## Repository Structure

- **`Src/`**: Contains the main application files.
  - **`main.py`**: The main Streamlit app script.
  - **`config.yaml`**: Configuration file for storing sensitive information like API keys.
  - **`requirements.txt`**: Dependencies required to run the application.
- **`.venv/`**: Virtual environment directory (not included in the repository).
- **`.gitignore`**: Ensures sensitive files like `config.yaml` are not committed.

---

## Prerequisites

1. Python 3.8 or higher
2. Virtual Environment (`venv`) setup
3. OpenAI API Key

---

## Installation and Setup

### Step 1: Clone the Repository

```
git clone https://github.com/<your-username>/Haqdarshak.git

cd Haqdarshak
```

### Step 2: Set Up a Virtual Environment
```
python -m venv .venv

source .venv/bin/activate     # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies
Navigate to the Src folder and install the dependencies:
```
pip install -r requirements.txt
```
---

## Configuration

1. Create a config.yaml file inside the Src directory.
2. Add your OpenAI API key to the file:
```
   openai_api_key: "your_openai_api_key"
```

---

## Usage

**Step 1:** Start the Application
  - Run the following command from the project directory:
```
    streamlit run Src/main.py
```
  
**Step 2:** Provide Input URLs
1. Use the sidebar in the Streamlit interface to paste URLs (one per line) of scheme-related articles.
2. Click the Process URLs button to fetch and process the content.

**Step 3:** Ask Questions
1. Use the query input box to ask questions, e.g., "What are the benefits of the scheme?"
2. Click Submit Query to retrieve answers based on the indexed content.

---

## Project Workflow
- **Input URLs:** Users input URLs of scheme-related articles via the sidebar.
- **Content Loading:** Articles are fetched using LangChain's *UnstructuredURLLoader*.
- **Text Splitting:** Content is split into manageable chunks using *RecursiveCharacterTextSplitter*.
- **Embedding Creation:** Semantic embeddings are generated for the chunks using OpenAI's API.
- **FAISS Indexing:** Chunks are indexed using FAISS for efficient similarity-based searches.
- **Interactive Q&A:** Users can query the system and get answers from the indexed content.

---

## Contributing
Feel free to fork the repository and submit pull requests for improvements or additional features. If you encounter any issues, report them in the **`Issues`** section.

