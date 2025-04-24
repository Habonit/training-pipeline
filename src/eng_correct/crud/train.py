from sqlalchemy.orm import Session
from src.eng_correct.db_model import Train, SessionLocal
from src.eng_correct.crud.task import TaskCRUD
from src.eng_correct.crud.instruction_prompt import InstructionPromptCRUD
from src.eng_correct.crud.task_instruction_map import TaskInstructionMapCRUD
from src.eng_correct.crud.system_prompt import SystemPromptCRUD


class TrainCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        task_instruction_map_id: int,
        system_prompt_id: int | None,
        context: str,
        example: str,
        output: str
    ) -> Train:
        train_data = Train(
            task_instruction_map_id=task_instruction_map_id,
            system_prompt_id=system_prompt_id,
            context=context,
            example=example,
            output=output
        )
        self.session.add(train_data)
        self.session.commit()
        self.session.refresh(train_data)
        return train_data

    def read(self, train_id: int) -> Train | None:
        return self.session.query(Train).filter(Train.id == train_id).first()
    
    def read_all(self) -> list[Train]:
        return self.session.query(Train).all()

    def update(
        self,
        train_id: int,
        context: str = None,
        example: str = None,
        output: str = None,
        system_prompt_id: int = None
    ) -> Train | None:
        train_data = self.read(train_id)
        if not train_data:
            return None
        if context is not None:
            train_data.context = context
        if example is not None:
            train_data.example = example
        if output is not None:
            train_data.output = output
        if system_prompt_id is not None:
            train_data.system_prompt_id = system_prompt_id
        self.session.commit()
        return train_data

    def delete(self, train_id: int) -> Train | None:
        train_data = self.read(train_id)
        if train_data:
            self.session.delete(train_data)
            self.session.commit()
        return train_data

if __name__ == "__main__":
    session = SessionLocal()

    # 사전 준비
    task = TaskCRUD(session).create("TrainData용 Task", "desc")
    inst = InstructionPromptCRUD(session).create("Train용 인스트럭션")
    mapping = TaskInstructionMapCRUD(session).create(task.id, inst.id)
    sys = SystemPromptCRUD(session).create("시스템 톤")

    crud = TrainCRUD(session)
    print("TrainData CRUD 테스트")

    # Create
    train = crud.create(
        task_instruction_map_id=mapping.id,
        system_prompt_id=sys.id,
        context="이 문장을 고쳐줘.",
        example="문제가 뭐디 => 문제가 뭐지지",
        output="고쳐졌습니다."
    )
    print("생성됨:", train.id)

    # Read
    read_train = crud.read(train.id)
    print("조회:", read_train.id, read_train.output)

    # Update
    updated = crud.update(train.id, output="최종 수정 문장")
    print("수정됨:", updated.output)

    # Delete
    deleted = crud.delete(train.id)
    print("삭제 완료:", deleted.id)

    # 정리
    TaskInstructionMapCRUD(session).delete(mapping.id)
    TaskCRUD(session).delete(task.id)
    InstructionPromptCRUD(session).delete(inst.id)
    SystemPromptCRUD(session).delete(sys.id)