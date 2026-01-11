"""
app_controller.py

Sorumluluklari:
    login -> dashboard gecisi
    global state (aktif user, vault unlocked mi)
    uygulama kapanirken cleanup

Bilmesi gerekenler:
    auth_controller
    vault_controller
    ui ekranlari

Bilmemesi gerekenler:
    sifre nasil sifreleniyor
    SQL nasil calisiyor
    """

class AppController:

    def __init__(self, auth_controller, vault_controller):
        self.auth_controller = auth_controller
        self.vault_controller = vault_controller

        self.current_user = None
        self.vault_unlocked = False

    # ---- AUTH FLOW ----
    def start_app(self):
        if self.auth_controller.is_first_run():
            return "SET_MASTER_PASSWORD"
        return "LOGIN"

    def login(self, master_password: str) -> bool:
        success = self.auth_controller.login(master_password)

        if success:
            self.vault_unlocked = True
            return True

        return False

    def logout(self):
        self.current_user = None
        self.vault_unlocked = False
        self.vault_controller.lock_vault()

    # ---- APP LIFECYCLE ----
    def shutdown(self):
        self.vault_controller.cleanup()
