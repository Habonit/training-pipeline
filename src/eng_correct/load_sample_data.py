import os
from src.utils.load_json import load_json

from src.eng_correct.crud.task import TaskCRUD
from src.eng_correct.crud.instruction_prompt import InstructionPromptCRUD
from src.eng_correct.crud.system_prompt import SystemPromptCRUD
from src.eng_correct.crud.generation_prompt import GenerationPromptCRUD
from src.eng_correct.crud.task_instruction_map import TaskInstructionMapCRUD
from src.eng_correct.crud.task_generation_map import TaskGenerationMapCRUD

def insert_sample_from_directory(session, sample_dir):
    task_data = load_json(os.path.join(sample_dir, "task.json"))
    instruction_data = load_json(os.path.join(sample_dir, "instruction_prompt.json"))
    system_data = load_json(os.path.join(sample_dir, "system_prompt.json"))
    generation_data = load_json(os.path.join(sample_dir, "generation_prompt.json"))
    instruct_mapping_data = load_json(os.path.join(sample_dir, "task_instruction_map.json"))
    generation_mapping_data = load_json(os.path.join(sample_dir, "task_generation_map.json"))

    task_crud = TaskCRUD(session)
    instruction_crud = InstructionPromptCRUD(session)
    system_crud = SystemPromptCRUD(session)
    generation_crud = GenerationPromptCRUD(session)
    instruct_mapping_crud = TaskInstructionMapCRUD(session)
    generation_mapping_crud = TaskGenerationMapCRUD(session)

    for t in task_data:
        task_crud.create(**t)

    for i in instruction_data:
        instruction_crud.create(**i)

    for s in system_data:
        system_crud.create(**s)
        
    for g in generation_data:
        generation_crud.create(**g)

    for i in instruct_mapping_data:
        instruct_mapping_crud.create(**i)
        
    for g in generation_mapping_data:
        generation_mapping_crud.create(**g)

    print("샘플 데이터 삽입 완료")