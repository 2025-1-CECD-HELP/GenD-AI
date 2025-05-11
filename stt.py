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
    ActivityDetails: str
    SpecialNotes: str
    ClubRepresentative: str
    Supervisor: str

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


def k_analysis(transcription, k):
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

    return output
