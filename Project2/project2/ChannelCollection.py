class ChannelCollection:
    def __init__(self):
        self._channelNameToChannel = {}

    def addChannel(self, channelName, channel):
        self._channelNameToChannel[channelName] = channel

    def retrieveAllChannelNames(self):
        return self._channelNameToChannel.keys()

    def retrieveChannelByName(self, channelName):
        return self._channelNameToChannel[channelName]

    def isChannelNameAvailable(self, channelName):
        return (channelName not in self._channelNameToChannel.keys())
