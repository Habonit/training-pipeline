from sqlalchemy.orm import Session
from src.eng_correct.db_model import Task, SessionLocal

class TaskCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, description: str):
        task = Task(name=name, description=description)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def read(self, task_id: int):
        return self.session.query(Task).filter(Task.id == task_id).first()

    def read_all(self) -> list[Task]:
        return self.session.query(Task).all()

    def update(self, task_id: int, name=None, description=None):
        task = self.read(task_id)
        if not task:
            return None
        if name: task.name = name
        if description: task.description = description
        self.session.commit()
        return task

    def delete(self, task_id: int):
        task = self.read(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()
        return task

if __name__ == "__main__":
    session = SessionLocal()
    crud = TaskCRUD(session)

    print("Task CRUD 테스트")

    # Create
    task = crud.create("테스트 태스크", "이건 설명입니다.")
    print("생성됨:", task.id, task.name)

    # Read
    read_task = crud.read(task.id)
    print("조회:", read_task.id, read_task.description)

    # Update
    updated = crud.update(task.id, name="수정된 태스크")
    print("수정됨:", updated.name)

    # Delete
    deleted = crud.delete(task.id)
    print("삭제 완료:", deleted.id)
