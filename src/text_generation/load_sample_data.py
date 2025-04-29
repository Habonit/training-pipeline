import pandas as pd
import os
from datetime import datetime

from src.text_generation.crud.speaker_num import SpeakerNumCRUD
from src.text_generation.crud.form import FormCRUD
from src.text_generation.crud.example import ExampleCRUD
from src.text_generation.crud.emotion import EmotionCRUD
from src.text_generation.crud.mapping_speaker_num_form import MappingSpeakerNumFormCRUD
from src.text_generation.crud.mapping_emotion_form import MappingEmotionFormCRUD
from src.text_generation.crud.system_prompt import SystemPromptCRUD
from src.text_generation.crud.generation_prompt import GenerationPromptCRUD
from src.text_generation.crud.creativity import CreativityCRUD
from src.text_generation.crud.length import LengthCRUD
from src.text_generation.crud.generated_text import GeneratedTextCRUD
from src.utils.logger import setup_logger

# 로거 세팅
logger = setup_logger()

# 로그 파일도 추가로 저장
now = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs("logs", exist_ok=True)
logger.add(f"logs/insert_sample_{now}.log", level="DEBUG", encoding="utf-8")

def insert_sample_from_excel(session, excel_path: str, target_sheets: list[str] = None):
    df_dict = pd.read_excel(excel_path, sheet_name=None)

    crud_mapping = {
        'speaker_num': SpeakerNumCRUD,
        'form': FormCRUD,
        'example': ExampleCRUD,
        'emotion': EmotionCRUD,
        'mapping_speaker_num_form': MappingSpeakerNumFormCRUD,
        'mapping_emotion_form': MappingEmotionFormCRUD,
        'system_prompt': SystemPromptCRUD,
        'generation_prompt': GenerationPromptCRUD,
        'creativity': CreativityCRUD,
        'length': LengthCRUD,
        'generated_text': GeneratedTextCRUD,
    }

    insert_order = [
        'speaker_num',
        'form',
        'example',
        'emotion',
        'mapping_speaker_num_form',
        'mapping_emotion_form',
        'system_prompt',
        'generation_prompt',
        'creativity',
        'length',
        'generated_text'
    ]

    for sheet_name in insert_order:
        if target_sheets and sheet_name not in target_sheets:
            continue

        if sheet_name not in df_dict:
            logger.warning(f"[스킵] {sheet_name} 시트 없음")
            continue

        if sheet_name not in crud_mapping:
            logger.warning(f"[스킵] {sheet_name}은 CRUD 매핑이 없습니다.")
            continue

        df = df_dict[sheet_name]
        crud_class = crud_mapping[sheet_name]
        crud = crud_class(session)

        records = df.to_dict(orient="records")
        inserted_count = 0

        for record in records:
            try:
                clean_record = {k: (None if pd.isna(v) else v) for k, v in record.items() if k != 'id'}
                crud.create(**clean_record)
                inserted_count += 1
            except Exception as e:
                session.rollback()
                logger.error(f"[에러] {sheet_name} 레코드 삽입 중 오류 발생: {e}")
                continue

        try:
            session.commit()
            logger.success(f"[완료] {sheet_name} 테이블에 {inserted_count}개 레코드 삽입 완료.")
        except Exception as e:
            session.rollback()
            logger.error(f"[에러] {sheet_name} 테이블 커밋 중 오류 발생: {e}")
