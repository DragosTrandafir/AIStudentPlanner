import json
import re
from typing import Any, Dict


def extract_json_from_llm(text: str) -> Dict[str, Any]:
    """
    Cleans LLM output and extracts valid JSON.
    Handles cases where JSON is wrapped in ```json ``` fences.
    """
    if not text:
        raise ValueError("Empty LLM response")

    # Remove markdown fences if present
    cleaned = re.sub(r"^```json\s*", "", text.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    # Parse JSON
    return json.loads(cleaned)
