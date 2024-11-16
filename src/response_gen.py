class ResponseGenerator:
    """Generate formatted responses for code queries."""

    def format_response(self, query_result: str, relevant_snippets: List[Dict[str, Any]]) -> str:
        """Format the response with relevant code snippets and explanations."""
        response = ["### Query Response\n"]
        response.append(query_result)

        response.append("\n### Relevant Code Snippets\n")
        for i, snippet in enumerate(relevant_snippets, 1):
            response.append(f"\n#### Snippet {i}")
            response.append(f"```python\n{snippet['document']}\n```")

        return "\n".join(response)