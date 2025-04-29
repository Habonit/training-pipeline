from sqlalchemy.orm import Session
from src.text_generation.db_model import Length

class LengthCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, length: int) -> Length:
        obj = Length(length=length)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def read(self, length_id: int) -> Length | None:
        return self.session.query(Length).filter(Length.id == length_id).first()

    def read_all(self, skip: int = 0, limit: int = 100) -> list[Length]:
        return self.session.query(Length).offset(skip).limit(limit).all()

    def update(self, length_id: int, length: int = None) -> Length | None:
        obj = self.read(length_id)
        if not obj:
            return None
        if length is not None:
            obj.length = length
        self.session.commit()
        return obj

    def delete(self, length_id: int) -> Length | None:
        obj = self.read(length_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj
