from sqlalchemy.orm import Session
from src.eng_correct.db_model import TaskGenerationMap, SessionLocal
from src.eng_correct.crud.task import TaskCRUD
from src.eng_correct.crud.generation_prompt import GenerationPromptCRUD

class TaskGenerationMapCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, task_id: int, generation_prompt_id: int) -> TaskGenerationMap:
        mapping = TaskGenerationMap(
            task_id=task_id,
            generation_prompt_id=generation_prompt_id
        )
        self.session.add(mapping)
        self.session.commit()
        self.session.refresh(mapping)
        return mapping

    def read(self, mapping_id: int) -> TaskGenerationMap | None:
        return self.session.query(TaskGenerationMap).filter(TaskGenerationMap.id == mapping_id).first()

    def read_all(self) -> list[TaskGenerationMap]:
        return self.session.query(TaskGenerationMap).all()
    
    def read_by_task_id(self, task_id: int) -> list[TaskGenerationMap]:
        return self.session.query(TaskGenerationMap).filter(
            TaskGenerationMap.task_id == task_id
        ).all()

    def update(self, mapping_id: int, task_id: int = None, generation_prompt_id: int = None) -> TaskGenerationMap | None:
        mapping = self.read(mapping_id)
        if not mapping:
            return None
        if task_id is not None:
            mapping.task_id = task_id
        if generation_prompt_id is not None:
            mapping.generation_prompt_id = generation_prompt_id
        self.session.commit()
        return mapping

    def delete(self, mapping_id: int) -> TaskGenerationMap | None:
        mapping = self.read(mapping_id)
        if mapping:
            self.session.delete(mapping)
            self.session.commit()
        return mapping
    
if __name__ == "__main__":
    session = SessionLocal()

    # 사전 준비
    task = TaskCRUD(session).create("맵핑 테스트", "설명")
    inst = GenerationPromptCRUD(session).create("지시문")

    crud = TaskGenerationMap(session)
    print("TaskGenerationMap CRUD 테스트")

    # Create
    mapping = crud.create(task.id, inst.id)
    print("생성됨:", mapping.id)

    # Read
    read_mapping = crud.read(mapping.id)
    print("조회:", read_mapping.id)

    # Update
    updated = crud.update(mapping.id, generation_prompt_id=inst.id)
    print("수정됨:", updated.id)

    # Delete
    deleted = crud.delete(mapping.id)
    print("삭제 완료:", deleted.id)

    # 정리
    TaskCRUD(session).delete(task.id)
    GenerationPromptCRUD(session).delete(inst.id)