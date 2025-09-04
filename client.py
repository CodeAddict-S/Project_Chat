import requests
import websocket
import threading
import json

HTTP_BACKEND = 'http://localhost:8000'
WS_BACKEND = 'ws://localhost:8000/ws'

access_token = ''

def create_chat():
    if not access_token:
        print('You must be logged in')
        return

    name = input("Chat name: ")
    user_id = input("Other user's id: ")
    res = requests.post(HTTP_BACKEND+'/chat/chat/', json={
        "user": user_id,
        "name": name
    }, headers={'Authorization': 'Bearer '+ access_token})
    print(res.text)
    print(res.json())

def login(): 
    username = input("username: ")
    password = input("password: ")

    res = requests.post(HTTP_BACKEND+'/auth/login/', json={
        "username": username,
        "password": password
    })
    global access_token
    print(res.json(), type(res.json()))
    access_token = res.json()['access']
    print(res.json(), end='\n\n')

def signup():
    name = input("Your first name: ")
    last_name = input("Your last name: ")
    username = input("Your username: ")

    password1: str
    password2: str
    while True:
        password1 = input("Your password: ")
        password2 = input("Confirm password: ")
        if password1 != password2:
            print("Passwords don't match")
            continue
        break
    
    res = requests.post(HTTP_BACKEND+'/auth/register/', json={
        "username": username,
        "last_name": last_name,
        "first_name": name,
        "password": password1
    })

    global access_token
    access_token = res.json()['tokens']['access']

    print(res.json(), end='\n\n')

def get_info():
    if not access_token:
        print('You must be logged in')
    res = requests.get(HTTP_BACKEND+'/auth/me/', headers={'Authorization': 'Bearer ' + access_token})
    print(res.json(), end='\n\n')

def enter_chat():
    if not access_token:
        print('You must be logged in')
        return
    chat_name = input('Enter chat name: ')

    def on_error(ws, error): print(error)
    def on_message(ws, message):
        data = json.loads(message)
        print('\n' + data['username'] + ': ' + data['content'])

    ws = websocket.WebSocketApp(WS_BACKEND+'/chat/'+chat_name+'/?token='+access_token,
                                on_message=on_message,
                                on_error=on_error)

    def show_messages():
        ws.run_forever()

    show_messages_thread = threading.Thread(target=show_messages)
    show_messages_thread.start()

    print('type your message and press enter to send one')

    while True:
        message = input()
        ws.send(message)

while True: 

    print(
"""\
Available Actions:
1 - Create chat
2 - Enter chat
3 - Get My Info
4 - Log in
5 - Sign up
"""
    )

    action = int(input("Choose action: "))

    match action:
        case 1:
            create_chat()
        case 2:
            enter_chat()
        case 3 :
            get_info()
        case 4:
            login()
        case 5:
            signup()

