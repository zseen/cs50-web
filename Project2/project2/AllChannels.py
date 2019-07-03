class AllChannels:
    def __init__(self):
        self._channels = {}

    def addChannel(self, channel):
        self._channels[channel] = []

    def retrieveChannels(self):
        return self._channels

    def retrieveChannelByName(self, channelName):
        for channel in self._channels:
            if channel.name == channelName:
                return channel
        return None

    def isChannelNameAvailable(self, channelName):
        return self.retrieveChannelByName(channelName) is None
