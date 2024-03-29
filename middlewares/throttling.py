
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


# class ThrottlingMiddleware(BaseMiddleware):
#     """
#     Simple middleware
#     """

#     def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
#         self.rate_limit = limit
#         self.prefix = key_prefix
#         super(ThrottlingMiddleware, self).__init__()

    # async def on_process_message(self, message: types.Message, data: dict):
    #     """
    #     This handler is called when dispatcher receives a message

    #     :param message:
    #     """
    #     # Get current handler
    #     handler = current_handler.get()

    #     # Get dispatcher from context
    #     dispatcher = Dispatcher.get_current()
    #     # If handler was configured, get rate limit and key from handler
    #     if handler:
    #         limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
    #         key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
    #     else:
    #         limit = self.rate_limit
    #         key = f"{self.prefix}_message"

    #     # Use Dispatcher.throttle method.
    #     try:
    #         await dispatcher.throttle(key, rate=limit)
    #     except Throttled as t:
    #         # Execute action
    #         await self.message_throttled(message, t)

    #         # Cancel current handler
    #         raise CancelHandler()
        
    # async def on_process_message(self, message: types.Message, data: dict):
    #     await self.check_throttling(message)

    # async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
    #     await self.check_throttling(callback_query)

    # async def check_throttling(self, obj):
    #     handler = current_handler.get()
    #     dispatcher = Dispatcher.get_current()

    #     if handler:
    #         limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
    #         key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
    #     else:
    #         limit = self.rate_limit
    #         key = f"{self.prefix}_common"

    #     try:
    #         await dispatcher.throttle(key, rate=limit)
    #     except Throttled as t:
    #         await self.throttled(obj, t)
    #         raise CancelHandler()

    # async def message_throttled(self, message: types.Message, throttled: Throttled):
    #     """
    #     Notify user only on first exceed and notify about unlocking only on last exceed

    #     :param message:
    #     :param throttled:
    #     """
    #     handler = current_handler.get()
    #     dispatcher = Dispatcher.get_current()
    #     if handler:
    #         key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
    #     else:
    #         key = f"{self.prefix}_message"

    #     # Calculate how many time is left till the block ends
    #     delta = throttled.rate - throttled.delta

    #     # Prevent flooding
    #     if throttled.exceeded_count <= 2:
    #         await message.reply('Too many requests! ')

    #     # Sleep.
    #     await asyncio.sleep(delta)

    #     # Check lock status
    #     thr = await dispatcher.check_key(key)

    #     # If current message is not last with current key - do not send message
    #     if thr.exceeded_count == throttled.exceeded_count:
    #         await message.reply('Unlocked.')

    # async def callback_query_throttled(self, callback_query: types.CallbackQuery, throttled: Throttled):
    #         handler = current_handler.get()
    #         dispatcher = Dispatcher.get_current()

    #         if handler:
    #             key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
    #         else:
    #             key = f"{self.prefix}_callback_query"

    #         delta = throttled.rate - throttled.delta

    #         if throttled.exceeded_count <= 2:
    #             await callback_query.message.reply("Too many requests!")

    #         await asyncio.sleep(delta)

    #         thr = await dispatcher.check_key(key)

    #         if thr.exceeded_count == throttled.exceeded_count:
    #             await callback_query.message.reply("Unlocked.")

class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        await self.check_throttling(message)

    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        await self.check_throttling(callback_query)

    async def check_throttling(self, obj):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()

        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_common"

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.throttled(obj, t)
            raise CancelHandler()

    async def throttled(self, obj, throttled: Throttled):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        # Calculate how much time is left till the block ends
        delta = throttled.rate - throttled.delta

        # Prevent flooding
        if throttled.exceeded_count <= 2:
            if isinstance(obj, types.Message):
                await obj.reply('Too many requests! ')
            elif isinstance(obj, types.CallbackQuery):
                await obj.message.reply('Too many requests! ')

        # Sleep.
        await asyncio.sleep(delta)

        # Check lock status
        thr = await dispatcher.check_key(key)

        # If current message is not the last with the current key - do not send a message
        if thr.exceeded_count == throttled.exceeded_count:
            if isinstance(obj, types.Message):
                await obj.reply('Wait 30 seconds. And then call /start')
            elif isinstance(obj, types.CallbackQuery):
                await obj.message.reply('Wait 30 seconds. And then call /start')