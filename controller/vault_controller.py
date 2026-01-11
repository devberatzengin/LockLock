"""
vault_controller.py

Asil is burada donecek.

    Yapar:
        sifre ekleme
        sifre silme
        sifre listeleme
        kategoriye gore filtreleme
        search_service’i tetikleme

    Baglantilari:
        models (account, category, vault)
        services (search, encryption, storage)
        ui (dashboard, dialogs)

Bu dosya kalabalik olur, normal. Ama her sey yonetim seviyesinde kalmali.
"""
# Core importu kaldırıldı, doğrudan modellerden alıyoruz
from models.account import Account

class VaultController:

    def __init__(self, storage_service, encryption_service, search_service, logger):
        self.storage = storage_service
        self.encryption = encryption_service
        self.search = search_service
        self.logger = logger
        self.is_locked = True

    def unlock_vault(self):
        self.is_locked = False

    def lock_vault(self):
        self.is_locked = True

    def cleanup(self):
        self.storage.close()

    def add_account(self, site, username, raw_password, category_id):
        if self.is_locked:
            raise PermissionError("Vault is locked")

        encrypted = self.encryption.encrypt(raw_password)

        # Yeni Account modelini kullanıyoruz.
        # Constructor içinde otomatik validate() çağrılıyor.
        account = Account(
            site=site,
            username=username,
            encrypted_password=encrypted,
            category_id=category_id
        )

        account_id = self.storage.save_account(account)
        self.logger.info("ACCOUNT_ADDED", f"id={account_id}")

        return account_id

    def delete_account(self, account_id: int) -> bool:
        if self.is_locked:
            raise PermissionError("Vault is locked")

        success = self.storage.delete_account_by_id(account_id)

        if success:
            self.logger.info("ACCOUNT_DELETED", f"id={account_id}")

        return success

    def list_accounts(self):
        if self.is_locked:
            raise PermissionError("Vault is locked")

        return self.storage.get_all_accounts()

    def list_by_category(self, category_id: int):
        return self.storage.get_accounts_by_category_id(category_id)

    def search_accounts(self, keyword: str):
        # search_service'deki doğru metod ismine dikkat: global_search
        results = self.search.global_search(keyword) 
        self.logger.info("SEARCH", keyword)
        return results

    def change_master_key_and_reencrypt(self, old_key: bytes, new_key: bytes):
        if self.is_locked:
            raise PermissionError("Vault locked")

        try:
            self.logger.security("MASTER_KEY_CHANGE_START", "Re-encryption started")
            self.storage.begin_transaction()

            self.encryption.load_key(old_key)
            accounts = self.storage.get_all_accounts()
            decrypted = []

            for acc in accounts:
                plain = self.encryption.decrypt(acc.encrypted_password)
                decrypted.append((acc.id, plain))

            self.encryption.load_key(new_key)
            for acc_id, plain in decrypted:
                new_encrypted = self.encryption.encrypt(plain)
                self.storage.update_encrypted_password(acc_id, new_encrypted)

            self.storage.update_master_key_hash(new_key.decode() if isinstance(new_key, bytes) else new_key)
            self.storage.commit()
            self.logger.security("MASTER_KEY_CHANGE_SUCCESS", "All passwords re-encrypted")

        except Exception as e:
            self.storage.rollback()
            self.logger.error("MASTER_KEY_CHANGE_FAILED", str(e))
            raise