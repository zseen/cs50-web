MAX_MESSAGES_TO_STORE = 100


class Channel:
    def __init__(self, name):
        self.name = name
        self.messagesInChannel = []

    def addMessage(self, message):
        self.messagesInChannel.append(message.__dict__)
        if len(self.messagesInChannel) > MAX_MESSAGES_TO_STORE:
            del self.messagesInChannel[0]

    def retrieveMessages(self):
        return self.messagesInChannel

