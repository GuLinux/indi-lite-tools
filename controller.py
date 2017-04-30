from session import Session
import os

class Controller:
    def __init__(self):
        self.__sessions = []
        self.path = os.environ['HOME']

    def sessions(self):
        return [s.name for s in self.__sessions]

    def new_session(self, name):
        if(self.get_session(name)):
            return False
        self.__sessions.append(Session(name, self.path))
        return True

    def remove_session(self, name):
        session = self.get_session(name)
        if not session:
            return False
        self.__sessions = [s for s in self.__sessions if s.name != name]
        session.remove()
        return True

    def get_session(self, name):
        session = [s for s in self.__sessions if s.name == name]
        return session[0] if len(session) > 0 else None
