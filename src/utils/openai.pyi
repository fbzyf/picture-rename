from typing import Any, Dict, List, Optional

class OpenAI:
    def __init__(self, api_key: str, base_url: str) -> None: ...
    
    class chat:
        class completions:
            @staticmethod
            def create(
                model: str,
                messages: List[Dict[str, str]],
                max_tokens: int = ...,
                temperature: float = ...
            ) -> Any: ... 