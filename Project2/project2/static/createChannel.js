document.addEventListener('DOMContentLoaded', () =>
{
    document.querySelector('#channelCreationForm').onsubmit = () =>
    {
        const request = new XMLHttpRequest();
        const channelName = document.querySelector('#channelName').value;
        request.open('POST', '/createChannel');

        request.onload = () =>
        {
            const channelCreationResponse = JSON.parse(request.responseText);

            if (channelCreationResponse.success)
            {
                return window.location = '/';
            }
            else
            {
                document.querySelector('#errorMessagePlace').innerHTML = channelCreationResponse.errorMessage;
            }
        }

        const channelData = new FormData();
        channelData.append('channelName', channelName);
        request.send(channelData);

        return false;
    };
});