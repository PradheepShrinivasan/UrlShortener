import bcrypt
from app import app

from flask_login import UserMixin
from models.user_database import UserDatabase


class User(UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.authenticated = False

    @classmethod
    def getuser(cls, email):
        """Get the user given a email address
            it returns a User object with email address
            and hashes password from database"""

        user_db = UserDatabase()
        password = user_db.get_password(email)
        if password:
            return User(email, password)
        else:
            return None

    def checkpassword(self, password):
        """ hashes the password provided and checks with the
        password from the database
        """

        # In this case the encoded password is stored in the self.password and
        # password is the raw password
        app.logger.debug("user name (%s) and hashed password(%s)", self.email, self.password)
        if self.password == bcrypt.hashpw(password.encode('utf-8'), self.password.encode('utf-8')):
            self.authenticated = True
            return True
        else:
            self.authenticated = False
            return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def add_user(self):
        """store the user information to database"""

        app.logger.debug("saving user(%s) with password(%s)", self.email, self.password)
        user_db = UserDatabase()

        password_hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        return user_db.save_user(self.email, password_hashed)