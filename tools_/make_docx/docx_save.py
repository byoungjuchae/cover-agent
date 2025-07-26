from docx import Document
from mcp.server.fastmcp import FastMCP
from langchain.tools import tool


@tool
def save_docx(cover_letter:str,save_name:str):
    "If you want to save docx file, use this tool."
    doc = Document()
    doc.add_paragraph(cover_letter)
    doc.save(f"{save_name}.docx")

