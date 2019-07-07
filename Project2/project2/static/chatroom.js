document.addEventListener('DOMContentLoaded', () =>
{
    const request = new XMLHttpRequest();
    request.open("POST", "/showMessagesInChannel");

    request.onload = () =>
    {
        const parsedResponse = JSON.parse(request.responseText);
        localStorage.setItem("chatroomName", parsedResponse["chatroomName"]);

        for (let i = 0; i < parsedResponse["messages"].length; i++)
        {
            const message = parsedResponse["messages"][i];
            renderMessageInLine(message);
        }
    };
    request.send();


    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () =>
    {
        document.querySelector('button').onclick = function()
        {
            const newMessage = document.querySelector('input').value;
            this.form.reset();
            socket.emit('submit message',
            {
                'newMessage': newMessage
            });
        };
    });

    socket.on('cast message', parsedResponse =>
    {
        if (parsedResponse["chatroomName"] === localStorage.chatroomName)
        {
            renderMessageInLine(parsedResponse["newMessage"]);
        }
    });
});


function renderMessageInLine(message)
{
    const messageLine = document.createElement('li');
    document.querySelector('#messagesToDisplay').append(messageLine);

    var timestampFormat = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric'
    };
    var date = new Date(message.time);
    var timestamp = date.toLocaleDateString("en-GB", timestampFormat)

    messageLine.innerHTML = `<strong>${message.sender}
                            </strong> at
                            <small>${timestamp}</small> : <span class="mx-4">
                            <big>${message.text}</big></span>`;
}