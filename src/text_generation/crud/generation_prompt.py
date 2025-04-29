from sqlalchemy.orm import Session
from src.text_generation.db_model import GenerationPrompt

class GenerationPromptCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, prompt: str) -> GenerationPrompt:
        obj = GenerationPrompt(prompt=prompt)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def read(self, generation_prompt_id: int) -> GenerationPrompt | None:
        return self.session.query(GenerationPrompt).filter(GenerationPrompt.id == generation_prompt_id).first()

    def read_all(self, skip: int = 0, limit: int = 100) -> list[GenerationPrompt]:
        return self.session.query(GenerationPrompt).offset(skip).limit(limit).all()

    def update(self, generation_prompt_id: int, prompt: str = None) -> GenerationPrompt | None:
        obj = self.read(generation_prompt_id)
        if not obj:
            return None
        if prompt is not None:
            obj.prompt = prompt
        self.session.commit()
        return obj

    def delete(self, generation_prompt_id: int) -> GenerationPrompt | None:
        obj = self.read(generation_prompt_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj
