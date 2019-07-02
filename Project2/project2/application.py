import os

from flask import Flask, jsonify, render_template, request, session, redirect
from flask_socketio import SocketIO, emit
from datetime import datetime

from AllChannels import AllChannels
from Channel import Channel
from Message import Message


app = Flask(__name__)
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = 'super secret key'
socketio = SocketIO(app)

allChannels = AllChannels()


@app.route("/")
def index():
    if "username" not in session:
        return render_template("register.html")

    return render_template("layout.html", username=session["username"], channels=allChannels.retrieveChannels())


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    username = request.form.get("username")
    if not username:
        return jsonify({"success": False})

    session["username"] = username
    return jsonify({"success": True, "username": username})


@app.route("/createChannel", methods=["GET", "POST"])
def createChannel():
    if request.method == "GET":
        return render_template("createChannel.html")

    channelName = request.form.get("channelName")

    if not channelName:
        return jsonify({"success": False})

    if allChannels.retrieveChannelByName(channelName):
        return jsonify({"success": False})

    newChannel = Channel(channelName)
    allChannels.addChannel(newChannel)

    session["channel"] = channelName
    return jsonify({"success": True, "channelName": newChannel.name})


@app.route("/enterChannel/<channelName>", methods=["GET", "POST"])
def enterChannel(channelName):
    currentChannel = allChannels.retrieveChannelByName(channelName)
    if not currentChannel:
        return "Channel unavailable"

    session["channel"] = channelName
    return render_template("viewChannelContent.html", channelName=channelName, username=session["username"])


@socketio.on("submit message")
def sendMessage(data):
    newMessage = Message(data["newMessage"], session["username"], datetime.now().strftime("%Y-%m-%d %H:%M"))

    currentChannel = allChannels.retrieveChannelByName(session["channel"])
    currentChannel.addMessage(newMessage)

    emit("cast message", {"newMessage": newMessage.__dict__, "chatroomName": str(session["channel"])}, broadcast=True)


@app.route("/showMessagesInChannel", methods=["POST"])
def showMessagesInChannel():
    currentChannel = allChannels.retrieveChannelByName(session["channel"])
    messages = currentChannel.retrieveMessages()

    return jsonify({**{"messages": messages}, **{"chatroomName": session["channel"]}})

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")



