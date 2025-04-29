from sqlalchemy.orm import Session
from src.text_generation.db_model import Emotion

class EmotionCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, emotion: str) -> Emotion:
        obj = Emotion(emotion=emotion)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def read(self, emotion_id: int) -> Emotion | None:
        return self.session.query(Emotion).filter(Emotion.id == emotion_id).first()

    def read_all(self, skip: int = 0, limit: int = 100) -> list[Emotion]:
        return self.session.query(Emotion).offset(skip).limit(limit).all()

    def update(self, emotion_id: int, emotion: str = None) -> Emotion | None:
        obj = self.read(emotion_id)
        if not obj:
            return None
        if emotion is not None:
            obj.emotion = emotion
        self.session.commit()
        return obj

    def delete(self, emotion_id: int) -> Emotion | None:
        obj = self.read(emotion_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj
