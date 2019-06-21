MAX_MESSAGES_TO_STORE = 100


class Channel:
    def __init__(self, name):
        self.name = name
        self.messagesInChannel = []

    def addMessage(self, message):
        self.messagesInChannel.append(message)
        if len(self.messagesInChannel) > MAX_MESSAGES_TO_STORE:
            self.messagesInChannel[0].remove()

    def retrieveMessages(self):
        return self.messagesInChannel

