document.addEventListener('DOMContentLoaded', () => {

    const request = new XMLHttpRequest();
    request.open("POST", "/showMessagesInChannel");

    request.onload = () => {
        const messagingData = JSON.parse(request.responseText);
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
        };
    });

    socket.on ('cast message', messagingData => {

        if (messagingData["chatroomName"] === localStorage.chatroomName) {
            const messageLine  = document.createElement('li');
            document.querySelector('#messagesToDisplay').append(messageLine );

            displayMessagesOnEachLine(messagingData, messageLine);
        }
    });
});


function displayMessagesOnEachLine(message, line)
{
    line.innerHTML = `<strong>${message["username"]}</strong> at <small>${message["time"]}</small> : <span class="mx-4"><big>${message["newMessage"]}</big></span>`;
}

