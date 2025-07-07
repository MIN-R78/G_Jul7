# PDF RAG Toolkit

A toolkit for parsing PDF documents, generating text embeddings, and running retrieval-augmented generation (RAG) pipelines. Supports flexible PDF text extraction, vector search with FAISS, and integration with large language models for question answering and summarization.

# Features
- Dual PDF parser support (PyPDF2 and pdfplumber)
- Command-line selection of PDF and parser
- Multilingual query handling (English, Chinese, Korean)
- Summarization mode for long-document queries
- FAISS-based vector similarity search
- Easy integration with LLMs (e.g., Azure OpenAI)

# Getting Started
1. Clone the repository:
   git clone https://github.com/MIN-R78/Google_Jul7.git
   cd Google-Jul7

2. Install dependencies:
   pip install -r requirements.txt

3. (Optional) Set up environment variables for LLM API keys if needed.

4. Start the server:
   python rag_mcp_server.py

5. Run test scripts to interact with the system:
   python simple_test.py
   python test_rag_mcp.py

All configuration and example usage are included in the code files.
