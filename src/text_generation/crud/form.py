from sqlalchemy.orm import Session
from src.text_generation.db_model import Form

class FormCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, form: str, description: str) -> Form:
        obj = Form(form=form, description=description)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def read(self, form_id: int) -> Form | None:
        return self.session.query(Form).filter(Form.id == form_id).first()

    def read_all(self, skip: int = 0, limit: int = 100) -> list[Form]:
        return self.session.query(Form).offset(skip).limit(limit).all()

    def update(self, form_id: int, form: str = None, description: str = None) -> Form | None:
        obj = self.read(form_id)
        if not obj:
            return None
        if form is not None:
            obj.form = form
        if description is not None:
            obj.description = description
        self.session.commit()
        return obj

    def delete(self, form_id: int) -> Form | None:
        obj = self.read(form_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj