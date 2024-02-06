


import requests

# URL вашего API
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
    except FileNotFoundError:
        response = requests.post(create_user_req, data=user_data, files={'image': open(f'photos/none.png', 'rb')})
    print(response.text)
    return response


def get_users():
    api_url = 'http://127.0.0.1:8000/api/users/'
    response = requests.get(api_url)
    return response.json()



# URL for creating a new ChatMessage object
def create_chat_message(user_id, message_id, message_datetime, message_sender, text):
    create_msg_req = 'http://127.0.0.1:8000/api/messages/create/'

    new_message_data = {
        'user': user_id,  
        'message_id': message_id,
        'message_text': text,
        'message_datetime': message_datetime,
        'message_sender': message_sender
    }

    response = requests.post(create_msg_req, json=new_message_data)
    print(response.text)
    return response.status_code



def get_messages():
    get_msgs_req = 'http://127.0.0.1:8000/api/messages/' #?chat_id=x

    get_response = requests.get(get_msgs_req)

    return get_response.json()

# pgit initint(get_users())