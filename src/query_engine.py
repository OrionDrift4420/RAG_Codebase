from typing import List, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv
import os


class QueryEngine:
    """Process natural language queries and generate responses."""

    def __init__(self):
        """Initialize the query engine with Gemini API."""
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')

    def process_query(self, query: str, relevant_snippets: List[Dict[str, Any]]) -> str:
        """Process a natural language query and generate a response."""
        # Construct prompt with context
        context = "\n".join([
            f"Code snippet {i + 1}:\n{snippet['document']}\n"
            for i, snippet in enumerate(relevant_snippets)
        ])

        prompt = f"""Based on the following code snippets from the codebase:

{context}

Question: {query}

Please provide a detailed explanation of the relevant code functionality."""

        response = self.model.generate_content(prompt)
        return response.text