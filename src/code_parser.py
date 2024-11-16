import ast
import libcst
from typing import Dict, List, Any
import os


class CodeParser:
    """Parse and analyze Python source code."""

    def __init__(self):
        self.file_contents = {}

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a single Python file and extract relevant information."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.file_contents[file_path] = content

        # Parse with ast for basic code structure
        tree = ast.parse(content)

        # Extract functions, classes, and docstrings
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)

        return {
            'path': file_path,
            'functions': analyzer.functions,
            'classes': analyzer.classes,
            'docstrings': analyzer.docstrings,
            'imports': analyzer.imports
        }

    def parse_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Recursively parse all Python files in a directory."""
        results = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    results.append(self.parse_file(file_path))
        return results


class CodeAnalyzer(ast.NodeVisitor):
    """Analyze Python AST and extract relevant information."""

    def __init__(self):
        self.functions = []
        self.classes = []
        self.docstrings = []
        self.imports = []

    def visit_FunctionDef(self, node):
        """Extract function definitions and their docstrings."""
        func_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node),
            'lineno': node.lineno
        }
        self.functions.append(func_info)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Extract class definitions and their docstrings."""
        class_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node),
            'lineno': node.lineno
        }
        self.classes.append(class_info)
        self.generic_visit(node)

    def visit_Import(self, node):
        """Extract import statements."""
        for name in node.names:
            self.imports.append(name.name)

    def visit_ImportFrom(self, node):
        """Extract from-import statements."""
        module = node.module if node.module else ''
        for name in node.names:
            self.imports.append(f"{module}.{name.name}")