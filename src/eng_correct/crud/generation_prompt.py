from sqlalchemy.orm import Session
from src.eng_correct.db_model import GenerationPrompt, SessionLocal

class GenerationPromptCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, context_prompt: str, example_prompt: str) -> GenerationPrompt:
        prompt = GenerationPrompt(context_prompt=context_prompt, example_prompt=example_prompt)
        self.session.add(prompt)
        self.session.commit()
        self.session.refresh(prompt)
        return prompt

    def read(self, prompt_id: int) -> GenerationPrompt | None:
        return self.session.query(GenerationPrompt).filter(GenerationPrompt.id == prompt_id).first()

    def read_all(self) -> list[GenerationPrompt]:
        return self.session.query(GenerationPrompt).all()

    def update(self, prompt_id: int, context_prompt: str = None, example_prompt: str = None) -> GenerationPrompt | None:
        prompt = self.read(prompt_id)
        if not prompt:
            return None
        if context_prompt is not None:
            prompt.context_prompt = context_prompt
        if example_prompt is not None:
            prompt.example_prompt = example_prompt
        self.session.commit()
        return prompt

    def delete(self, prompt_id: int) -> GenerationPrompt | None:
        prompt = self.read(prompt_id)
        if prompt:
            self.session.delete(prompt)
            self.session.commit()
        return prompt
    
if __name__ == "__main__":
    session = SessionLocal()
    crud = GenerationPromptCRUD(session)

    print("GenerationPrompt CRUD 테스트")

    # Create
    prompt = crud.create(context_prompt="이 문장은 기발하게 작성해줘." ,example_prompt="이 문장은 정중하게 작성해줘.")
    print("생성됨:", prompt.id, prompt.context_prompt, prompt.example_prompt)

    # Read
    read_prompt = crud.read(prompt.id)
    print("조회:", read_prompt.id, read_prompt.context_prompt, read_prompt.example_prompt)

    # Update
    updated = crud.update(prompt.id, context_prompt="격식을 갖춰줘.", example_prompt="격식을 갖춰줘.")
    print("수정됨:", updated.context_prompt, updated.example_prompt)

    # Delete
    deleted = crud.delete(prompt.id)
    print("삭제 완료:", deleted.id)