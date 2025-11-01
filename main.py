from fastapi import FastAPI
from fastapi_mcp import FastAPIMCP

app = FastAPI()

# Example DeepSeek endpoint (replace with your actual DeepSeek API interaction logic)
@app.post("/deepseek_chat")
async def deepseek_chat(prompt: str):
    # Call DeepSeek API here and return response
    return {"response": f"DeepSeek processed: {prompt}"}

mcp_server = FastAPIMCP(
    app,
    name="DeepSeek MCP Server",
    description="Exposes DeepSeek's language models as MCP tools.",
    base_url="http://localhost:8000"  # Adjust as needed
)

# Mount the FastAPI app to the MCP instance
mcp_server.mount(app)