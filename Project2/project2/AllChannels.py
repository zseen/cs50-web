class AllChannels:
    def __init__(self):
        self.channels = {}

    def addChannel(self, channel):
        self.channels[channel] = []

    def retrieveChannels(self):
        return self.channels

    def retrieveChannelByName(self, channelName):
        for channel in self.channels:
            if channel.name == channelName:
                return channel
        return None

