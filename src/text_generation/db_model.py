from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from dotenv import load_dotenv
import os

Base = declarative_base()

class SpeakerNum(Base):
    __tablename__ = 'speaker_num'
    __table_args__ = {'comment': '글의 화자 수를 저장하는 테이블(0명일 경우 발화 상황이 가정되지 않은 글)'}

    id = Column(Integer, primary_key=True)
    speaker_num = Column(Integer, nullable=False)

class Form(Base):
    __tablename__ = 'form'
    __table_args__ = {'comment': '글의 형태를 정의하는 테이블'}

    id = Column(Integer, primary_key=True)
    form = Column(String, nullable=False)
    description = Column(String, nullable=False)

class Example(Base):
    __tablename__ = 'example'
    __table_args__ = {'comment': '글의 형태에 대한 예시 문장을 저장하는 테이블'}

    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey('form.id'), nullable=False)
    example = Column(Text, nullable=False)

    form = relationship("Form")

class Emotion(Base):
    __tablename__ = 'emotion'
    __table_args__ = {'comment': '글의 감정 상태를 정의하는 테이블'}

    id = Column(Integer, primary_key=True)
    emotion = Column(String, nullable=False)

class MappingSpeakerNumForm(Base):
    __tablename__ = 'mapping_speaker_num_form'
    __table_args__ = {'comment': '화자 수와 글의 형태의 관계를 저장하여 화자 속성을 정의하는 테이블'}

    id = Column(Integer, primary_key=True)
    speaker_num_id = Column(Integer, ForeignKey('speaker_num.id'), nullable=False)
    form_id = Column(Integer, ForeignKey('form.id'), nullable=False)
    attribute = Column(String, nullable=True)

    speaker_num = relationship("SpeakerNum")
    form = relationship("Form")

class MappingEmotionForm(Base):
    __tablename__ = 'mapping_emotion_form'
    __table_args__ = {'comment': '감정 상태와 글의 형태의 관계를 저장하여 글의 어조를 정의하 테이블'}

    id = Column(Integer, primary_key=True)
    emotion_id = Column(Integer, ForeignKey('emotion.id'), nullable=False)
    form_id = Column(Integer, ForeignKey('form.id'), nullable=False)
    tone = Column(String, nullable=True)

    emotion = relationship("Emotion")
    form = relationship("Form")

class SystemPrompt(Base):
    __tablename__ = 'system_prompt'
    __table_args__ = {'comment': '시스템 레벨에서 사용하는 프롬프트를 저장하는 테이블'}

    id = Column(Integer, primary_key=True)
    prompt = Column(Text, nullable=False)

class GenerationPrompt(Base):
    __tablename__ = 'generation_prompt'
    __table_args__ = {'comment': '생성 단계에 입력될 프롬프트 문장을 저장하는 테이블'}

    id = Column(Integer, primary_key=True)
    prompt = Column(Text, nullable=False)

class Creativity(Base):
    __tablename__ = 'creativity'
    __table_args__ = {'comment': '생성 텍스트의 창의성 수준을 정의하는 테이블'}

    id = Column(Integer, primary_key=True)
    degree = Column(Integer, nullable=False)
    description = Column(String, nullable=False)

class Length(Base):
    __tablename__ = 'length'
    __table_args__ = {'comment': '생성 텍스트의 길이 수준을 정의하는 테이블'}

    id = Column(Integer, primary_key=True)
    length = Column(Integer, nullable=False)

class GeneratedText(Base):
    __tablename__ = 'generated_text'
    __table_args__ = {'comment': '생성한 텍스트와 관련 메타데이터를 저장하는 테이블'}

    id = Column(Integer, primary_key=True)
    system_prompt_id = Column(Integer, ForeignKey('system_prompt.id'), nullable=False)
    mapping_speaker_num_form_id = Column(Integer, ForeignKey('mapping_speaker_num_form.id'), nullable=False)
    mapping_emotion_form_id = Column(Integer, ForeignKey('mapping_emotion_form.id'), nullable=False)
    creativity_id = Column(Integer, ForeignKey('creativity.id'), nullable=False)
    length_id = Column(Integer, ForeignKey('length.id'), nullable=False)
    necessary_expression = Column(String, nullable=True)
    style = Column(String, nullable=True)
    theme = Column(String, nullable=True)
    generated_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now())

    system_prompt = relationship("SystemPrompt")
    mapping_speaker_num_form = relationship("MappingSpeakerNumForm")
    mapping_emotion_form = relationship("MappingEmotionForm")
    creativity = relationship("Creativity")
    length = relationship("Length")

# TODO: 하드 코딩 삭제할 예정
#load_dotenv(dotenv_path="/usr/local/project/src/text_generation/.env")
load_dotenv()
DB_NAME = os.environ["TEXT_GENERATION_DB_NAME"]
DB_USER = os.environ["TEXT_GENERATION_DB_USER"]
DB_PASSWORD = os.environ["TEXT_GENERATION_DB_PASSWORD"]

DB_HOST = os.environ["POSTGRES_HOST"]
DB_PORT = os.environ["POSTGRES_PORT"]

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)