document.addEventListener('DOMContentLoaded', () =>
{
  document.querySelector('#channelCreationForm').onsubmit = () =>
  {
      const request = new XMLHttpRequest();
      const channelName = document.querySelector('#channelName').value;
      request.open('POST', '/createChannel');
      console.log(channelName);


      request.onload = () =>
      {
          console.log("entered request.onload");
          const channelCreation = JSON.parse(request.responseText);

          console.log(channelCreation.success);

          if (channelCreation.success)
          {
              console.log("time to redirect");
              return window.location = '/';
          }
          else
          {
              document.querySelector('#errorMessagePlace').innerHTML = 'There was an error.';
          }
      }
      console.log("about to send channelData");
      const channelData = new FormData();
      channelData.append('channelName', channelName);

      request.send(channelData);
      console.log("channelData sent");
      return false;
  };
});