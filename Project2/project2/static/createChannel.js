document.addEventListener('DOMContentLoaded', () =>
{
  document.querySelector('#channelCreationForm').onsubmit = () =>
  {
      const request = new XMLHttpRequest();
      const channelName = document.querySelector('#channelName').value;
      request.open('POST', '/createChannel');

      request.onload = () =>
      {
          const channelCreation = JSON.parse(request.responseText);

          if (channelCreation.success)
          {
              return window.location = '/';
          }
          else
          {
              document.querySelector('#errorMessagePlace').innerHTML = channelCreation.errorMessage;
          }
      }

      const channelData = new FormData();
      channelData.append('channelName', channelName);
      request.send(channelData);

      return false;
  };
});