from ..api import Api, USER_NOT_FOUND, INVALID_PASSWORD
from ..tk.tk_signin import TkSignin
from ..tk.tk_alert import tk_alert


def signin(api: Api):
    def on_submit(username, password):
        result = api.signin(username, password)
        error = result[1]

        if error is None:
            nonlocal user
            user = result[0]
            return ui.destroy()

        if error == USER_NOT_FOUND:
            return tk_alert.showerror("Erro", "Usuário não encontrado!")

        if error == INVALID_PASSWORD:
            return tk_alert.showerror("Erro", "Senha incorreta!")

    user = None
    ui = TkSignin()
    ui.on_submit = on_submit
    ui.run()
    return user
