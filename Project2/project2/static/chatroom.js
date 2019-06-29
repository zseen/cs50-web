document.addEventListener('DOMContentLoaded', () => {

    const request = new XMLHttpRequest();
    request.open("POST", "/listmessages");
    console.log("after request.open");

    request.onload = () => {
        console.log("currently in request.onload");
        const data = JSON.parse(request.responseText);
        console.log("currently in request.onload");
        localStorage.setItem("chatName", data["chatName"])
        let i;
        for ( i = 0; i < data["message"].length; i++) {
            const li = document.createElement('li');
            const response = data["message"][i];

            li.innerHTML = `<strong>${response["username"]}</strong> at <small>${response["time"]}</small> : <span class="mx-4"><big>${response["selection"]}</big></span>`;
            document.querySelector('#messages').append(li);
        }
    };
    request.send();


    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    console.log(socket);

    socket.on('connect', () => {
        console.log("socket connected");

        document.querySelector('button').onclick = function () {
            console.log("clicked on button");
            const selection = document.querySelector('input').value;
            this.form.reset();
            socket.emit('submit message', {'selection': selection});
        };
    });

    socket.on ('cast message', data => {
        if (data["chatName"] === localStorage.chatName) {
            const li = document.createElement('li');

            li.innerHTML = `<strong>${data["username"]}</strong> at <small>${data["time"]}</small> : <span class="mx-4"><big>${data["selection"]}</big></span>`;
            document.querySelector('#messages').append(li);
        }
    });


});