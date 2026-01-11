from models.log import Log

class LogService:

    def __init__(self, storage_service):
        self.storage = storage_service

    def info(self, action: str, detail: str = ""):
        self._write(Log(action, detail, "INFO"))

    def warning(self, action: str, detail: str = ""):
        self._write(Log(action, detail, "WARNING"))

    def error(self, action: str, detail: str = ""):
        self._write(Log(action, detail, "ERROR"))

    def security(self, action: str, detail: str = ""):
        self._write(Log(action, detail, "SECURITY"))

    def _write(self, log: Log):
        query = """
        INSERT INTO logs (action, detail, level, created_at)
        VALUES (?, ?, ?, ?)
        """
        self.storage.execute(query, log.to_db_tuple(), commit=True)
