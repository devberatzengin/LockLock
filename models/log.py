import datetime

class Log:
    def __init__(
        self,
        id: int | None,
        level: str,
        action: str,
        message: str,
        created_at: datetime.datetime | None = None
    ):
        self.id = id
        self.level = level          
        self.action = action        
        self.message = message
        self.created_at = created_at or datetime.datetime.now()

    def validate(self):
        if self.level not in ("INFO", "ERROR", "WARNING", "SECURITY"):
            raise ValueError("Geçersiz log seviyesi.")
        if not self.action:
            raise ValueError("Log action boş olamaz.")

    @staticmethod
    def from_row(row) -> "Log":
        return Log(
            id=row[0],
            action=row[1],
            message=row[2],
            level=row[3],
            created_at=datetime.datetime.fromisoformat(row[4])
        )

    def to_db_params(self) -> tuple:
        return (
            self.action,
            self.message,
            self.level,
            self.created_at.isoformat()
        )