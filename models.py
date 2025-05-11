from pydantic import BaseModel

class DocxModel(BaseModel):
	docxUrl: str

class ChatModel(BaseModel):
	secretaryQuestion: str