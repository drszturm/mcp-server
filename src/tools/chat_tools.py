from typing import List, Dict, Any
from src.models.mcp_models import ToolDefinition, CallToolResult, TextContent
from src.models.deepseek_models import DeepSeekMessage
from src.services.deepseek_service import deepseek_service


class ChatTools:
    @staticmethod
    def get_tools() -> List[ToolDefinition]:
        return [
            ToolDefinition(
                name="chat_completion",
                description="Generate text completions using DeepSeek AI",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "messages": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "role": {
                                        "type": "string",
                                        "enum": ["user", "assistant", "system"],
                                    },
                                    "content": {"type": "string"},
                                },
                                "required": ["role", "content"],
                            },
                            "description": "List of messages in the conversation",
                        },
                        "max_tokens": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 4096,
                            "default": 2048,
                            "description": "Maximum number of tokens to generate",
                        },
                        "temperature": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 2.0,
                            "default": 0.7,
                            "description": "Sampling temperature for creativity",
                        },
                    },
                    "required": ["messages"],
                },
            ),
            ToolDefinition(
                name="quick_chat",
                description="Send a single message to DeepSeek and get a response",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message to send to DeepSeek",
                        },
                        "system_prompt": {
                            "type": "string",
                            "description": "Optional system prompt to guide the response",
                        },
                    },
                    "required": ["message"],
                },
            ),
            ToolDefinition(
                name="analyze_text",
                description="Analyze text for sentiment, key points, or summary",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to analyze"},
                        "analysis_type": {
                            "type": "string",
                            "enum": ["sentiment", "summary", "key_points", "all"],
                            "default": "all",
                            "description": "Type of analysis to perform",
                        },
                    },
                    "required": ["text"],
                },
            ),
        ]

    @staticmethod
    async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
        if name == "chat_completion":
            return await ChatTools._handle_chat_completion(arguments)
        elif name == "quick_chat":
            return await ChatTools._handle_quick_chat(arguments)
        elif name == "analyze_text":
            return await ChatTools._handle_analyze_text(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

    @staticmethod
    async def _handle_chat_completion(arguments: Dict[str, Any]) -> CallToolResult:
        messages = [DeepSeekMessage(**msg) for msg in arguments["messages"]]
        max_tokens = arguments.get("max_tokens", 2048)
        temperature = arguments.get("temperature", 0.7)

        result = await deepseek_service.chat_completion(
            messages=messages, max_tokens=max_tokens, temperature=temperature
        )

        return CallToolResult(content=[TextContent(type="text", text=result.content)])

    @staticmethod
    async def _handle_quick_chat(arguments: Dict[str, Any]) -> CallToolResult:
        messages = []

        if "system_prompt" in arguments:
            messages.append(
                DeepSeekMessage(role="system", content=arguments["system_prompt"])
            )

        messages.append(DeepSeekMessage(role="user", content=arguments["message"]))

        result = await deepseek_service.chat_completion(messages=messages)

        return CallToolResult(content=[TextContent(type="text", text=result.content)])

    @staticmethod
    async def _handle_analyze_text(arguments: Dict[str, Any]) -> CallToolResult:
        text = arguments["text"]
        analysis_type = arguments.get("analysis_type", "all")

        prompt = f"Please analyze the following text:\n\n{text}\n\n"

        if analysis_type == "sentiment":
            prompt += "Provide a sentiment analysis (positive, negative, neutral) with confidence level."
        elif analysis_type == "summary":
            prompt += "Provide a concise summary of the main points."
        elif analysis_type == "key_points":
            prompt += "Extract the key points as bullet points."
        else:  # all
            prompt += "Provide a comprehensive analysis including sentiment, summary, and key points."

        messages = [DeepSeekMessage(role="user", content=prompt)]
        result = await deepseek_service.chat_completion(messages=messages)

        return CallToolResult(content=[TextContent(type="text", text=result.content)])
