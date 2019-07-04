class ChannelCollection:
    def __init__(self):
        self._channels = {}

    def addChannel(self, channelName, channel):
        self._channels[channelName] = channel

    def retrieveAllChannelNames(self):
        return self._channels.keys()

    def retrieveChannelByName(self, channelName):
        return self._channels[channelName]

    def isChannelNameAvailable(self, channelName):
        return channelName not in self._channels.keys()
