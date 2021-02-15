from flask_login import UserMixin


class User(UserMixin):
     
     def __init__(self, user_id, username, password):
          self.user_id = str(user_id)
          self.username = username
          self.password = password

     def get_id(self):
          return self.user_id