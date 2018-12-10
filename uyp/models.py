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
    def __init__(self, title, lvl, maxCap, curSize, instructorID, room, timeslotID, sessionID, classID, price):
        self.title = title
        self.lvl = lvl
        self.maxCap = maxCap
        self.curSize = curSize
        self.instructorID = instructorID
        self.room = room
        self.timeslotID = timeslotID
        self.sessionID = sessionID
        self.classID = classID
        self.price = price

    def __repr__(self):
        return "Class( title={0}, lvl={1}, maxCap={2}, curSize={3}, instructorID={4}, room={5}, timeslotID={6}, sessionID={7}, classID={8}, price={9} )".format(
            self.title, self.lvl, self.maxCap, self.curSize, self.instructorID, self.room, self.timeslotID,
            self.sessionID, self.classID, self.price)


class Student:
    def __init__(self, id, fName, mName, lName, suffix, preferred, bDay, gender, race, gradeLevel, expGradDate,
                 street, city, state, zip, email, phone, esl, gt, acceptedYear, acceptedBy, bill, NCHI, status,
                 grantFunded, otherInfo, expSchool):
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
        self.expGradDate = expGradDate
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.email = email
        self.phone = phone
        self.esl = esl
        self.gt = gt
        self.acceptedYear = acceptedYear
        self.acceptedBy = acceptedBy
        self.bill = bill
        self.NCHI = NCHI
        self.status = status
        self.grantFunded = grantFunded
        self.otherInfo = otherInfo
        self.expSchool = expSchool

    def __repr__(self):
        return "Class( id={0}, fName={1}, mName={2}, lName={3}, suffix={4}, preferred={5}, bDay={6}, gender={7}, race={8}, gradeLevel={9}, expGradDate={10}, street={11}, city={12}, state={13}, zip={14}, email={15}, phone={16}, esl={17}, gt={18}, accepted={19}, acceptedBy={20}, bill={21}, NCHI={22}, status={23}, grantFunded={24}, otherInfo={25}, expSchool={26} )".format(
            self.id, self.fName, self.mName, self.lName, self.suffix, self.preferred, self.bDay, self.gender, self.race,
            self.gradeLevel, self.expGradDate, self.street, self.city, self.state, self.zip, self.email, self.phone,
            self.esl, self.gt, self.accepted, self.acceptedBy, self.bill, self.NCHI, self.status, self.grantFunded,
            self.otherInfo, self.expSchool)


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

    def __repr__(self):
        return "Class( id={0}, fName={1}, mName={2}, lName={3}, suffix={4}, phone={5}, email={6}, street={7}, city={8}, state={9}, zip={10} )".format(
            self.id, self.fName, self.mName, self.lName, self.suffix, self.phone, self.email, self.street, self.city,
            self.state, self.zip)


class Guardian:
    def __init__(self, studentID, fName, mName, lName, phone, email, street, city, state, zip):
        self.studentID = studentID
        self.fName = fName
        self.mName = mName
        self.lName = lName
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.email = email
        self.phone = phone


class HealthCondition:
    def __init__(self, studentID, condition, description):
        self.studentID = studentID
        self.condition = condition
        self.description = description


class Disability:
    def __init__(self, studentID, disability):
        self.studentID = studentID
        self.disability = disability


class School:
    def __init__(self, studentID, name, type, district, schoolID):
        self.studentID = studentID
        self.name = name
        self.type = type
        self.district = district
        self.schoolID = schoolID
#
# class Gt:
#     def __index__(self, studentID, schoolID):
#         self.studentID = studentID
#         self.schoolID = schoolID
