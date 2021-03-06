from flask import Flask, jsonify, render_template, request, session, redirect
from flask_socketio import SocketIO, emit
from datetime import datetime
import os

from ChannelCollection import ChannelCollection
from Channel import Channel
from Message import Message
from MessageToDictConverter import MessageToDictConverter

app = Flask(__name__)

app.secret_key = os.urandom(24)
socketio = SocketIO(app)

allChannels = ChannelCollection()


@app.route("/")
def index():
    if "username" not in session:
        return render_template("layout.html")

    if "channelName" in session:
        return render_template("viewChannelContent.html", channelName=session["channelName"], username=session["username"])

    return render_template("layout.html", username=session["username"],
                           channelNames=allChannels.retrieveAllChannelNames())


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    session.clear()

    username = request.form.get("username")
    if not username:
        return jsonify({"success": False, "errorMessage": "Please submit a user name."})

    session["username"] = username
    return jsonify({"success": True, "username": username})


@app.route("/createChannel", methods=["GET", "POST"])
def createChannel():
    if request.method == "GET":
        return render_template("createChannel.html")

    channelName = request.form.get("channelName")
    if not channelName:
        return jsonify({"success": False, "errorMessage": "Please submit a channel name."})

    if not allChannels.isChannelNameAvailable(channelName):
        return jsonify({"success": False, "errorMessage": "Channel already exists with this name."})

    allChannels.addChannel(channelName, Channel(channelName))
    session["channelName"] = channelName

    return jsonify({"success": True, "channelName": channelName})


@app.route("/enterChannel/<channelName>", methods=["GET", "POST"])
def enterChannel(channelName):
    currentChannel = allChannels.retrieveChannelByName(channelName)
    if not currentChannel:
        return render_template("apology.html", errorMessage="Channel not found")

    session["channelName"] = channelName
    return render_template("viewChannelContent.html", channelName=channelName, username=session["username"])


@socketio.on("submit message")
def sendMessage(data):
    messageTime = datetime.now().isoformat()
    newMessage = Message(data["messageText"], session["username"], messageTime)

    currentChannel = allChannels.retrieveChannelByName(session["channelName"])
    currentChannel.addMessage(newMessage)
    newMessageDict = MessageToDictConverter.convertMessageToDict(newMessage)

    emit("cast message", {"messageText": newMessageDict, "chatroomName": session["channelName"]}, broadcast=True)


@app.route("/showMessagesInChannel", methods=["POST"])
def showMessagesInChannel():
    currentChannel = allChannels.retrieveChannelByName(session["channelName"])

    messages = currentChannel.retrieveMessages()
    messagesConvertedToDictsList = MessageToDictConverter.convertAllMessagesToDict(messages)

    return jsonify({"messages": messagesConvertedToDictsList, "chatroomName": session["channelName"]})


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
