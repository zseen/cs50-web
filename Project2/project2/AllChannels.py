class AllChannels:
    def __init__(self):
        self.channels = []

    def addChannel(self, channel):
        self.channels.append(channel)

    def retrieveChannels(self):
        return self.channels
