import os

from flask import Flask, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import os
import requests


from AllChannels import AllChannels
from Channel import Channel
from Message import Message


from flask import Flask, jsonify, render_template, request, session, redirect

app = Flask(__name__)
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = 'super secret key'
socketio = SocketIO(app)


allChannels = AllChannels()


@app.route("/")
def index():
    if "username" in session:
        print("logged in as ", session["username"])

    if "username" not in session:
        return render_template("register.html")

    return render_template("layout.html", username=session["username"], channels=allChannels.retrieveChannels())


@app.route("/register", methods=["GET", "POST"])
def login():
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
def message(data):
    print(data)
    newMessage = data["newMessage"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M")

    response_dict = {"newMessage": newMessage, "time": time, "username": session["username"]}
    currentChannel = allChannels.retrieveChannelByName(session["channel"])

    currentChannel.addMessage(response_dict)

    emit("cast message", {**response_dict, **{"chatroomName": str(session["channel"])}}, broadcast=True)


@app.route("/showMessagesInChannel", methods=["POST"])
def showMessagesInChannel():
    currentChannel = allChannels.retrieveChannelByName(session["channel"])
    messages = currentChannel.retrieveMessages()
    print("messages in listMessage", messages)

    return jsonify({**{"messages": messages}, **{"chatroomName": session["channel"]}})

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")



