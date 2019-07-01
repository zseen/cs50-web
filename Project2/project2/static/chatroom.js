document.addEventListener('DOMContentLoaded', () => {

    const request = new XMLHttpRequest();
    request.open("POST", "/showMessagesInChannel");

    request.onload = () => {
        console.log("in request.onload");
        const messagingData = JSON.parse(request.responseText);
        console.log("json: ", request.responseText)
        console.log("messagingData in request.onload: ", messagingData);
        localStorage.setItem("chatroomName", messagingData["chatroomName"])


        for (let i = 0; i < messagingData["messages"].length; i++) {
            const messageLine = document.createElement('li');
            const singleMessageData = messagingData["messages"][i];
            document.querySelector('#messagesToDisplay').append(messageLine);

            displayMessagesOnEachLine(singleMessageData, messageLine);
        }
    };
    request.send();


    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        document.querySelector('button').onclick = function () {
            const newMessage = document.querySelector('input').value;
            this.form.reset();
            socket.emit('submit message', {'newMessage': newMessage});
            console.log("newMessage in connected socket: ", newMessage);
        };
    });

    socket.on ('cast message', messagingData => {
        console.log("messagingData in cast message: ", messagingData);
        console.log(messagingData["chatroomName"]);
        console.log(messagingData["chatroomName"] === localStorage.chatroomName);

        if (messagingData["chatroomName"] === localStorage.chatroomName) {
            const messageLine  = document.createElement('li');
            document.querySelector('#messagesToDisplay').append(messageLine );

            displayMessagesOnEachLine(messagingData["newMessage"], messageLine);
        }
    });
});


function displayMessagesOnEachLine(message, line)
{
    console.log("sender: ", message["sender"]);
    line.innerHTML = `<strong>${message.sender}</strong> at <small>${message.time}</small> : <span class="mx-4"><big>${message.text}</big></span>`;
}

