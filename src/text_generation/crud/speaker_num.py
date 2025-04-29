from sqlalchemy.orm import Session
from src.text_generation.db_model import SpeakerNum

class SpeakerNumCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, speaker_num: int) -> SpeakerNum:
        obj = SpeakerNum(speaker_num=speaker_num)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def read(self, speaker_num_id: int) -> SpeakerNum | None:
        return self.session.query(SpeakerNum).filter(SpeakerNum.id == speaker_num_id).first()

    def read_all(self, skip: int = 0, limit: int = 100) -> list[SpeakerNum]:
        return self.session.query(SpeakerNum).offset(skip).limit(limit).all()

    def update(self, speaker_num_id: int, speaker_num: int = None) -> SpeakerNum | None:
        obj = self.read(speaker_num_id)
        if not obj:
            return None
        if speaker_num is not None:
            obj.speaker_num = speaker_num
        self.session.commit()
        return obj

    def delete(self, speaker_num_id: int) -> SpeakerNum | None:
        obj = self.read(speaker_num_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj
