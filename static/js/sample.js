
function show_hide_password(target){
	var input = document.getElementById('password-input');
	if (input.getAttribute('type') == 'password') {
		target.classList.add('view');
		input.setAttribute('type', 'text');
	} else {
		target.classList.remove('view');
		input.setAttribute('type', 'password');
	}
	return false;
}


function signup(target){
	var input = document.getElementById('password');
	if (input.getAttribute('type') == 'password') {
		target.classList.add('view');
		input.setAttribute('type', 'text');
	} else {
		target.classList.remove('view');
		input.setAttribute('type', 'password');
	}
	return false;
}

function password_confirm(target){
	var input = document.getElementById('confirm_password');
	if (input.getAttribute('type') == 'password') {
		target.classList.add('view');
		input.setAttribute('type', 'text');
	} else {
		target.classList.remove('view');
		input.setAttribute('type', 'password');
	}
	return false;
}



var state= false;
function toggle(){
    if(state){
	document.getElementById("password").setAttribute("type","password");
	document.getElementById("eye").style.color='#7a797e';
	state = false;
     }
     else{
	document.getElementById("password").setAttribute("type","text");
	document.getElementById("eye").style.color='#5887ef';
	state = true;
     }
}


// $(document).ready(function (){$('input').bind('input', function() {  var c = this.selectionStart,      r = /[^a-z0-9 .]/gi,      v = $(this).val();  if(r.test(v)) {    $(this).val(v.replace(r, ''));    c--;  }  this.setSelectionRange(c, c);});

// });


// function verifyPassword() {
// 	var pw = document.getElementById("pswd").value;
// 	var pw1 = document.getElementById("pswd1").value;  
// 	//check empty password field
// 	if(pw == "") {
// 	   document.getElementById("message").innerHTML = "**Fill the password please!";
// 	   return false;
// 	}

// 	if(pw != pw1)  
// 	{   
// 	  //alert("Passwords did not match");  
// 	  document.getElementById("message1").innerHTML = "Passwords did not match";
// 	  return false;
// 	}
// 	else {  
// 		//alert("Password created successfully");  
// 	  }  
   
//    //minimum password length validation
// 	if(pw.length < 8) {
// 	   document.getElementById("message").innerHTML = "**Please type at least 8 charcters";
	   
// 	   return false;
// 	}

	
//   //maximum length of password validation
// 	if(pw.length > 15) {
// 	   document.getElementById("message").innerHTML = "**Password length must not exceed 15 characters";
// 	   return false;
// 	} else {
// 	   alert("Password is correct");
// 	}
//   }
