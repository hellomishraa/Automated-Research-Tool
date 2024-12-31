import streamlit as st
import yaml
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import pickle
import os


# Load OpenAI API key from config
def load_config():
    with open("../config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = config["openai_api_key"]

# App layout
st.title("Automated Scheme Research Tool")
st.sidebar.header("Input URLs")

# Sidebar inputs
urls = st.sidebar.text_area("Enter URLs (one per line):", height=150)

if st.sidebar.button("Process URLs"):
    if urls:
        # Extract and process articles
        url_list = urls.strip().split("\n")
        st.info("Fetching and processing articles...")

        # Load content from URLs
        loader = UnstructuredURLLoader(urls=url_list)
        documents = loader.load()

        # Display the first 500 characters of each document to debug the content
        for i, doc in enumerate(documents):
            st.write(f"Document {i} content preview: {doc.page_content[:500]}")

        # Check if documents were loaded successfully
        if not documents:
            st.error("No content extracted from the provided URLs.")
            raise ValueError("No content extracted.")

        st.success(f"Loaded {len(documents)} articles.")

        # Filter out very short documents
        docs = [doc for doc in documents if len(doc.page_content) >= 200]

        if not docs:
            st.error("After filtering, all documents are too short to generate embeddings.")
            raise ValueError("No valid documents after filtering.")

        st.info(f"Number of valid documents after filtering: {len(docs)}")

        # Text splitting
        st.info("Splitting text into chunks...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        docs = splitter.split_documents(docs)

        # Log document lengths and inspect the content
        st.info(f"Number of documents after splitting: {len(docs)}")
        for i, doc in enumerate(docs):
            st.write(f"Document {i} length: {len(doc.page_content)}")
            if len(doc.page_content) < 100:
                st.warning(f"Document {i} is too short ({len(doc.page_content)} characters). Skipping this document.")

        # Create embeddings and FAISS index
        embeddings = OpenAIEmbeddings()

        # Ensure embeddings are generated
        embeddings_list = embeddings.embed_documents([doc.page_content for doc in docs])
        if not embeddings_list:
            st.error("Failed to generate embeddings. The documents might be too short or empty.")
            raise ValueError("No embeddings generated.")

        # Create FAISS index if embeddings are valid
        if embeddings_list:
            vector_store = FAISS.from_documents(docs, embeddings)
            st.success("FAISS index created successfully.")

            # Save the FAISS index for future use
            with open("faiss_store_openai.pkl", "wb") as f:
                pickle.dump(vector_store, f)
            st.success("FAISS index saved successfully.")

# Load FAISS index
if os.path.exists("faiss_store_openai.pkl"):
    st.sidebar.subheader("Ask a Question")
    question = st.sidebar.text_input("Enter your question:")
    if st.sidebar.button("Get Answer"):
        with open("faiss_store_openai.pkl", "rb") as f:
            vector_store = pickle.load(f)

        retriever = vector_store.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm="gpt-4", retriever=retriever)

        if question:
            st.info("Fetching response...")
            response = qa_chain.run(question)
            st.write("### Answer")
            st.write(response)
        else:
            st.warning("Please enter a question.")
else:
    st.warning("No FAISS index found. Please process URLs first.")
