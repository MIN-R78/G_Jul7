### Min
### Simple test script for RAG MCP Server
### This script tests basic functionality without requiring PDF files

import json
import subprocess
import os


def simple_test():
    """Simple test for RAG MCP server"""

    # Test embedding functionality only (no PDF required)
    test_texts = [
        "Hello world",
        "This is a test",
        "Python programming"
    ]

    # Create test request
    test_request = {
        "tool": "embedding",
        "function": "embed_texts",
        "inputs": {
            "texts": test_texts,
            "model_name": "all-MiniLM-L6-v2"
        }
    }

    print("=== Simple Embedding Test ===")
    print("Request:", json.dumps(test_request, indent=2))

    # Start server process
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env = os.environ.copy()
    env["PYTHONPATH"] = current_dir + os.pathsep + env.get("PYTHONPATH", "")

    try:
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

        # Send request
        stdout, stderr = proc.communicate(json.dumps(test_request) + "\n")

        print("=== Response ===")
        try:
            response = json.loads(stdout)
            print("Success:", response.get("output", {}).get("success", False))
            print("Embedding dimension:", response.get("output", {}).get("embedding_dim", "N/A"))
            print("Number of texts:", response.get("output", {}).get("num_texts", "N/A"))
        except:
            print("Raw output:", stdout)

        if stderr:
            print("=== Error ===")
            print(stderr)

    except Exception as e:
        print(f"Error running test: {e}")
    finally:
        if 'proc' in locals():
            proc.terminate()


if __name__ == "__main__":
    simple_test()
### #%#