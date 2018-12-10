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


class Class:
    def __init__(self, title, lvl, maxCapacity, curSize, instructorID, room, timeslotID, sessionID, classID, price):
        self.title = title
        self.lvl = lvl
        self.maxCapacity = maxCapacity
        self.curSize = curSize
        self.instructorID = instructorID
        self.room = room
        self.timeslotID = timeslotID
        self.sessionID = sessionID
        self.classID = classID
        self.price = price

    def __repr__(self):
        return "Class( ID={0}, Title=\"{1}\", Level={2}, MaxCapacity={3}, " \
               "CurrentSize={4}, InstructorID={5}, Room={6}, TimeSlotID={7}, SessionID={8} )".format(
            self.id, self.title, self.lvl, self.maxCapacity, self.curSize, self.instructorID, self.room,
            self.timeslotID, self.sessionID)


class Student:
    def __init__(self, id, fName, mName, lName, suffix, preferred, bDay, gender, race, gradeLevel, expGradYear,
                 street, city, state, zip, email, phone, esl, gt):
        self.id = id
        self.fName = fName
        self.mName = mName
        self.lName = lName
        self.suffix = suffix
        self.preferred = preferred
        self.bDay = bDay
        self.gender = gender
        self.race = race
        self.gradeLevel = gradeLevel
        self.expGradYear = expGradYear
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.email = email
        self.phone = phone
        self.esl = esl
        self.gt = gt


class Staff:
    def __init__(self, id, fName, mName, lName, suffix, phone, email, street, city, state, zip):

        self.id = id
        self.fName = fName
        self.mName = mName
        self.lName = lName
        self.suffix = suffix
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.email = email
        self.phone = phone

