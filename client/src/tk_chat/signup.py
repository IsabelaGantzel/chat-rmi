from ..api import Api, USER_ALREADY_EXISTS, USER_NOT_FOUND, INVALID_PASSWORD
from ..tk.tk_signup import TkSignup
from ..tk.tk_alert import tk_alert


def signup(api: Api):
    def on_submit(username, password):
        # TODO: Validar username e password
        if len(password) < 4:
            return tk_alert.showerror("Erro", "A senha deve ter no mínimo 4 caracteres")

        (_, error) = api.signup(username, password)

        if error is None:
            return ui.destroy()

        if error == USER_ALREADY_EXISTS:
            return tk_alert.showerror("Erro", "Usuário já cadastrado")

    ui = TkSignup()
    ui.on_submit = on_submit
    ui.run()
