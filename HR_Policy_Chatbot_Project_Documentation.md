# HR Policy Chatbot Project Documentation

---

## Project Overview and Usage

This project implements an HR Policy Chatbot using Streamlit and LangChain with Ollama embeddings and language models. The chatbot allows users to ask questions about various HR policies, such as Leave, Remote Work, Dress Code, Harassment, Appraisals, and Security, and receive relevant answers based on the indexed policy documents.

### Key Components

- **Policies/**: Directory containing HR policy documents in PDF format.
- **build_index.py**: Script to extract text from policy PDFs, split into chunks, generate embeddings, and build a FAISS vector index.
- **vectordb/**: Directory where the FAISS index files are saved.
- **hr_policy_chatbot_streamlit.py**: Streamlit app that loads the FAISS index and provides a chat interface for querying the policies.
- **requirements.txt**: Lists the Python dependencies with specific version pins for reproducibility.

### Workflow

1. Run `build_index.py` to process the policy PDFs and build the FAISS index.
2. Launch the Streamlit app by running `hr_policy_chatbot_streamlit.py`.
3. Use the chat interface to ask questions about HR policies.
4. The app retrieves relevant information from the indexed documents and provides answers.

### Installation and Setup

1. Create a Python virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the `Policies/` directory contains the relevant PDF documents.

4. Build the vector index:

   ```bash
   python build_index.py
   ```

5. Run the Streamlit app:

   ```bash
   streamlit run hr_policy_chatbot_streamlit.py
   ```

### Usage

- Open the Streamlit app in your browser.
- Enter your questions related to HR policies in the chat input.
- The chatbot will respond with answers based on the indexed policy documents.
- If the index is missing, the app will prompt you to run `build_index.py`.

---

## Project Architecture and Design

### Architecture Overview

The HR Policy Chatbot project is designed as a document-based question answering system that leverages modern NLP techniques to provide users with accurate answers about company HR policies. The architecture consists of the following layers:

1. **Data Layer**  
   - Contains HR policy documents in PDF format stored in the `Policies/` directory.
   - These documents serve as the knowledge base for the chatbot.

2. **Indexing Layer**  
   - The `build_index.py` script extracts text from PDFs using PyMuPDF.
   - Text is split into manageable chunks using LangChain's RecursiveCharacterTextSplitter.
   - Embeddings for each chunk are generated using OllamaEmbeddings.
   - A FAISS vector index is built from these embeddings and saved in the `vectordb/` directory.

3. **Application Layer**  
   - The Streamlit app (`hr_policy_chatbot_streamlit.py`) loads the FAISS index.
   - It uses Ollama LLM to perform retrieval-augmented generation via LangChain's RetrievalQA chain.
   - The app provides a chat interface for multi-turn conversations with users.

### Design Details

#### Text Extraction and Chunking

- PDFs are parsed page by page to extract raw text.
- Text is split into chunks of 500 characters with 50 characters overlap to preserve context.
- This chunking strategy balances retrieval granularity and context retention.

#### Embeddings and Vector Store

- OllamaEmbeddings model "all-minilm" is used for fast and efficient embedding generation.
- FAISS is used as the vector store for similarity search, enabling quick retrieval of relevant chunks.

#### Language Model and QA Chain

- Ollama LLM model "llama3" (configurable) is used for generating answers.
- The RetrievalQA chain combines the retriever (FAISS) and the LLM to answer user queries.
- The chain is configured to return answers without source documents for a clean chat experience.

#### Streamlit UI

- The UI maintains chat history in session state for multi-turn conversations.
- User inputs are sent to the QA chain, and responses are displayed with role-based avatars.
- The app checks for the presence of the FAISS index and prompts to build it if missing.

### Dependencies and Environment

- Python 3.8+ recommended.
- Key libraries: streamlit, langchain, langchain-community, pymupdf, faiss-cpu, ollama, numpy, tiktoken.
- Ollama CLI and models must be installed and configured separately.

---

## Improvement and Future Plans Roadmap

### Current Improvements (Short-Term)

1. **Speed Optimization**
   - Switch to smaller/faster Ollama models like `mistral`, `phi`, or `gemma` for faster response times.
   - Enable streaming responses in Streamlit to display tokens as they are generated.
   - Optimize indexing by:
     - Using efficient chunk sizes (300–500 tokens with overlap).
     - Experimenting with FAISS index types like `IndexFlatL2` or quantized indexes for speed.

2. **Multi-turn Conversation Handling**
   - Implement `ConversationalRetrievalChain` to maintain chat history and context.
   - Ensure follow-up questions retain relevance by preserving conversation state.

3. **User Interface Enhancements**
   - Add chat bubble UI with user messages on the right and bot messages on the left.
   - Display typing animations while the bot generates responses.
   - Support emoji and markdown formatting in chat replies.
   - Add quick action buttons for common topics like "Leave Policy", "Dress Code", "Remote Work".

### Medium-Term Enhancements

4. **Source Document Transparency**
   - Display source document snippets or page references alongside answers.
   - Allow users to view the original policy text for verification.

5. **Incremental Index Updates**
   - Enable updating the FAISS index incrementally when new or updated policies are added.
   - Avoid full re-indexing to save time and resources.

6. **User Authentication and Access Control**
   - Add login functionality with role-based access to restrict sensitive information.
   - Customize answers based on user roles (e.g., Intern, Manager).

7. **Analytics and Feedback**
   - Track user queries and chatbot performance metrics.
   - Collect user feedback to improve answer accuracy and coverage.

### Long-Term and Advanced Features

8. **Hybrid Search**
   - Combine keyword-based (BM25) and vector-based retrieval for improved accuracy.
   - Use `RetrievalQAWithSourcesChain` for richer responses.

9. **Fine-tuning and Domain Adaptation**
   - Fine-tune smaller models (e.g., Mistral with LoRA) on company-specific data.
   - Improve retrieval-augmented generation pipelines for better alignment with HR policies.

10. **Deployment and Scalability**
    - Containerize the app using Docker.
    - Deploy on cloud platforms like Streamlit Cloud, Render, or AWS EC2.
    - Implement CI/CD pipelines for automated testing and deployment.

11. **Voice Interaction**
    - Add voice input and output capabilities using libraries like `SpeechRecognition` and `pyttsx3`.

12. **Policy Update Notifications**
    - Notify users proactively about changes or updates in HR policies via chatbot.

### Project Structure Best Practices

```
project/
│
├── data/                # Raw and processed policy PDFs and text files
├── index/               # FAISS index files and related assets
├── src/                 # Core Python modules (chains, retriever, config)
│   ├── chains.py
│   ├── retriever.py
│   └── config.py
├── app/                 # Streamlit frontend application
│   └── main.py
├── requirements.txt     # Project dependencies with version pins
├── README.md            # Project overview and setup instructions
└── docs/                # Documentation files and roadmaps
```

---

This single document consolidates all essential information about the HR Policy Chatbot project, including overview, architecture, usage, improvements, and future plans, providing a comprehensive guide for developers and stakeholders.

# End of Document
