from remote_api import remote

new_app = remote()
username = ""

def login():
    global username
    global new_app
    while True:
        input_choose = int(input("Make a  choose\n\n1. Login\n2. Signup\n"))
        if input_choose == 1:
            user = input("Enter username: ")
            pasw = input("Enter password: ")
            if new_app.login(user,pasw):
                username = user
                break
        elif input_choose == 2:
            user = input("Enter username: ")
            pasw = input("Enter password: ")
            if new_app.signup(user,pasw):
                username = user
                break
        print("Error trying to login/signup")

def message():
    global username
    global new_app
    new_app.message(username,"","qdfuasefawesfuwh")
    pass

login()
