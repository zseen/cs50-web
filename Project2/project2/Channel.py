MAX_MESSAGES_TO_STORE = 100


class Channel:
    def __init__(self, name):
        self._name = name
        self._messages = []

    def addMessage(self, message):
        self._messages.append(message)
        if len(self._messages) > MAX_MESSAGES_TO_STORE:
            del self._messages[0]

    def retrieveMessages(self):
        return self._messages


