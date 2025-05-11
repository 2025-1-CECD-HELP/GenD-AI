from fastapi import FastAPI, File, UploadFile  # FastAPI import
from stt import transcribe_audio, k_analysis  # Importing functions from stt module
from audio_upload import upload_file_to_local, upload_file_to_s3  # Importing functions from audio_upload module
from docx_to_db import docx_to_pine
from docx_rag import chat_with_sources
from models import DocxModel, ChatModel  # Importing Pydantic models
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

TMP_DIR = os.getenv("TMP_DIR")

@app.get("/")
def printHello():
	return "Hello World"

@app.post("/api/v1/meetings")
async def upload_to_local(meetingRecord: UploadFile = File(...)):
	tmp_path, tmp_file = upload_file_to_local(meetingRecord)
	upload_path = upload_file_to_s3(meetingRecord, tmp_file)
	transcription = transcribe_audio(tmp_path)
    # meetingRecord = open('/home/teom142/goinfre/study/ai_study/stt/trans2.txt', 'r')
    # transcription = meetingRecord.read()
    # meetingRecord.close()
	minutes = k_analysis(transcription, 4)
	result = []
	for i in minutes.keys():
		result.append({
			"objectKey": i,
			"objectValue": minutes[i]
        })

	return {
		# "minutes": result
		"s3Url": upload_path,
		"fileName": tmp_file
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
