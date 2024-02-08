from aiogram.dispatcher.filters.state import State, StatesGroup
from fsm import *

class GetIdPocket(StatesGroup):
    getting_id = State()

class GetIdQuotex(StatesGroup):
    getting_id = State()

class PassCaptcha(StatesGroup):
    make_captcha = State()
    get_input = State()