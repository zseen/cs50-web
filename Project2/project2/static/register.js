 document.addEventListener('DOMContentLoaded', () => {

      document.querySelector('#form').onsubmit = () => {

          // Initialize new request
          const request = new XMLHttpRequest();
          const username = document.querySelector('#username').value;
          request.open('POST', '/register');

          // Callback function for when request completes
          request.onload = () => {

              // Extract JSON data from request
              const registration = JSON.parse(request.responseText);

              // Update the result div
              if (registration.success) {
                  const greeting = `Hello ${registration.username}!`
                  document.querySelector('#result').innerHTML = greeting;
              }
              else {
                  document.querySelector('#result').innerHTML = 'There was an error.';
              }
          }

          // Add data to send with request
          const userData = new FormData();
          userData.append('username', username);

          // Send request
          request.send(userData);

          return window.location.pathname = '/layout.html';
      };
  });