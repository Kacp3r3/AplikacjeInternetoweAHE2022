from condition_monitor.models import *
import random
import datetime
import time
class DBGenerator():
    def __init__(self):
        self.db = DBConnection()
        self.rooms = []
        self.users = []

    def cleanDB(self):
        self.db._engine.drop_all()
        self.db._engine.create_all()

    def genDB(self):
        self.genUsers()
        self.genRooms()
        self.genAccesses()
        self.genMeasurements()

    def genUsers(self):
        usernames = ["Kacper", "Bartek", "Ola", "Karolina", "Kasia", "Natalia", "Krzysztof", "Jan"]
        for user in usernames:
            user = User(username=user, email=user+"@gmail.com", password_hash="###")
            self.users.append(user)
            self.db.session.add(user)
        self.db.flsuh()

    def genRooms(self):
        room_letters = ["A","B"]
        floors = 6
        for letter in room_letters:
            for floor in range(floors):
                for d in [1,2,3,4,5,7]:
                    for j in [1,2,3,4]:
                        room = Room(name=letter+str(floor+1)+str(d)+str(j))
                        self.rooms.append(room)
                        self.db.session.add(room)
        self.db.flsuh()

    def genAccesses(self):
        for user in self.users:
            selected_ids = [-1]
            for i in range(random.randint(10, 40)):
                randomid = -1
                while randomid in selected_ids:
                    randomid = self.rooms[random.randint(0, len(self.rooms)-1)].id
                self.db.session.add(Access(userid=user.id, roomid = randomid))
        self.db.flsuh()

    def genMeasurements(self):
        time_now = datetime.datetime.now()
        time_start = time_now - datetime.timedelta(days=3)
        time_curr = time_start
        for room in self.rooms:
            time_curr = time_start
            while time_curr < time_now:
                self.db.session.add(Measurement(roomid = room.id, temperature = int(random.gauss(15,10)), humidity = int(random.gauss(50,15)), timestamp = time_curr))
                time_curr += datetime.timedelta(minutes=80)
        self.db.flsuh()

if __name__ == "__main__":
    generator = DBGenerator()
    generator.cleanDB()
    generator.genDB()