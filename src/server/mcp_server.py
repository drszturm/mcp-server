import logging
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from src.config.settings import settings
from src.models.mcp_models import (
    ListToolsResult,
    CallToolRequest,
    CallToolResult,
    ErrorResponse,
)
from src.tools.chat_tools import ChatTools
from src.services.deepseek_service import deepseek_service
from src.services.langchain_service import langchain_service

logger = logging.getLogger(__name__)


class MCPServer:
    def __init__(self):
        self.app = FastAPI(
            title=settings.MCP_SERVER_NAME,
            version=settings.MCP_SERVER_VERSION,
            docs_url="/docs",
            redoc_url="/redoc",
        )
        self._setup_routes()
        self._setup_middleware()

    def _setup_routes(self):
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "service": settings.MCP_SERVER_NAME}

        @self.app.get("/tools")
        async def list_tools() -> ListToolsResult:
            try:
                tools = ChatTools.get_tools()
                return ListToolsResult(tools=tools)
            except Exception as e:
                logger.error(f"Error listing tools: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/tools/call")
        async def call_tool(request: CallToolRequest) -> CallToolResult:
            try:
                result = await ChatTools.call_tool(request.name, request.arguments)
                return result
            except ValueError as e:
                logger.warning(f"Invalid tool call: {str(e)}")
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                logger.error(f"Error calling tool {request.name}: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/info")
        async def server_info():
            return {
                "name": settings.MCP_SERVER_NAME,
                "version": settings.MCP_SERVER_VERSION,
                "capabilities": {"tools": True, "resources": False, "prompts": False},
            }

        @self.app.get("/lang")
        async def get_lang():
            return langchain_service.invoke("San Francisco")

    def _setup_middleware(self):
        @self.app.middleware("http")
        async def log_requests(request, call_next):
            logger.info(f"Incoming request: {request.method} {request.url}")
            response = await call_next(request)
            logger.info(f"Response status: {response.status_code}")
            return response

    async def startup(self):
        logger.info("Starting DeepSeek MCP Server...")
        await deepseek_service.initialize()
        langchain_service.initialize()

        logger.info("DeepSeek service initialized")

    async def shutdown(self):
        logger.info("Shutting down DeepSeek MCP Server...")
        await deepseek_service.close()
        logger.info("DeepSeek service closed")


# Create server instance
mcp_server = MCPServer()


# Add lifespan events
@mcp_server.app.on_event("startup")
async def startup_event():
    await mcp_server.startup()


@mcp_server.app.on_event("shutdown")
async def shutdown_event():
    await mcp_server.shutdown()
