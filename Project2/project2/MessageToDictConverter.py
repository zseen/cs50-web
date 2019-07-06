class MessageToDictConverter:

    @staticmethod
    def convertMessageToDict(message):
        data = {'text': message.text, 'sender': message.sender, 'time': message.time}
        return data

    @staticmethod
    def convertAllMessagesToDict(messages):
        convertedMessages = []
        print("messages in SAM :", messages)
        for message in messages:
            convertedMessages.append(MessageToDictConverter.convertMessageToDict(message))

        return convertedMessages