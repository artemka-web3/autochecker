import aiohttp
import asyncio
import aiofiles
import requests
import os

def create_user(username, first_name, last_name, tg_id):
    create_user_req = 'http://127.0.0.1:8000/api/users/create/'
    user_data = {
        'username': str(username),
        'first_name': str(first_name),
        'last_name': str(last_name),
        'tg_id': tg_id,
    }
    try:
        response = requests.post(create_user_req, data=user_data, files={'image': open(f'photos/{username}.png', 'rb')})
        os.system(f'rm photos/{username}.png')
    except FileNotFoundError:
        response = requests.post(create_user_req, data=user_data, files={'image': open(f'photos/none.png', 'rb')})

    print(response.text)
    return response

                
async def get_users():
    api_url = 'http://127.0.0.1:8000/api/users/'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            return await response.json()

async def create_chat_message(user_id, message_id, message_datetime, message_sender, text):
    create_msg_req = 'http://127.0.0.1:8000/api/messages/create/'

    new_message_data = {
        'user': user_id,
        'message_id': message_id,
        'message_text': text,
        'message_datetime': message_datetime,
        'message_sender': message_sender
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(create_msg_req, json=new_message_data) as response:
            print(await response.text())
            return response.status

async def get_messages():
    get_msgs_req = 'http://127.0.0.1:8000/api/messages/'  # ?chat_id=x

    async with aiohttp.ClientSession() as session:
        async with session.get(get_msgs_req) as response:
            return await response.json()