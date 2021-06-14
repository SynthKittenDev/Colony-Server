from logging import getLogger

from lib.exceptions import UserNotFoundInRoom

log = getLogger(__name__)


class User:
    def __init__(self, reader, writer, id):
        self.room = -1
        self.id = id
        self.mod = 0
        self.name = ""
        self.password = ""
        self.rank = 1
        self.gamesPlayed = 0
        self.gamesWon = 0
        self.gamesConsecutiveWins = 0
        self.reader = reader
        self.writer = writer
        self.address = writer.get_extra_info('peername')

    def clean(self, a):
        """
        Formats the message properly to the client format
        this function must be used before sending or client wont recognise
        """
        a = a + "\x00"
        try:
            a = a.encode('ascii')
        except UnicodeEncodeError:
            a = a.encode('UTF-8')
        return a

    async def send(self, data):
        """
        Send Data to the target
        :param data:
        :return:
        """
        data = self.clean(data)
        self.writer.write(data)
        log.debug("Sent: %r" % data)
        await self.writer.drain()


class Room:
    def __init__(self, name, id):
        self.id = id
        self.priv = 0
        self.temp = 0
        self.game = 0
        self.pwd = ''  # Room Password
        self.ucnt = 0  # User count
        self.maxu = 100  # Max User Count
        self.maxs = 0  # Max Spectator Count
        self.name = name
        self.gs = 0  # Game type
        self.users = {}
        self.usr_pos = [None, None, None, None]
        self.user_pos_id = [0, 0, 0, 0]

    async def add_user(self, user: User):
        user.room = self.id
        self.users[user.id] = user
        self.ucnt += 1

    async def remove_user(self, user_id: int):
        user = self.users.pop(user_id)
        if user is not None:
            self.ucnt -= 1
        else:
            raise UserNotFoundInRoom

    async def move_user(self, rms, user_id: int, dst: int, user):
        if self.id == dst:
            user.room = self.id
            self.users[user.id] = user
            self.ucnt += 1
            return
        user = self.users.pop(user_id, None)
        if user is not None:
            self.ucnt -= 1
            user.room = dst
            rms[dst].users[user.id] = user
            rms[dst].ucnt += 1
        else:
            raise UserNotFoundInRoom
