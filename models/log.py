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
        self.level = level          # INFO, ERROR
        self.action = action        # CREATE_ACCOUNT, UPDATE_ACCOUNT vs.
        self.message = message
        self.created_at = created_at or datetime.datetime.now()

    def validate(self):
        if self.level not in ("INFO", "ERROR"):
            raise ValueError("Log level must be INFO or ERROR")

        if not self.action:
            raise ValueError("Log action cannot be empty")

        if not self.message:
            raise ValueError("Log message cannot be empty")

    @staticmethod
    def from_row(row) -> "Log":
        return Log(
            id=row["id"],
            level=row["level"],
            action=row["action"],
            message=row["message"],
            created_at=datetime.datetime.fromisoformat(row["created_at"])
        )

    def to_db_params(self) -> tuple:
        """
        INSERT icin hazir parametreler
        """
        return (
            self.level,
            self.action,
            self.message,
            self.created_at.isoformat()
        )
