import uvicorn
import logging
from src.config.settings import settings
from src.server.mcp_server import mcp_server

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    logger.info(f"Starting {settings.MCP_SERVER_NAME} v{settings.MCP_SERVER_VERSION}")

    uvicorn.run(
        "src.server.mcp_server:mcp_server.app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
    )


if __name__ == "__main__":
    main()
