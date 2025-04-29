import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.text_generation.db_model import Base, SessionLocal
from src.text_generation.load_sample_data import insert_sample_from_excel

# TODO: 하드 코딩 삭제할 예정
# 환경변수 로드 (공통 → text_generation 전용 순으로 덮어쓰기)
# load_dotenv(dotenv_path="/usr/local/project/postgres/.env")                  # 공통 admin 정보
# load_dotenv(dotenv_path="/usr/local/project/src/text_generation/.env")       # text_generation 전용 설정
load_dotenv()

# 설정 값 로드
container = False

db_user = os.environ["TEXT_GENERATION_DB_USER"]
db_password = os.environ["TEXT_GENERATION_DB_PASSWORD"]
db_name = os.environ["TEXT_GENERATION_DB_NAME"]

db_host = os.environ["POSTGRES_HOST"]
admin_user = os.environ["POSTGRES_USER"]
admin_password = os.environ["POSTGRES_PASSWORD"]
db_port = os.environ["POSTGRES_PORT"]

init_flag = os.environ.get("INIT", "false").lower() == "true"
sample_flag = os.environ.get("INSERT_SAMPLE", "false").lower() == "true"

def create_db_and_user():
    conn = psycopg2.connect(
        dbname="postgres",
        user=admin_user,
        password=admin_password,
        host=db_host,
        port=db_port
    )
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}';")
    except Exception as e:
        print(f"ℹ️ 유저 생성 생략 또는 실패: {e}")
    try:
        cur.execute(f"CREATE DATABASE {db_name} OWNER {db_user};")
    except Exception as e:
        print(f"ℹ️ DB 생성 생략 또는 실패: {e}")
    cur.execute(f"GRANT ALL ON SCHEMA public TO {db_user};")
    conn.close()

def create_tables():
    url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(url)

    if init_flag:
        print("♻️ INIT=true → 기존 테이블 삭제 후 재생성 중...")
        Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)
    print("✅ text_generation 테이블 생성 완료")

    if sample_flag:
        print("🧪 INSERT_SAMPLE=true → 샘플 데이터 삽입 중...")
        session = SessionLocal()
        excel_path = "./src/text_generation/sample/text_generation_schema.xlsx"
        insert_sample_from_excel(session, excel_path)
        session.close()

if __name__ == "__main__":
    create_db_and_user()
    create_tables()
