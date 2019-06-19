import os

from flask import Flask, request
from flask_socketio import SocketIO, emit
import os
import requests


from AllChannels import AllChannels

from flask import Flask, jsonify, render_template, request, session, redirect

app = Flask(__name__)
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = 'super secret key'
socketio = SocketIO(app)


allChannels = AllChannels()


@app.route("/")
def index():
    print("Got into index()")

    print(session)

    if "username" in session:
        print("logged in as ", session["username"])

    if not "username" in session:
        print("No one logged in")
        return render_template("register.html")

    print(allChannels.retrieveChannels())


    return render_template("layout.html", username=session["username"], channels=allChannels.retrieveChannels())


@app.route("/register", methods=["GET", "POST"])
def login():
    session.clear()

    username = request.form.get("username")
    print(username)
    print("Does it get here?")

    if not username:
        return jsonify({"success": False})

    session["username"] = username

    print("session: ", session["username"])

    if "username" in session:
        print("login success")

    return jsonify({"success": True, "username": username})


@app.route("/createChannel", methods=["GET", "POST"])
def createChannel():
    if request.method == "GET":
        return render_template("createChannel.html")

    channelName = request.form.get("channelName")

    print("trying to create: ", channelName)

    if not channelName:
        return jsonify({"success": False})

    print("channel already exists: ", channelName in allChannels.retrieveChannels())

    if channelName in allChannels.retrieveChannels():
        return jsonify({"success": False})

    allChannels.addChannel(channelName)

    print(allChannels.retrieveChannels())

    session["channel"] = channelName
    return jsonify({"success": True, "channelName": channelName})


def enterChannel():
    pass



@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")



