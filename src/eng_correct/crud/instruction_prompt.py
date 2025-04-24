from sqlalchemy.orm import Session
from src.eng_correct.db_model import InstructionPrompt, SessionLocal

class InstructionPromptCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, instruction_prompt: str) -> InstructionPrompt:
        prompt = InstructionPrompt(instruction_prompt=instruction_prompt)
        self.session.add(prompt)
        self.session.commit()
        self.session.refresh(prompt)
        return prompt

    def read(self, prompt_id: int) -> InstructionPrompt | None:
        return self.session.query(InstructionPrompt).filter(InstructionPrompt.id == prompt_id).first()

    def read_all(self) -> list[InstructionPrompt]:
        return self.session.query(InstructionPrompt).all()

    def update(self, prompt_id: int, instruction_prompt: str = None) -> InstructionPrompt | None:
        prompt = self.read(prompt_id)
        if not prompt:
            return None
        if instruction_prompt is not None:
            prompt.instruction_prompt = instruction_prompt
        self.session.commit()
        return prompt

    def delete(self, prompt_id: int) -> InstructionPrompt | None:
        prompt = self.read(prompt_id)
        if prompt:
            self.session.delete(prompt)
            self.session.commit()
        return prompt

if __name__ == "__main__":
    session = SessionLocal()
    crud = InstructionPromptCRUD(session)

    print("InstructionPrompt CRUD 테스트")

    # Create
    prompt = crud.create("문장을 자연스럽게 고쳐줘.")
    print("생성됨:", prompt.id, prompt.instruction_prompt)

    # Read
    read_prompt = crud.read(prompt.id)
    print("조회:", read_prompt.id, read_prompt.instruction_prompt)

    # Update
    updated = crud.update(prompt.id, instruction_prompt="좀 더 포멀하게 고쳐줘.")
    print("수정됨:", updated.instruction_prompt)

    # Delete
    deleted = crud.delete(prompt.id)
    print("삭제 완료:", deleted.id)