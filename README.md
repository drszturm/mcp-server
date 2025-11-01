# mcp-server
deepseek-mcp-server/
├── pyproject.toml
├── requirements.txt
├── .env.example
├── README.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── server/
│   │   ├── __init__.py
│   │   ├── mcp_server.py
│   │   └── session_manager.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── deepseek_service.py
│   │   └── rate_limiter.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── mcp_models.py
│   │   └── deepseek_models.py
│   ├── tools/
│   │   ├── __init__.py
│   │   └── chat_tools.py
│   └── config/
│       ├── __init__.py
│       └── settings.py
└── tests/
    ├── __init__.py
    ├── test_deepseek_service.py
    └── test_mcp_server.py