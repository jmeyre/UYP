from uyp import config, login_manager
from mysql import connector
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    # Create the connection to the database
    conn = connector.connect(**config)

    # Create the cursor for the connection
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = '{0}'".format(user_id))

    result = cursor.fetchone()
    user = User(result[0], result[1], result[2])

    # Commit the data to the database
    conn.commit()

    # Close the cursor
    cursor.close()

    # Close the connection to the database
    conn.close()

    return user


class User:
    def __init__(self, id, category, pword):
        self.id = id
        self.category = category
        self.pword = pword

    def __repr__(self):
        return "User( ID={0}, Category={1} )".format(self.id, self.category)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        # May want to add authentication to user object here. Right now just returns true.
        return True

    def get_id(self):
        return self.id

