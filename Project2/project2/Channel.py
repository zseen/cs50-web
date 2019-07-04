MAX_MESSAGES_TO_STORE = 100


class Channel:
    def __init__(self, name):
        self._name = name
        self._messagesInChannel = []

    def addMessage(self, message):
        self._messagesInChannel.append(message)
        if len(self._messagesInChannel) > MAX_MESSAGES_TO_STORE:
            del self._messagesInChannel[0]

    def retrieveMessages(self):
        return self._messagesInChannel

    def serializeMessage(self, message):
        return message.__dict__

    def serializeAllMessages(self):
        serializedMessages = []
        for message in self._messagesInChannel:
            serializedMessages.append(message.__dict__)

        return serializedMessages
