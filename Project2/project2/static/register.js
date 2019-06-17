 document.addEventListener('DOMContentLoaded', () => {

     //alert("guess I am in eventListener")

      document.querySelector('#form').onsubmit = () => {

          //alert("entered onsubmit")

          // Initialize new request
          const request = new XMLHttpRequest();
          const username = document.querySelector('#username').value;
          request.open('POST', '/register');

          //alert(username)

          // Callback function for when request completes
          request.onload = () => {

              // Extract JSON data from request
              const registration = JSON.parse(request.responseText);

              //alert("entered request.onload")

              // Update the result div
              if (registration.success) {
                  //alert(registration.success)
                  //alert("Welcome")

                  return window.location = '/';
                  alert("should not be here")

              }
              else {
                  document.querySelector('#result').innerHTML = 'There was an error.';
              }
          }

           //alert("send userdata")
          // Add data to send with request
          const userData = new FormData();
          userData.append('username', username);

          // Send request
          request.send(userData);
          //alert("userdata sent")

      };


  });