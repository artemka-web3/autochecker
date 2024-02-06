from aiogram.dispatcher.filters.state import State, StatesGroup
from fsm import *

class GetId(StatesGroup):
    getting_id = State()