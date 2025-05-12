from docx import Document
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field


mcp = FastMCP('made_docx')

class DocxInput(BaseModel):
    path : str =Field(description='it is the save path of the docx file')
    content : str = Field(description='it is the cover letter content')
    



@mcp.tool()
def save_docx(input: DocxInput):
    doc = Document()
    doc.add_paragraph(input.content)
    doc.save(input.path)
    
if __name__ =='__main__':
    
    mcp.run(transport="stdio")
    # save_docx('/home/abc.docx','hello')