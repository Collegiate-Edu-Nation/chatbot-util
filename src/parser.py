from typing import List
from langchain_core.output_parsers import BaseOutputParser

# Define the output parser to read lines. Adapted from multi_query.py
class LineListOutputParser(BaseOutputParser[List[str]]):
    """Output parser for a list of lines."""

    def remove_empty(self, lines):
        """Remove empty lines"""
        for line in lines:
            if line == '':
                lines.remove(line)
        return lines

    def remove_numbers(self, lines):
        """Remove numbers"""
        for i, line in enumerate(lines):
            if line[1] == ".":
                lines[i] = line[3:]
        return lines

    def parse(self, text: str) -> List[str]:
        """Parse lines from LLM and clean them before returning"""
        lines = text.strip().split("\n")
        nonempty_lines = self.remove_empty(lines)
        cleaned_lines = self.remove_numbers(nonempty_lines)
        return cleaned_lines