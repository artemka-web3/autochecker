import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from config import *
from keyboards import *
from save_msg import *
from fsm import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
from misc.throttling import rate_limit
from api import read_root
import asyncio
import aiohttp
import os
import middlewares


logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
middlewares.setup(dp)


async def download_photo(file_id, username):
    try:
        # Get the file object using the file ID
        photo_file = await bot.get_file(file_id)

        # Get the URL of the photo file
        photo_url = f'https://api.telegram.org/file/bot{API_TOKEN}/{photo_file.file_path}'
        print(photo_url)
        async with aiohttp.ClientSession() as session:
            async with session.get(photo_url) as response:
                if response.status == 200:
                    # Create a directory for downloaded photos if not exists
                    os.makedirs("photos", exist_ok=True)

                    # Save the photo as a PNG file
                    file_path = os.path.join("photos", f"{username}.png")
                    with open(file_path, "wb") as file:
                        file.write(await response.read())

                    return file_path
                else:
                    return None

    except Exception as e:
        print(f"Error: {e}")
        return None

async def get_and_download_profile_photo(user_id):
    try:
        # Get user profile photos
        user = await bot.get_chat(user_id)
        username = user.username
        photos = await bot.get_user_profile_photos(user_id=user_id, limit=1)

        if photos.photos:
            # Get the file ID of the photo
            file_id = photos.photos[0][-1].file_id

            # Download the photo
            downloaded_file_path = await download_photo(file_id, username)
            return downloaded_file_path
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None




"""
CRM
"""
@dp.message_handler(commands=['crm'])
async def get_crm(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer('Your CRM is here 👇', reply_markup=crm())
    else:
        await message.answer('Вы не админ')

@dp.message_handler(lambda message: '/add_admins_' in message.text)
async def add_admins(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        id_admin =  message.text.replace('/add_admins_', '')
        admin = await bot.get_chat(id_admin)
        admin_username = admin.username
        ADMINS.append(id_admin)
        await message.answer(f'New Admin added - @({admin_username})')
    else:
        await message.answer('Вы не админ')
"""
CRM
"""

@rate_limit(limit=10, key='/start')
@dp.message_handler(commands=['start'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await state.reset_state()
    await get_and_download_profile_photo(message.from_user.id)
    create_user(message.from_user.username, message.from_user.first_name, message.from_user.last_name, message.from_user.id)
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(message.from_user.id, message.message_id, msg_date, 'user', '/start')
    msg = """
    Welcome to our exclusive trading community! Here you get access to PRO trading signals tailored for Quotex and Pocket Option platforms. Maximize your profits now - choose your platform:
    """
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(message.from_user.id, message.message_id, msg_date, 'bot', msg)
    await message.answer(msg, reply_markup=chain_1())


@rate_limit(limit=10, key='pocket')
@dp.callback_query_handler(lambda callback: callback.data == 'pocket')
async def chain_2_pocket(callback: types.CallbackQuery):
    await callback.answer()
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    print("IDDIDIID ", callback.from_user.id)
    await create_chat_message(user_id=callback.from_user.id, message_id=callback.id, message_datetime=msg_date, message_sender='user', text='Pocket Option')

    msg = """
    The usual price for access to our channel and signals is $300 per month. 

    However, we currently have a special new user offer:

    🔥 New User Promo 🔥

    You can get access to our exclusive channel and trading signals completely FREE.

    Here's what you need to do:

    1. Register a new broker account via our link
    2. Make a minimum deposit of $50

    And we'll grant you access to our premium channel with real-time signals from expert traders.

    Be sure to take advantage of this limited-time offer before it ends!    
    """
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg, reply_markup=chain_2_pocket_kb())

@rate_limit(limit=10, key='free_acces_pocket')
@dp.callback_query_handler(lambda callback: callback.data == 'free_acces_pocket')
async def chain_3_pocket_free(callback: types.CallbackQuery):
    await callback.answer() 
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'Get Free Access')
    msg = """
    Great, you've chosen Pocket Option! To access our exclusive Pocket Option signals channel, you need an account registered via our link. Do you already have a Pocket Option account?
    """
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg, reply_markup=chain_3_pocket_check_for_acc())

@rate_limit(limit=10, key='sub_pocket')
@dp.callback_query_handler(lambda callback: callback.data == 'sub_pocket')
async def chain_3_pocket_free(callback: types.CallbackQuery):
    await callback.answer()
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'Purchase Subscription')
    msg = """Fantastic, you've selected the Premium Monthly Subscription! 🎉 This is the best way to get instant access to all of our exclusive Pocket Option trading signals.
Please wait just a moment while we connect you with a membership manager to complete your purchase. This should only take a few minutes.

We appreciate your interest in our premium service - the manager will contact you ASAP to get your subscription activated right away!"""
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg)
    # send to nicky
    for admin in ADMINS:
        await bot.send_message(admin, f"англ платно\nUser @{callback.from_user.username} - {callback.from_user.id} wants Premium Monthly Subscription!")

@rate_limit(limit=10, key='no_pocket')
@dp.callback_query_handler(lambda callback: callback.data == 'no_pocket', state="*")
async def chain_4_pocket_no_acc(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'No, I need to create a Pocket Option account')
    msg = """No worries, we've got you covered! 
    After registering, please send us your trading account ID.
    """
    registration_link_pocket_kb = types.InlineKeyboardMarkup()
    registration_link_pocket_kb.add(types.InlineKeyboardButton(text="Registration Link", url='https://pocket.click/register?utm_source=affiliate&a=CKmh6gq01Lo9Ff&ac=fond'))
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg, reply_markup=registration_link_pocket_kb)
    await asyncio.sleep(1)
    msg = """ID Located in the profile section.
    This is a set of numbers. Usually starts at 6
    Send id without spaces or letters. Only numbers
    """
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await state.set_state(GetIdPocket.getting_id)
    await callback.message.answer(msg)


@rate_limit(limit=10, key='have_pocket')
@dp.callback_query_handler(lambda callback: callback.data == 'have_pocket', state="*")
async def chain_4_pocket_have_acc(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'Yes, I have a Pocket Option account')
    msg = """Awesome! Please send us your trading account ID. We'll verify with the account manager to ensure your account is linked to our partnership program. If you have any questions, we're always here to assist you! 🙏
    """
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg)
    await asyncio.sleep(1)
    msg = """ID Located in the profile section.

    This is a set of numbers. Usually starts at 6

    Send id without spaces or letters. Only numbers
    """
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await state.set_state(GetIdPocket.getting_id)
    await callback.message.answer(msg)

@dp.message_handler(state=GetIdPocket.getting_id)
@rate_limit(limit=10, key='chain_5_check_id_pocket')
async def chain_5_check_id_pocket(message: types.Message, state: FSMContext):
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(message.from_user.id, message.message_id, msg_date, 'user', message.text)
    result = await read_root('AffiliatePocketBot', message.text)

    
    if result == {'result': 'not_found'}:
        
        msg = """The account manager has informed us that this ID is not registered via our affiliate link.

To gain access to the Private Club, you need to register an account using our affiliate link.

Do you agree to this condition?"""
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(types.InlineKeyboardButton('yes', callback_data='yes_not_found_pocket'))
        kb.add(types.InlineKeyboardButton('no', callback_data='no_not_found_pocket'))

        msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        await create_chat_message(message.from_user.id, message.message_id, msg_date, 'bot', msg)
        await message.answer(msg, reply_markup=kb)
        await state.reset_state()
    elif result == {'result': 'less'}:
        msg = """
Congratulations. You have registered via our link.

The account manager has informed us that your account balance is currently less than $30.

To join our team, your account balance needs to be at least $30.

Please click the button below once you have deposited funds to reach the $30 minimum balance."""
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(types.InlineKeyboardButton('Balance Funded', callback_data=f'balance_5_pocket_{message.text}'))
        msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        await create_chat_message(message.from_user.id, message.message_id, msg_date, 'bot', msg)
        await message.answer(msg, reply_markup=kb)
        await state.reset_state()

    elif result == {'result': 'more'}:
        msg = """Thank you for your trust. Please stand by as our manager will soon grant you access to the Private Club."""
        await state.reset_state()
        msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        await create_chat_message(message.from_user.id, message.message_id, msg_date, 'bot', msg)
        for admin in ADMINS:
            await bot.send_message(admin, f'Надо проверить и добавить в группу\nUser @{message.from_user.username} - {message.from_user.id}') 
    elif result == {'result': 'error'}:
        msg = """Input ID correctly please (use numbers only)"""
        msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        await create_chat_message(message.from_user.id, message.message_id, msg_date, 'bot', msg)
        await message.answer(msg)

@rate_limit(limit=10, key='yes_not_found_pocket')
@dp.callback_query_handler(lambda callback: callback.data == 'yes_not_found_pocket')
async def agree_and_reg_pocket(callback:types.CallbackQuery):
    await callback.answer()
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'Yes')
    msg = """Here is the registration link 👇

After registering, please send us the ID of your trading account.

We are here to help guide you through every step! 😊"""
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Registration Link', url='https://pocket.click/register?utm_source=affiliate&a=CKmh6gq01Lo9Ff&ac=fond'))
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg, reply_markup=kb)

@rate_limit(limit=10, key='no_not_found_pocket')
@dp.callback_query_handler(lambda callback: callback.data == 'no_not_found_pocket')
async def answer_not_agree_pocket(callback: types.CallbackQuery):
    await callback.answer()
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'no')
    msg = """
We understand your position. However, registering via our affiliate link is truly important to get full support from our team when working with this broker.

Let's discuss any concerns you may have about registering - perhaps we can find a solution together.

We also recommend subscribing to our channel with free test signals, so you can already start getting familiar with our community."""
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Our Signals Channel', url="https://pocket.click/register?utm_source=affiliate&a=CKmh6gq01Lo9Ff&ac=fond"))
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg, reply_markup=kb)



@rate_limit(limit=10, key='check_balance_pocket')
@dp.callback_query_handler(lambda callback: callback.data.startswith('balance_5_pocket'))
async def check_balance_pocket(callback: types.CallbackQuery):
    await callback.answer()
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'Balance Funded')
    id = callback.data.replace('balance_5_pocket_', '')
    res = await read_root('AffiliatePocketBot', id)
    if res == {'result': 'less'}:
        msg = """The account manager has informed us that your account balance is currently less than $30.

If you have just made a deposit, it's possible the funds have not hit your trading account yet. It may take some time to process.

Once the money arrives in your account, please click the button below:"""
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text="Funds Received in Account", callback_data=f"balance_5_pocket_{id}"))
        msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
        await callback.message.answer(msg, reply_markup=kb)
    elif res == {'result': 'more'}:
        msg = """Thank you for your trust. Please stand by as our manager will soon grant you access to the Private Club."""
        msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
        for admin in ADMINS:
            await bot.send_message(admin, f'Надо проверить и добавить в группу\nUser @{callback.from_user.username} - {callback.from_user.id}')
    


































"""QOTEXTQOTEXTQOTEXTQOTEXTQOTEXTQOTEXTQOTEXTQOTEXTQOTEXTQOTEXTQOTEXTQOTEXT"""







































@rate_limit(limit=10, key='quotex')
@dp.callback_query_handler(lambda callback: callback.data == 'quotex')
async def chain_2_quotex(callback: types.CallbackQuery):
    await callback.answer()
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'Quotex')

    msg = """The usual price for access to our channel and signals is $300 per month. 

However, we currently have a special new user offer:

🔥 New User Promo 🔥

You can get access to our exclusive channel and trading signals completely FREE.

Here's what you need to do:

1. Register a new broker account via our link
2. Make a minimum deposit of $50

And we'll grant you access to our premium channel with real-time signals from expert traders.

Be sure to take advantage of this limited-time offer before it ends!"""
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg, reply_markup=chain_2_quotex_kb())

@rate_limit(limit=10, key='free_acces_quotex')
@dp.callback_query_handler(lambda callback: callback.data == 'free_acces_quotex')
async def chain_3_quotex_free(callback: types.CallbackQuery):
    await callback.answer() 
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'Get Free Access')
    msg = """
    Great, you've chosen Quotex! To access our exclusive Pocket Option signals channel, you need an account registered via our link. Do you already have a Quotex account?
    """
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg, reply_markup=chain_3_quotex_check_for_acc())

@rate_limit(limit=10, key='sub_quotex')
@dp.callback_query_handler(lambda callback: callback.data == 'sub_quotex')
async def chain_3_quotex_free(callback: types.CallbackQuery):
    await callback.answer()
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'Purchase Subscription')
    msg = """Fantastic, you've selected the Premium Monthly Subscription! 🎉 This is the best way to get instant access to all of our exclusive Quotex trading signals.
Please wait just a moment while we connect you with a membership manager to complete your purchase. This should only take a few minutes.

We appreciate your interest in our premium service - the manager will contact you ASAP to get your subscription activated right away!"""
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg)
    # send to nicky
    for admin in ADMINS:
        await bot.send_message(admin, f"англ платно\nUser @{callback.from_user.username} - {callback.from_user.id} wants Premium Monthly Subscription!")


@rate_limit(limit=10, key='no_quotex')
@dp.callback_query_handler(lambda callback: callback.data == 'no_quotex', state='*')
async def chain_4_quotex_no_acc(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'No, I need to create a Quotex account')
    msg = """No worries, we've got you covered! 
    After registering, please send us your trading account ID.
    """
    registration_link_quotex_kb = types.InlineKeyboardMarkup()
    registration_link_quotex_kb.add(types.InlineKeyboardButton(text="Registration Link", url='https://broker-qx.pro/sign-up/?lid=452677'))
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg, reply_markup=registration_link_quotex_kb)
    await asyncio.sleep(1)
    msg = """ID Located in the profile section.
    This is a set of numbers. Usually starts at 6
    Send id without spaces or letters. Only numbers
    """
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await set.state
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg)

@rate_limit(limit=10, key='have_quotex')
@dp.callback_query_handler(lambda callback: callback.data == 'have_quotex', state="*")
async def chain_4_quotex_have_acc(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'Yes, I have a Quotex account')
    msg = """Awesome! Please send us your trading account ID. We'll verify with the account manager to ensure your account is linked to our partnership program. If you have any questions, we're always here to assist you! 🙏
    """
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg)
    await asyncio.sleep(1)
    msg = """ID Located in the profile section.

    This is a set of numbers. Usually starts at 6

    Send id without spaces or letters. Only numbers
    """
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await state.set_state(GetIdQuotex.getting_id)
    await callback.message.answer(msg)


@rate_limit(limit=10, key='chain_5_check_id_quotex')
@dp.message_handler(state=GetIdQuotex.getting_id)
async def chain_5_check_id_quotex(message: types.Message, state: FSMContext):
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(message.from_user.id, message.message_id, msg_date, 'user', message.text)
    result = await read_root('QuotexPartnerBot', message.text)

    
    if result == {'result': 'not_found'}:
        
        msg = """The account manager has informed us that this ID is not registered via our affiliate link.

To gain access to the Private Club, you need to register an account using our affiliate link.

Do you agree to this condition?"""
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(types.InlineKeyboardButton('yes', callback_data='yes_not_found_quotex'))
        kb.add(types.InlineKeyboardButton('no', callback_data='no_not_found_quotex'))

        msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        await create_chat_message(message.from_user.id, message.message_id, msg_date, 'bot', msg)
        await message.answer(msg, reply_markup=kb)
        await state.reset_state()
    elif result == {'result': 'less'}:
        msg = """
Congratulations. You have registered via our link.

The account manager has informed us that your account balance is currently less than $30.

To join our team, your account balance needs to be at least $30.

Please click the button below once you have deposited funds to reach the $30 minimum balance."""
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(types.InlineKeyboardButton('Balance Funded', callback_data=f'balance_5_quotex_{message.text}'))
        msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        await create_chat_message(message.from_user.id, message.message_id, msg_date, 'bot', msg)
        await message.answer(msg, reply_markup=kb)
        await state.reset_state()

    elif result == {'result': 'more'}:
        msg = """Thank you for your trust. Please stand by as our manager will soon grant you access to the Private Club."""
        await state.reset_state()
        msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        await create_chat_message(message.from_user.id, message.message_id, msg_date, 'bot', msg)
        for admin in ADMINS:
            await bot.send_message(admin, f'Надо проверить и добавить в группу\nUser @{message.from_user.username} - {message.from_user.id}') 
    elif result == {'result': 'error'}:
        msg = """Input ID correctly please (use numbers only)"""
        msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        await create_chat_message(message.from_user.id, message.message_id, msg_date, 'bot', msg)
        await message.answer(msg)


@rate_limit(limit=10, key='yes_not_found_quotex')
@dp.callback_query_handler(lambda callback: callback.data == 'yes_not_found_quotex')
async def agree_and_reg_quotex(callback:types.CallbackQuery):
    await callback.answer()
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'Yes')
    msg = """Here is the registration link 👇

After registering, please send us the ID of your trading account.

We are here to help guide you through every step! 😊"""
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Registration Link', url='https://broker-qx.pro/sign-up/?lid=452677'))
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg, reply_markup=kb)

@rate_limit(limit=10, key='no_not_found_quotex')
@dp.callback_query_handler(lambda callback: callback.data == 'no_not_found_quotex')
async def answer_not_agree_quotex(callback: types.CallbackQuery):
    await callback.answer()
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'no')
    msg = """
We understand your position. However, registering via our affiliate link is truly important to get full support from our team when working with this broker.

Let's discuss any concerns you may have about registering - perhaps we can find a solution together.

We also recommend subscribing to our channel with free test signals, so you can already start getting familiar with our community."""
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Our Signals Channel', url="https://t.me/quotex_pocketoption_iqoption_sig"))
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
    await callback.message.answer(msg, reply_markup=kb)

@rate_limit(limit=10, key='check_balance_quotex')
@dp.callback_query_handler(lambda callback: callback.data.startswith('balance_5_quotex'))
async def check_balance_quotex(callback: types.CallbackQuery):
    await callback.answer()
    msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    await create_chat_message(callback.from_user.id, callback.id, msg_date, 'user', 'Balance Funded')
    id = callback.data.replace('balance_5_quotex_', '')
    res = await read_root('QuotexPartnerBot', id)
    if res == {'result': 'less'}:
        msg = """The account manager has informed us that your account balance is currently less than $30.

If you have just made a deposit, it's possible the funds have not hit your trading account yet. It may take some time to process.

Once the money arrives in your account, please click the button below:"""
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text="Funds Received in Account", callback_data=f"balance_5_quotex_{id}"))
        msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
        await callback.message.answer(msg, reply_markup=kb)
    elif res == {'result': 'more'}:
        msg = """Thank you for your trust. Please stand by as our manager will soon grant you access to the Private Club."""
        msg_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        await create_chat_message(callback.from_user.id, callback.id, msg_date, 'bot', msg)
        for admin in ADMINS:
            await bot.send_message(admin, f'Надо проверить и добавить в группу\nUser @{callback.from_user.username} - {callback.from_user.id}')
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)