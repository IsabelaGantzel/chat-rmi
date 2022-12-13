from .api import Api, USER_ALREADY_EXISTS, USER_NOT_FOUND, INVALID_PASSWORD
from .tk.signin import TkSignin
from .tk.signup import TkSignup
from .tk.alert import alert
from src.cmd import menu, MENU_OPTION_SIGNIN, MENU_OPTION_SIGNUP


def signin(api: Api):
    def on_submit(username, password):
        result = api.signin(username, password)
        error = result[1]

        if error is None:
            nonlocal user
            user = result[0]
            return ui.destroy()

        if error == USER_NOT_FOUND:
            return alert.showerror("Erro", "Usuário não encontrado!")

        if error == INVALID_PASSWORD:
            return alert.showerror("Erro", "Senha incorreta!")

    user = None
    ui = TkSignin()
    ui.on_submit = on_submit
    ui.run()
    print(user)
    return user


def signup(api: Api):
    def on_submit(username, password):
        (_, error) = api.signup(username, password)

        if error is None:
            return ui.destroy()

        if error == USER_ALREADY_EXISTS:
            return alert.showerror("Erro", "Usuário já cadastrado")

    ui = TkSignup()
    ui.on_submit = on_submit
    ui.run()


def menu_interactive(api: Api):
    while True:
        option = menu()

        if option == MENU_OPTION_SIGNIN:
            result = signin(api)
            if result is not None:
                return result

        if option == MENU_OPTION_SIGNUP:
            signup(api)
