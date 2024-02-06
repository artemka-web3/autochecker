import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from config import *
from keyboards import *
from save_msg import *
from fsm import *
from api import read_root
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import aiohttp
import os


bot = Bot(token='6891450437:AAHiTvbueexeDiGsurs19ixLGTdwyEQG2oQ')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)