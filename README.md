# HR Policy Chatbot

This project implements an HR Policy Chatbot using Streamlit and LangChain with Ollama embeddings and language models. The chatbot allows users to ask questions about various HR policies and receive relevant answers based on indexed policy documents.

## Features

- Semantic search over HR policy PDFs using FAISS vector store.
- Multi-turn conversation with chat history.
- Uses Ollama models for embeddings and language generation.
- Streamlit-based web UI for easy interaction.

## Setup and Installation

1. Create and activate a Python virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Place your HR policy PDF documents in the `Policies/` directory.

4. Build the vector index:

   ```bash
   python build_index.py
   ```

5. Run the Streamlit app:

   ```bash
   streamlit run hr_policy_chatbot_streamlit.py
   ```

## Usage

- Open the Streamlit app in your browser.
- Ask questions related to HR policies in the chat interface.
- The chatbot will respond with answers based on the indexed documents.

## Project Structure

```
project/
│
├── Policies/            # HR policy PDF documents
├── vectordb/            # FAISS index files
├── build_index.py       # Script to build FAISS index from PDFs
├── hr_policy_chatbot_streamlit.py  # Streamlit chatbot app
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── docs/                # Additional documentation
```

## Future Improvements

See the `docs/Improvement_and_Future_Plans_Roadmap.md` for detailed plans on enhancing the project.
