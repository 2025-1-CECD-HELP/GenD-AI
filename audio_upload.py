import os
import boto3
import string
import secrets
import shutil

from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME= os.getenv("BUCKET_NAME")
TEMP_AUDIO_DIR = os.getenv("TEMP_AUDIO_DIR")

# 민기 s3 버킷
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def random_key(length: int = 20) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def upload_file_to_s3(file, tmp_file):
    # 파일 메타데이터
    filename = file.filename
    content_type = file.content_type
    _, ext = os.path.splitext(filename)
    # S3 객체 키(key) 지정 (원하는 경로로 변경 가능)
    s3_key = f"audio/{tmp_file}"
    s3.upload_fileobj(
            Fileobj=file.file,
            Bucket=BUCKET_NAME,
            Key=s3_key,
            ExtraArgs={"ContentType": content_type}
        )

    # 3) 업로드된 파일의 퍼블릭 URL 생성 (퍼블릭 액세스가 허용되어 있어야 함)
    file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

    return file_url

def upload_file_to_local(file):
    filename = file.filename
    _, ext = os.path.splitext(filename)
    tmp_file = f"{random_key()}{ext}"
    tmp_path = os.path.join(TEMP_AUDIO_DIR, tmp_file)

    # UploadFile.file 을 읽어 로컬 디스크에 저장
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return tmp_path, tmp_file