# Min
# Test script for RAG MCP Server

import subprocess
import json
import os
import time


def test_rag_mcp_server():
    # Start server
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env = os.environ.copy()
    env["PYTHONPATH"] = current_dir + os.pathsep + env.get("PYTHONPATH", "")

    print("Starting RAG server...")
    proc = subprocess.Popen(
        ["python", "rag_mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        cwd=current_dir,
        env=env
    )

    def send_request(request):
        # Send request via stdin/stdout
        try:
            # Send request
            proc.stdin.write(json.dumps(request) + "\n")
            proc.stdin.flush()

            # Read response
            response_line = proc.stdout.readline()
            if response_line:
                return json.loads(response_line)
            else:
                return {"error": "No response from server"}
        except Exception as e:
            return {"error": str(e)}

    try:
        # PDF parsing test
        print("\n=== Test 1: PDF Parsing ===")
        test_request = {
            "tool": "pdf_parser",
            "function": "parse_pdf",
            "inputs": {
                "pdf_path": "C:/Users/lmesd/OneDrive/桌面/Test-file/EJ333.pdf",
                "parser_type": "advanced",
                "chunk_size": 3
            }
        }
        print("Sending request:", json.dumps(test_request, indent=2))
        result = send_request(test_request)
        print("Result:", json.dumps(result, indent=2))

        # Embedding test
        print("\n=== Test 2: Text Embedding ===")
        test_texts = [
            "This is the first test text.",
            "This is the second test text.",
            "This is the third test text."
        ]
        test_request = {
            "tool": "embedding",
            "function": "embed_texts",
            "inputs": {
                "texts": test_texts,
                "model_name": "all-MiniLM-L6-v2"
            }
        }
        print("Sending request:", json.dumps(test_request, indent=2))
        result = send_request(test_request)
        print("Result:", json.dumps(result, indent=2))

        # Create vector index test
        print("\n=== Test 3: Create Vector Index ===")
        test_request = {
            "tool": "embedding",
            "function": "create_vector_index",
            "inputs": {
                "texts": test_texts,
                "model_name": "all-MiniLM-L6-v2"
            }
        }
        print("Sending request:", json.dumps(test_request, indent=2))
        result = send_request(test_request)
        print("Result:", json.dumps(result, indent=2))

        # Similarity search test
        print("\n=== Test 4: Similarity Search ===")
        test_request = {
            "tool": "embedding",
            "function": "search_similar",
            "inputs": {
                "query": "test text",
                "top_k": 2
            }
        }
        print("Sending request:", json.dumps(test_request, indent=2))
        result = send_request(test_request)
        print("Result:", json.dumps(result, indent=2))

    finally:
        # Clean up
        print("\nStopping server...")
        proc.terminate()
        proc.wait()
        print("Server stopped")


if __name__ == "__main__":
    test_rag_mcp_server()
### #%#