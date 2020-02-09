class MessageToDictConverter:

    @staticmethod
    def convertMessageToDict(message):
        return {'text': message.text, 'sender': message.sender, 'time': message.time}


    @staticmethod
    def convertAllMessagesToDict(messages):
        convertedMessages = []
        for message in messages:
            convertedMessages.append(MessageToDictConverter.convertMessageToDict(message))

        return convertedMessages