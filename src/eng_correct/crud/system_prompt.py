from sqlalchemy.orm import Session
from src.eng_correct.db_model import SystemPrompt, SessionLocal

class SystemPromptCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, system_prompt: str) -> SystemPrompt:
        prompt = SystemPrompt(system_prompt=system_prompt)
        self.session.add(prompt)
        self.session.commit()
        self.session.refresh(prompt)
        return prompt

    def read(self, prompt_id: int) -> SystemPrompt | None:
        return self.session.query(SystemPrompt).filter(SystemPrompt.id == prompt_id).first()

    def read_all(self) -> list[SystemPrompt]:
        return self.session.query(SystemPrompt).all()

    def update(self, prompt_id: int, system_prompt: str = None) -> SystemPrompt | None:
        prompt = self.read(prompt_id)
        if not prompt:
            return None
        if system_prompt is not None:
            prompt.system_prompt = system_prompt
        self.session.commit()
        return prompt

    def delete(self, prompt_id: int) -> SystemPrompt | None:
        prompt = self.read(prompt_id)
        if prompt:
            self.session.delete(prompt)
            self.session.commit()
        return prompt
    
if __name__ == "__main__":
    session = SessionLocal()
    crud = SystemPromptCRUD(session)

    print("SystemPrompt CRUD 테스트")

    # Create
    prompt = crud.create("이 문장은 정중하게 작성해줘.")
    print("생성됨:", prompt.id, prompt.system_prompt)

    # Read
    read_prompt = crud.read(prompt.id)
    print("조회:", read_prompt.id, read_prompt.system_prompt)

    # Update
    updated = crud.update(prompt.id, system_prompt="격식을 갖춰줘.")
    print("수정됨:", updated.system_prompt)

    # Delete
    deleted = crud.delete(prompt.id)
    print("삭제 완료:", deleted.id)