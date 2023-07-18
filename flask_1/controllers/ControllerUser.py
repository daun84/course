from flask_login import UserMixin

from models.ModelUser import ModelUser

class ControllerUser(UserMixin):
    def __init__(self, user):
        super().__init__()
        self.__user: ModelUser = user 

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        self.__user = user

    def get_id(self) -> str:
        return str(self.__user.username)
