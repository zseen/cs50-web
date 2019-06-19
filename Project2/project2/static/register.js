document.addEventListener('DOMContentLoaded', () =>
{
  document.querySelector('#registrationForm').onsubmit = () =>
  {
      const request = new XMLHttpRequest();
      const username = document.querySelector('#username').value;
      request.open('POST', '/register');
      console.log(username);

      userStorage = window.localStorage;
      userStorage.setItem(username, username)
      console.log(userStorage);

      request.onload = () =>
      {
          console.log("entered request.onload");
          const registration = JSON.parse(request.responseText);

          console.log(registration.success);

          if (registration.success)
          {
              console.log("time to redirect");
              return window.location = '/';
          }
          else
          {
              document.querySelector('#errorMessagePlace').innerHTML = 'There was an error.';
          }
      }
      console.log("about to send userdata");
      const userData = new FormData();
      userData.append('username', username);

      request.send(userData);
      console.log("userdata sent");
      return false;
  };
});