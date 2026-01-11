"""
    Icermeli:
        site
        username
        encrypted_password
        category_id
        timestamps

    Yapar:
        kendini validate edebilir
        serialize / deserialize

    Yapmaz:
        SQL baglantisi
        encryption

    """

from datetime import datetime

class Account:
    def __init__(
        self,
        site: str,
        username: str,
        encrypted_password: str,
        category_id: int,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        account_id: int | None = None
    ):
        self.id = account_id
        self.site = site
        self.username = username
        self.encrypted_password = encrypted_password
        self.category_id = category_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.validate()

    def validate(self):
        if not self.site or not self.site.strip():
            raise ValueError("Site adı boş olamaz.")
        if not self.username or not self.username.strip():
            raise ValueError("Kullanıcı adı boş olamaz.")
        if not self.encrypted_password:
            raise ValueError("Şifrelenmiş veri eksik.")
        if not isinstance(self.category_id, int):
            raise ValueError("Kategori ID bir sayı olmalıdır.")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "site": self.site,
            "username": self.username,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_row(cls, row):
        # row[5] ve row[6] string gelebilir, kontrol edip datetime'a çeviriyoruz
        created = datetime.fromisoformat(row[5]) if isinstance(row[5], str) else row[5]
        updated = datetime.fromisoformat(row[6]) if isinstance(row[6], str) else row[6]

        return cls(
            account_id=row[0],  # __init__ parametresiyle eşleşti
            site=row[1],
            username=row[2],
            encrypted_password=row[3],
            category_id=row[4],
            created_at=created,
            updated_at=updated
        )

    # StorageService'in kayıt için ihtiyaç duyduğu metod
    def to_db_params(self) -> tuple:
        return (
            self.site,
            self.username,
            self.encrypted_password,
            self.category_id,
            self.created_at.isoformat(),
            self.updated_at.isoformat()
        )