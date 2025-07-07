### Min
### RAG MCP Server
### Main server that combines PDF parser and embedding tools

from typing import Dict, Any, List
import json
import sys
from pdf_parser_mcp import PDFParserTool
from embedding_mcp import EmbeddingTool

class RAGMCPServer:
    def __init__(self):
        self.pdf_tool = PDFParserTool()
        self.embedding_tool = EmbeddingTool()
        self.tools = {
            "pdf_parser": self.pdf_tool,
            "embedding": self.embedding_tool
        }

    def run(self):
        ### Run MCP server and handle requests
        print("Starting RAG MCP Server...")
        print("Available tools:", list(self.tools.keys()))
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                data = json.loads(line)
                tool_name = data.get("tool")
                function_name = data.get("function")
                inputs = data.get("inputs", {})
                if tool_name not in self.tools:
                    print(json.dumps({"error": f"Tool '{tool_name}' not found"}))
                    continue
                tool = self.tools[tool_name]
                if function_name not in tool.functions:
                    print(json.dumps({"error": f"Function '{function_name}' not found in tool '{tool_name}'"}))
                    continue
                result = getattr(tool, function_name)(**inputs)
                print(json.dumps({"output": result}))
            except json.JSONDecodeError as e:
                print(json.dumps({"error": f"Invalid JSON: {str(e)}"}))
            except Exception as e:
                print(json.dumps({"error": f"Unexpected error: {str(e)}"}))

if __name__ == "__main__":
    server = RAGMCPServer()
    server.run()
### #%#