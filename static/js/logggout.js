

// function logout() {
//     // Delete JWT token from local storage
// localStorage.removeItem('jwtToken');

// // Delete JWT token from cookie
// document.cookie = "jwtToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";


// alert("CICKKKK")
//}
// Define the logout function
function logout() {
    // Delete JWT token from local storage
    //localStorage.removeItem('access_token');
  
    // Delete JWT token from cookie
    // document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    alert("CICKKKK")
  }
  
  // Make the logout function accessible from your HTML file
  //window.logout = logout;
  //window.location.href = '/login';

  const button = document.getElementById('logout-button');
  button.addEventListener('click', function() {

//   document.getElementById('logout-button').addEventListener('click', function() {
    // Remove the access token from local storage
    localStorage.removeItem('access_token');

    console.log('Button clicked!');


    // Remove the access token cookie
    document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';

    // Redirect the user to the login page
    //window.location.href = 'login.html';
    //window.location.href = '/login';
});




