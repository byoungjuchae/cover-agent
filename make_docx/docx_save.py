from docx import Document
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("docx_save")

@mcp.tool()
def save_docx():
    doc = Document()
    doc.save(f"{save}.docx")


if __name__ =='__main__':
    print("docx_save start")
    mcp.run(transport="stdio")
    