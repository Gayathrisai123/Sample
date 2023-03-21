document.getElementById("my_captcha_form").addEventListener("submit",function(evt)
  {
  
  var response = grecaptcha.getResponse();
  //alert( response+"please verify you are humann!"); 
  if(response.length == 0) 
  { 
    //reCaptcha not verified
    //alert("please the captcha!"); 
    Swal.fire('please Verify the captcha!')
    evt.preventDefault();
    document.getElementById("button1").disabled = false;
    return false;
  }
   
});

let loginbtn = document.getElementById("loginbtn")




// loginbtn.disabled = true

var code;
function createCaptcha() {
  //clear the contents of captcha div first 
  document.getElementById('captcha').innerHTML = "";
  var charsArray ="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@!#$%^&*";
  var lengthOtp = 5;
  var captcha = [];
  for (var i = 0; i < lengthOtp; i++) {
    //below code will not allow Repetition of Characters
    var index = Math.floor(Math.random() * charsArray.length + 1); //get the next character from the array
    if (captcha.indexOf(charsArray[index]) == -1)
      captcha.push(charsArray[index]);
    else i--;
  }
  var canv = document.createElement("canvas");
  canv.id = "captcha";
  canv.width = 100;
  canv.height = 50;
  var ctx = canv.getContext("2d");
  ctx.font = "25px Georgia";
  ctx.strokeText(captcha.join(""), 0, 30);
  //storing captcha so that can validate you can save it somewhere else according to your specific requirements
  code = captcha.join("");
  document.getElementById("captcha").appendChild(canv); // adds the canvas to the body element
}
function validateCaptcha() {
//   const response = g-recaptcha.getResponse();
//  alert(response)
  event.preventDefault();
  //debugger
  if (document.getElementById("cpatchaTextBox").value == code) {
    //alert("Valid Captcha")
     Swal.fire('Logged in!')
    //console.log("valid captcha")
   
    loginbtn.disabled=false
        loginbtn.classList.remove("loginbtndisable");
        loginbtn.classList.add("loginbtn")
    
    

//     const loginForm = document.getElementById('login-form');

// loginForm.addEventListener('submit', function(event) {
//   event.preventDefault();
//   // Your code to validate email and password and log in the user
// });
//     var email = document.querySelector("input[type='email']").value;
//     fetch('http://localhost:8000/register', {
//   method: 'POST',
//   body: JSON.stringify({
//     // include any required data to authenticate the user (e.g., username, password)
//       "email": email, 
//   }),
//   headers: {
//     'Content-Type': 'application/json'
//   }
// })
// .then(response => {
//   if (response.ok) {
//     // If the response is successful, redirect the user to the login page
//     window.location.href = 'http://localhost:8000/user/login';
//   } else {
//     // If the response is not successful, handle the error
//     throw new Error('Failed to fetch login page');
//   }
// })
// .catch(error => {
//   // Handle any errors that occurred during the fetch request
//   console.error(error);
// });


  }else{
    //alert("Invalid Captcha. try Again");
    Swal.fire("Invalid Captcha. try Again");    
  
    createCaptcha();
    loginbtn.disabled=true
  }
}


// const loginForm = document.getElementById('login-form');
// // const response = cpatchaTextBox.getResponse();
// const response= document.querySelector("input[type='cpatchaTextBox']").value;
// alert(response)

// loginForm.addEventListener('submit', function(event) {
//   event.preventDefault();
//   const response = grecaptcha.getResponse();
//   if (response !== '') {
//     const loginButton = document.getElementById('login-button');
//     loginButton.removeAttribute('disabled');
//   }
//   if (loginButton.hasAttribute('disabled')) {
//     alert('Please complete the captcha to enable the login button.');
//   } else {
//     // Your code to validate email and password and captcha and log in the user
//     alert('the login button.');
//   }
// });



        