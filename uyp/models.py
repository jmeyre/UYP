class User:
    def __init__(self, id, category, pword):
        self.id = id
        self.category = category
        self.pword = pword

    def __repr__(self):
        return "User( ID={0}, Category={1} )".format(self.id, self.category)
