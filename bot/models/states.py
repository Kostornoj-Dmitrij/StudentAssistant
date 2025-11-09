from aiogram.fsm.state import StatesGroup, State

class QuestionStates(StatesGroup):
    waiting_question = State()

class ProjectStates(StatesGroup):
    choosing_methodology = State()
    waiting_project_type = State()