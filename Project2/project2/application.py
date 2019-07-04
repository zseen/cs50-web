from flask import Flask, jsonify, render_template, request, session, redirect
from flask_socketio import SocketIO, emit
from time import strftime
import os

from ChannelCollection import ChannelCollection
from Channel import Channel
from Message import Message

app = Flask(__name__)

app.secret_key = os.urandom(24)
socketio = SocketIO(app)

channelCollection = ChannelCollection()


@app.route("/")
def index():
    print("you are in index")
    if "username" not in session:
        return render_template("register.html")

    return render_template("layout.html", username=session["username"],
                           channels=channelCollection.retrieveAllChannelNames())


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    username = request.form.get("username")
    if not username:
        return jsonify({"success": False, "errorMessage": "Please submit a channel name."})

    session["username"] = username
    return jsonify({"success": True, "username": username})


@app.route("/createChannel", methods=["GET", "POST"])
def createChannel():
    if request.method == "GET":
        return render_template("createChannel.html")

    channelName = request.form.get("channelName")
    if not channelName:
        return jsonify({"success": False, "errorMessage": "Please submit a username."})

    if not channelCollection.isChannelNameAvailable(channelName):
        return jsonify({"success": False, "errorMessage": "Channel already exists with this name."})

    channelCollection.addChannel(channelName, Channel(channelName))

    session["channel"] = channelName
    return jsonify({"success": True, "channelName": channelName})


@app.route("/enterChannel/<channelName>", methods=["GET", "POST"])
def enterChannel(channelName):
    currentChannel = channelCollection.retrieveChannelByName(channelName)
    if not currentChannel:
        return render_template("apology.html", errorMessage="Channel not found")

    session["channel"] = channelName
    return render_template("viewChannelContent.html", channelName=channelName, username=session["username"])


@socketio.on("submit message")
def sendMessage(data):
    messageTime = strftime("%Y-%m-%d %H:%M:%S")
    newMessage = Message(data["newMessage"], session["username"], messageTime)

    currentChannel = channelCollection.retrieveChannelByName(session["channel"])
    currentChannel.addMessage(newMessage)
    serializedNewMessage = currentChannel.serializeMessage(newMessage)

    emit("cast message", {"newMessage": serializedNewMessage, "chatroomName": session["channel"]}, broadcast=True)


@app.route("/showMessagesInChannel", methods=["POST"])
def showMessagesInChannel():
    currentChannel = channelCollection.retrieveChannelByName(session["channel"])
    serializedMessages = currentChannel.serializeAllMessages()

    return jsonify({"messages": serializedMessages, "chatroomName": session["channel"]})


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
