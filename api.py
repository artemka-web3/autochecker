from typing import Union
import pyrogram
from fastapi import FastAPI
from settings import *
import asyncio


client = pyrogram.Client('bot06', api_id, api_hash)
client_pocket = pyrogram.Client('bot_pocket', api_id_pocket, api_hash_pocket)


async def read_root(username:str, id: str):
    await client.start()
    if not id.isnumeric():
        return {'result': 'error'}
    await client.send_message(username, id.strip())
    await asyncio.sleep(3)
    result = ''
    async for i in client.get_chat_history(username, limit=2):

        print(i.text)
        if i.from_user.username == username:
            result = i.text
    if 'not found' in result.lower():
        print('dksfjdskjfckj')
        await client.stop()
        return {"result": 'not_found'}
    else:
        result = result.splitlines()
        for i in result:
            if 'Balance' in i:
                result = i.strip().split(': ')[-1]
        if '$' in result:
            result = result.split(' ')[-1].replace(',', ' ').strip()
            if float(result) >= 25:
                await client.stop()
                return {"result": 'more'} 
            else:
                await client.stop()
                return {"result": 'less'} 
        elif '₽' in result:
            result = result.split(' ')[-1].replace(',', ' ').strip()
            if float(result) >= 2200:
                await client.stop()
                return {"result": 'more'} 
            else:
                await client.stop()
                return {"result": 'less'} 
        elif '₸' in result:
            result = result.split(' ')[-1].replace(',', ' ').strip()
            if float(result) >= 11150:
                await client.stop()
                return {"result": 'more'} 
            else:
                await client.stop()
                return {"result": 'less'} 
        elif '₴' in result:
            result = result.split(' ')[-1].replace(',', ' ').strip()
            if float(result) >= 950:
                await client.stop()
                return {"result": 'more'} 
            else:
                await client.stop()
                return {"result": 'less'} 
        elif 'Rp' in result:
            result = result.split(' ')[-1].replace(',', ' ').strip()
            if float(result) >= 80:
                await client.stop()
                return {"result": 'more'} 
            else:
                await client.stop()
                return {"result": 'less'} 
        else: 
            try:
                result = float(result.replace(',', ' ').strip())
                if result >= 25:
                    await client.stop()
                    return {"result": 'more'} 
                else:
                    await client.stop()
                    return {"result": 'less'} 
            except:
                await client.stop()
                return {"result": ''}
#uvicorn main:app --reload
            

async def read_root_pocket(username:str, id: str):
    await client_pocket.start()
    if not id.isnumeric():
        return {'result': 'error'}
    await client_pocket.send_message(username, id.strip())
    await asyncio.sleep(3)
    result = ''
    async for i in client_pocket.get_chat_history(username, limit=2):

        print(i.text)
        if i.from_user.username == username:
            result = i.text
    if 'not found' in result.lower():
        print('dksfjdskjfckj')
        await client_pocket.stop()
        return {"result": 'not_found'}
    else:
        result = result.splitlines()
        for i in result:
            if 'Balance' in i:
                result = i.strip().split(': ')[-1]
        if '$' in result:
            result = result.split(' ')[-1].replace(',', ' ').strip()
            if float(result) >= 25:
                await client_pocket.stop()
                return {"result": 'more'} 
            else:
                await client_pocket.stop()
                return {"result": 'less'} 
        elif '₽' in result:
            result = result.split(' ')[-1].replace(',', ' ').strip()
            if float(result) >= 2200:
                await client_pocket.stop()
                return {"result": 'more'} 
            else:
                await client_pocket.stop()
                return {"result": 'less'} 
        elif '₸' in result:
            result = result.split(' ')[-1].replace(',', ' ').strip()
            if float(result) >= 11150:
                await client_pocket.stop()
                return {"result": 'more'} 
            else:
                await client_pocket.stop()
                return {"result": 'less'} 
        elif '₴' in result:
            result = result.split(' ')[-1].replace(',', ' ').strip()
            if float(result) >= 950:
                await client_pocket.stop()
                return {"result": 'more'} 
            else:
                await client_pocket.stop()
                return {"result": 'less'} 
        elif 'Rp' in result:
            result = result.split(' ')[-1].replace(',', ' ').strip()
            if float(result) >= 80:
                await client_pocket.stop()
                return {"result": 'more'} 
            else:
                await client_pocket.stop()
                return {"result": 'less'} 
        else: 
            try:
                result = float(result.replace(',', ' ').strip())
                if result >= 25:
                    await client_pocket.stop()
                    return {"result": 'more'} 
                else:
                    await client_pocket.stop()
                    return {"result": 'less'} 
            except:
                await client_pocket.stop()
                return {"result": ''}
