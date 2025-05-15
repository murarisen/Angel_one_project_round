from pathlib import Path
import fitz  # PyMuPDF
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# -------------------- CONFIG --------------------
POLICY_DIR = Path("policies")
VDB_DIR = Path("vectordb")
EMBED_MODEL = "all-minilm"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# -------------------- HELPERS --------------------
def extract_text(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text

def main():
    start = time.perf_counter()
    pdf_files = sorted(POLICY_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDFs found in 'policies/' folder.")
        return

    print(f"Found {len(pdf_files)} PDFs. Extracting...")
    texts = [extract_text(pdf) for pdf in pdf_files]

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = []
    for text in texts:
        chunks.extend(splitter.split_text(text))
    print(f"Generated {len(chunks)} text chunks.")

    print("Generating embeddings and building FAISS index...")
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    vectordb = FAISS.from_texts(chunks, embeddings)

    VDB_DIR.mkdir(exist_ok=True)
    vectordb.save_local(VDB_DIR.as_posix())
    print(f"Index built and saved in '{VDB_DIR}/' (Time: {time.perf_counter() - start:.1f}s)")

if __name__ == "__main__":
    main()