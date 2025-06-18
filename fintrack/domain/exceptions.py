class ConflictError(Exception):
    def __init__(self, model: str, field: str):
        super().__init__(f"Conflict in {model}.{field}")
