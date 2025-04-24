from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime
from itertools import product
import random
import json

from src.eng_correct.db_model import SessionLocal
from src.eng_correct.crud.train import TrainCRUD
from src.eng_correct.crud.system_prompt import SystemPromptCRUD
from src.eng_correct.crud.instruction_prompt import InstructionPromptCRUD
from src.eng_correct.crud.task import TaskCRUD
from src.eng_correct.crud.generation_prompt import GenerationPromptCRUD
from src.eng_correct.crud.task_instruction_map import TaskInstructionMapCRUD
from src.eng_correct.crud.task_generation_map import TaskGenerationMapCRUD
from src.module.llm.gpt import GPTClient

NUM = int(Variable.get("num", default_var=1))
ITERATIONS = int(Variable.get("iterations", default_var=10))
MODEL_NAME = Variable.get("model", default_var="gpt-4o-mini")
DB = Variable.get("db", default_var="eng_corr")
#["친구 사이의 대화 같은", "냉소적인","서정적인" ,"공손한", "분노에 찬"]
STYLES = json.loads(Variable.get("styles", default_var='["서정적인"]'))

def load_metadata(**kwargs):
    session = SessionLocal()
    task_data = []

    print(f"[Load Metadata]: {DB}에서 task, instruction_id, generation_id 받아오기기")
    for task in TaskCRUD(session).read_all():
        task_id = task.id
        instruction_ids = [x.instruction_prompt_id for x in TaskInstructionMapCRUD(session).read_by_task_id(task_id)]
        generation_ids = [y.generation_prompt_id for y in TaskGenerationMapCRUD(session).read_by_task_id(task_id)]
        task_data.append((task_id, instruction_ids, generation_ids))
        
    kwargs["ti"].xcom_push(key="task_metadata", value=task_data)
    
def create_cruds(**kwargs):
    try:
        session = SessionLocal()
        
        InstructionPromptCRUD(session)
        GenerationPromptCRUD(session)
        TaskInstructionMapCRUD(session)
        TaskGenerationMapCRUD(session)
        TrainCRUD(session)
        kwargs["ti"].xcom_push(key="cruds_ready", value=True)
    except Exception as e:
        print(f"[CRUD 생성 실패] DB 연결 오류 : {e}")
        kwargs["ti"].xcom_push(key="cruds_ready", value=False)
        
def generate_data(**kwargs):
    if not kwargs["ti"].xcom_pull(key="cruds_ready", task_ids="create_cruds"):
        print("[CRUD 생성 실패] 데이터 생성 중단")
        return 
    
    session = SessionLocal()
    
    system_prompt = SystemPromptCRUD(session).read(NUM).system_prompt
    gpt = GPTClient(model=MODEL_NAME, system_prompt=system_prompt)
    
    instruction_crud = InstructionPromptCRUD(session)
    generation_crud = GenerationPromptCRUD(session)
    task_instruction_map_crud = TaskInstructionMapCRUD(session)
    task_generation_map_crud = TaskGenerationMapCRUD(session)
    train_crud = TrainCRUD(session)
    
    task_data = kwargs["ti"].xcom_pull(key="task_metadata", task_ids="load_metadatas")
    
    for task_id, instruction_ids, generation_ids in task_data:
        for _ in range(ITERATIONS):
            for instruction_id, generation_id in product(instruction_ids, generation_ids):
                try:
                    format_dict = {"example":None, "context":None}
                    
                    task_instruction_map_id = task_instruction_map_crud.read_by_task_instruction_id(task_id, instruction_id).id
                    instruction = instruction_crud.read(instruction_id).instruction_prompt
                    generation_prompt = generation_crud.read(generation_id)
                    
                    context_output = gpt.send_hard_temporary_message(generation_prompt.context_prompt)
                    example_output = gpt.send_hard_temporary_message(generation_prompt.example_prompt)
                    
                    format_dict["context"] = context_output
                    format_dict["examples"] = example_output
                    if task_id == 2:
                        style = random.choice(STYLES)
                        format_dict["style"] = style

                    instruction_input = instruction.format(**format_dict)
                    instruction_output = gpt.send_hard_temporary_message(instruction_input)
                    
                    train_crud.create(
                        task_instruction_map_id=task_instruction_map_id,
                        system_prompt_id=NUM,
                        context=context_output,
                        example=example_output,
                        output=instruction_output
                    )
                except Exception as e:
                    print(f"[Data 생성 중 에러 발생] task_id={task_id}, instruction_id={instruction_id}, generation_id={generation_id}, error: {e}")
                    continue                
 
with DAG(
    dag_id=f"{DB}_data_generation_pipeline",
    start_date=datetime(2025,1,1),
    schedule_interval=None,
    catchup=False,
    description=f"{DB}에서 훈련할 데이터 생성",
    tags = [DB, MODEL_NAME, "data_generation"]
) as dag:
    
    t1 = PythonOperator(
        task_id="load_metadatas",
        python_callable=load_metadata,
        provide_context=True
    )
    
    t2 = PythonOperator(
        task_id="create_cruds",
        python_callable=create_cruds,
        provide_context=True
    )

    t3 = PythonOperator(
        task_id="generate_data",
        python_callable=generate_data,
        provide_context=True
    )
    
    t1 >> t2 >> t3

