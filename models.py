from pydantic import BaseModel

class DocxModel(BaseModel):
	docxUrl: str

class ChatModel(BaseModel):
	secretaryQuestion: str

class object(BaseModel):
	objectKey: str
	objectValue: str

class MinutesModel(BaseModel):
	templateContent: list[object]
	templateId: str

class TemplateModel(BaseModel):
	templateId: str