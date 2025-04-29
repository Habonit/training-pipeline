from sqlalchemy.orm import Session
from src.text_generation.db_model import MappingSpeakerNumForm

class MappingSpeakerNumFormCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, speaker_num_id: int, form_id: int, attribute: str = None) -> MappingSpeakerNumForm:
        obj = MappingSpeakerNumForm(
            speaker_num_id=speaker_num_id,
            form_id=form_id,
            attribute=attribute
        )
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def read(self, mapping_id: int) -> MappingSpeakerNumForm | None:
        return self.session.query(MappingSpeakerNumForm).filter(MappingSpeakerNumForm.id == mapping_id).first()

    def read_all(self, skip: int = 0, limit: int = 100) -> list[MappingSpeakerNumForm]:
        return self.session.query(MappingSpeakerNumForm).offset(skip).limit(limit).all()

    def update(self, mapping_id: int, speaker_num_id: int = None, form_id: int = None, attribute: str = None) -> MappingSpeakerNumForm | None:
        obj = self.read(mapping_id)
        if not obj:
            return None
        if speaker_num_id is not None:
            obj.speaker_num_id = speaker_num_id
        if form_id is not None:
            obj.form_id = form_id
        if attribute is not None:
            obj.attribute = attribute
        self.session.commit()
        return obj

    def delete(self, mapping_id: int) -> MappingSpeakerNumForm | None:
        obj = self.read(mapping_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj
