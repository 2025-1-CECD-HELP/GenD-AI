from fastapi import FastAPI, File, UploadFile, Form  # FastAPI import
from stt import transcribe_audio, template1_generate, template2_generate  # Importing functions from stt module
from audio_upload import upload_file_to_local, upload_file_to_s3  # Importing functions from audio_upload module
from docx_to_db import docx_to_pine, docx_to_s3
from docx_rag import chat_with_sources
from models import DocxModel, ChatModel, MinutesModel, TemplateModel  # Importing Pydantic models
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

TMP_DIR = os.getenv("TMP_DIR")

@app.get("/")
def printHello():
	return "Hello World"

@app.post("/api/v1/meetings")
async def upload_to_local(templateId: str = Form(), meetingRecord: UploadFile = File(...), ):
	tmp_path, tmp_file = upload_file_to_local(meetingRecord)
	upload_path = upload_file_to_s3(meetingRecord, tmp_file)
	transcription = transcribe_audio(tmp_path)

	if templateId == '1':
		minutes = template1_generate(transcription, 4)
	elif templateId == '2':
		minutes = template2_generate(transcription)
	result = []
	for i in minutes.keys():
		result.append({
			"objectKey": i,
			"objectValue": minutes[i]
        })

	return {
		"templateContent": result,
		"s3Url": upload_path,
		"fileName": tmp_file
    }

@app.post("/api/v1/meetings/save")
def save_meeting_minutes(request: MinutesModel):
	file_url = docx_to_s3(request.templateContent, request.templateId)
	return {
		"fileUrl": file_url
	}

@app.post("/api/v1/docx")
def s3_to_pinecone(request: DocxModel):
	result = docx_to_pine(request.url)
	return {
        "result": result,
    }

@app.post("/api/v1/secretary")
def chat(request: ChatModel):
	answer = chat_with_sources(request.secretaryQuestion)
	return {
		"secretaryChatId": 1,
		"secretaryQuestion": request.secretaryQuestion,
		"secretaryAnswer": answer
	}
