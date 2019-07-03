MAX_MESSAGES_TO_STORE = 100


class Channel:
    def __init__(self, name):
        self.name = name
        self._messagesInChannel = []

    def addMessage(self, message):
        self._messagesInChannel.append(message.__dict__)
        if len(self._messagesInChannel) > MAX_MESSAGES_TO_STORE:
            del self._messagesInChannel[0]

    def retrieveMessages(self):
        return self._messagesInChannel
