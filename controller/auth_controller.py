"""
auth_controller.py
    Yapar:
        master password kontrolu
        ilk giris mi kontrolu
        login ekranindan gelen veriyi validate etme
        basariliysa app_controller’a haber verme

    Kullanir:
        encryption_service
        storage_service
        validators

    Asla:
        UI cizmez
        SQL yazmaz

    """
class AuthController:

    def __init__(self, encryption_service, storage_service, validators):
        self.encryption_service = encryption_service
        self.storage_service = storage_service
        self.validators = validators

    def is_first_run(self) -> bool:
        return not self.storage_service.has_master_key()

    def setup_master_password(self, master_password: str):
        self.validators.validate_master_password(master_password)
        self.encryption_service.create_master_key(master_password)

    def login(self, master_password: str) -> bool:
        if not self.validators.validate_master_password(master_password):
            return False

        return self.encryption_service.verify_master_key(master_password)
