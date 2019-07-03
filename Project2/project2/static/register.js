document.addEventListener('DOMContentLoaded', () =>
{
  document.querySelector('#registrationForm').onsubmit = () =>
  {
      const request = new XMLHttpRequest();
      const username = document.querySelector('#username').value;
      request.open('POST', '/register');

      request.onload = () =>
      {
          const registration = JSON.parse(request.responseText);
          if (registration.success)
          {
              return window.location = '/';
          }
          else
          {
              document.querySelector('#errorMessagePlace').innerHTML = registration.errorMessage;
          }
      }

      const userData = new FormData();
      userData.append('username', username);
      request.send(userData);

      return false;
  };
});