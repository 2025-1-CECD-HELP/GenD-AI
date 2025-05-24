from fastapi import FastAPI, File, UploadFile, Form  # FastAPI import
from stt import transcribe_audio, template1_generate, template2_generate, template3_generate  # Importing functions from stt module
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

@app.post("/meetings")
async def upload_to_local(templateId: str = Form(), meetingRecord: UploadFile = File(...), ):
	# tmp_path, tmp_file = upload_file_to_local(meetingRecord)
	# upload_path = upload_file_to_s3(meetingRecord, tmp_file)
	# transcription = transcribe_audio(tmp_path)

	# if templateId == '1':
	# 	minutes = template1_generate(transcription, 4)
	# elif templateId == '2':
	# 	minutes = template2_generate(transcription)
	# result = []
	# for i in minutes.keys():
	# 	result.append({
	# 		"objectKey": i,
	# 		"objectValue": minutes[i]
    #     })

	# return {
	# 	"data": {
	# 		"templateContent": result,
	# 	},
	# 	"error": False,
	# 	"success": True,
	# 	# "s3Url": upload_path,
	# 	# "fileName": tmp_file
    # }
	return {
		"data": {
			"templateContent": [
				{
					"objectKey": "동아리 이름",
					"objectValue": "환경보호 동아리"
				},
				{
					"objectKey": "활동 일시",
					"objectValue": "2024년 6월 15일 오후 2시부터 5시까지"
				},
				{
					"objectKey": "활동 장소",
					"objectValue": "서울시 한강공원"
				},
				{
					"objectKey": "활동 목적",
					"objectValue": "한강공원 내 쓰레기 수거 및 환경 정화 활동을 통해 지역사회 환경 보호 의식 증진"
				},
				{
					"objectKey": "총 원",
					"objectValue": 4
				},
				{
					"objectKey": "활동 인원",
					"objectValue": 4
				},
				{
					"objectKey": "활동 내용",
					"objectValue": "2024년 6월 15일, 환경보호 동아리는 서울시 한강공원에서 환경 정화 활동을 실시하였다. 이번 활동은 지역사회 내 환경 보호 의식을 높이고, 공원 내 쓰레기 문제를 해결하기 위한 목적으로 진행되었다. 총 4명의 동아리 회원이 참여하였으며, 각자 분담하여 공원 내 주요 산책로와 휴식 공간을 중심으로 쓰레기 수거 작업을 수행하였다. 활동 중에는 플라스틱, 종이, 캔 등 다양한 종류의 쓰레기가 수거되었으며, 특히 플라스틱 폐기물이 다수 발견되어 환경 오염의 심각성을 다시 한 번 인식하는 계기가 되었다. 수거된 쓰레기는 분리수거 기준에 따라 재활용 가능한 자원과 일반 폐기물로 구분하여 처리하였다. 또한, 활동 후에는 간단한 환경 보호 교육 시간을 마련하여 동아리원들이 지속적으로 환경 보호에 관심을 가질 수 있도록 하였다. 이번 활동을 통해 지역사회 환경 개선에 기여함과 동시에 동아리원들의 환경 의식이 한층 강화되는 성과를 거두었다."
				},
				{
					"objectKey": "특기 사항",
					"objectValue": "이번 활동은 예상보다 많은 양의 쓰레기가 수거되어 환경 오염 문제의 심각성을 재확인하는 계기가 되었다. 또한, 소수 인원임에도 불구하고 체계적인 분담과 협력으로 효율적인 정화 활동이 이루어졌다. 앞으로도 정기적인 환경 정화 활동과 교육을 통해 지역사회와 함께하는 지속 가능한 환경 보호를 실천할 계획이다."
				},
				{
					"objectKey": "동아리 대표",
					"objectValue": "김민수"
				},
				{
					"objectKey": "지도 교사",
					"objectValue": "이영희"
				}
			],
		},
		"error": False,
		"success": True,
	}

@app.post("/dev")
async def upload_to_s3(templateId: str = Form()):
	# tmp_path, tmp_file = upload_file_to_local(meetingRecord)
	# upload_path = upload_file_to_s3(meetingRecord, tmp_file)
	file = open('/home/teom142/goinfre/study/ai_study/stt/trans2.txt', 'r')
	transcription = file.read()
	file.close()
	# transcription = transcribe_audio(tmp_path)

	if templateId == '1':
		minutes = template1_generate(transcription, 4)
	elif templateId == '2':
		minutes = template2_generate(transcription)
	elif templateId == '3':
		minutes = template3_generate(transcription)
	result = []
	for i in minutes.keys():
		result.append({
			"objectKey": i,
			"objectValue": minutes[i]
		})

	return {
		"templateContent": result,
	}

@app.post("/meetings/save")
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

@app.post("/secretary")
def chat(request: ChatModel):
	answer = chat_with_sources(request.secretaryQuestion)
	return {
		"data": {
			"secretaryChatId": 1,
			"secretaryQuestion": request.secretaryQuestion,
			"secretaryAnswer": answer
		}
	}
