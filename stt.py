from openai import OpenAI
from pydantic import BaseModel
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class MinuteFormat(BaseModel):
    ClubName: str
    DateAndTime: str
    LocationOfActivity: str
    PurposeOfActivity: str
    TotalNumberOfParticipants: int
    NumberOfParticipants: int
    ActivityDetails: str
    SpecialNotes: str
    ClubRepresentative: str
    Supervisor: str

minute_format = {
    "ClubName": "동아리 이름",
    "DateAndTime": "활동 일시",
    "LocationOfActivity": "활동 장소",
    "PurposeOfActivity": "활동 목적",
    "TotalNumberOfParticipants": "총 원",
    "NumberOfParticipants": "활동 인원",
    "ActivityDetails": "활동 내용",
    "SpecialNotes": "특기 사항",
    "ClubRepresentative": "동아리 대표",
    "Supervisor": "지도 교사"
}

class tmp2Format(BaseModel):
    Title: str
    Keywords: str
    StructuredNotes: str
    Summary: str

tmp2_format = {
    "Title": "제목",
    "Keywords": "키워드",
    "StructuredNotes": "필기내용",
    "Summary": "요약"
}

def transcribe_audio(audio_file_path):
    client = OpenAI(
    api_key=OPENAI_API_KEY
    )
    with open(audio_file_path, 'rb') as audio_file:
        transcription = client.audio.transcriptions.create(
            model = "whisper-1",
            file=audio_file,
            response_format="text",
        )
    return transcription


def template1_generate(transcription, k):
    client = OpenAI(
    api_key=OPENAI_API_KEY
    )
    
    minutes_k_prompt = f"""
    As the team leader, please prepare a formal report of our recent club activity for public release. Use the STT transcript to ensure accuracy, but present the information in a professional, third-person style. Please provide the information in Korean:

    1. 동아리 Name:
    2. Date and Time of Activity:
    3. Location of Activity:
    4. Purpose of Activity:
    5. Total Number of Participants: {k}
    6. Activity Details: (Please provide a comprehensive summary of approximately 300 words)
    7. Special Notes:

    Guidelines for writing:
    - Use a formal, objective tone appropriate for a public report.
    - In the Activity Details section, provide a clear and concise overview of the main events, achievements, and outcomes of the activity.
    - Focus on factual information and avoid personal opinions or subjective statements.
    - If certain information is not available or unclear, use phrases like "approximately" or "estimated" where appropriate.
    - If there is any information you don't know, mark it as unknown. Don't mark it as an ambiguous wrong answer.
    - In the Special Notes section, include any significant achievements, challenges overcome, or noteworthy occurrences that would be of interest to the public or stakeholders.
    - Ensure the report reflects positively on the club while maintaining honesty and transparency.

    Remember, this report may be viewed by club members, advisors, school officials, or even the general public. Aim to present a professional and comprehensive account of the club's activities. Answer Korean.
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4.1-mini-2025-04-14",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": minutes_k_prompt
            },
            {
                "role": "user",
                "content": transcription
            }
        ],
        response_format=MinuteFormat,
    )
    result = response.choices[0].message.content
    output = json.loads(result)

    processed_output = {}
    for key, value in output.items():
        if key in minute_format:
            processed_output[minute_format[key]] = value
        else:
            processed_output[key] = value

    return processed_output

def template2_generate(transcription):
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    prompt = f"""
    Please create a presentation note-taking template that allows for structured, topic-based organization of content, rather than simple chronological order.

    The template should include:

    1. Title: Area to note the name of the presentation or session
    2. Keywords: A space to list key terms and concepts discussed
    3. Structured Notes:
    - Organize this section into topic-based subheadings (e.g., 서론, 문제 제시, 주요 요점, 사례 연구, 결론)
    - Under each heading, leave room for key points or speaker quotes
    4. Summary: A brief paragraph (3–4 sentences) summarizing the overall message of the presentation

    Additional instructions:
    - Design it to be useful for university students or professionals.
    - Include example content under each heading.
    - Do not use Markdown output format.

    Answer Korean.
    """
    response = client.beta.chat.completions.parse(
        model="gpt-4.1-mini-2025-04-14",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": transcription
            }
        ],
        response_format=tmp2Format,
    )
    result = response.choices[0].message.content
    output = json.loads(result)
    processed_output = {}
    for key, value in output.items():
        if key in tmp2_format:
            processed_output[tmp2_format[key]] = value
        else:
            processed_output[key] = value
    return processed_output