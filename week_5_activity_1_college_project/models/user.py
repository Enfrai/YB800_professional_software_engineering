class User:
    """Base class for all system users."""

    def __init__(self, user_id: str, name: str, email: str):
        self._user_id = user_id
        self._name = name
        self._email = email

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    def display_info(self) -> str:
        return f"ID: {self._user_id} | Name: {self._name} | Email: {self._email}"