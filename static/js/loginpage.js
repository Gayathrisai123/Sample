let captchaDisplayed = document.getElementById("displayedcaptcha");
let captchaUserInput = document.getElementById("captchauserinputtext");
let username = document.getElementById("email");
let password = document.getElementById("password");
let errormsg = document.getElementById("errormsg")
let loginbtn = document.getElementById("loginbtn")
let audio = document.getElementById("audio")

audio.volume =0.04

loginbtn.disabled = true
errormsg.style.display = "none"

let captcha;
let chars = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

function generateCaptcha() {
    captcha = ""
    for (let i = 0; i < 4; i++) {
        let index = Math.floor(Math.random() * chars.length);
        captcha = captcha + chars[index]
    }
    captchaDisplayed.value = captcha
}
generateCaptcha()

function validateCaptcha() {

    if (captcha == captchaUserInput.value && username.value !="" && password.value !="") {
        console.log("valid captcha")
        loginbtn.disabled=false
        loginbtn.classList.remove("loginbtndisable");
        loginbtn.classList.add("loginbtn")
    }
    else {
        console.log("invalid captcha or username,password")
        loginbtn.disabled=true
        loginbtn.classList.add("loginbtndisable");
        loginbtn.classList.remove("loginbtn")
        errormsg.style.display = "block"
        generateCaptcha();
        captchaUserInput.value = ""
        username.value = ""
        password.value = ""
    }
}

// validations and errors

function errors() {
    let error = [];

    if (document.getElementById("email").value == "") error.push("email");
    if (document.getElementById("password").value == "") error.push("password");
    if (document.getElementById("captchauserinputtext").value == "") error.push("captchauserinputtext");

    console.log(error)
    return error;
}

function validateFormOnSubmit() {
    console.log("validateFormOnSubmit")
    let error = errors();
    if (error.length == 0) {

        let email = document.getElementById("email").value
        let password = document.getElementById("password").value;
 
        const options = {
            method: 'GET',
        };

        console.log("before fetcg", email, password)

        fetch(`http://localhost:8081/users/login/?email=${email}&password=${password}`, options)
            .then(res => res.json())
            .then(data => {
                console.log(data);
                if(data == true){

                    window.location.href = '../dashboard.html';
                }else{
                    document.getElementById("errormsg").innerHTML = "Email or password not found !";
                    errormsg.style.display="block"
                    errormsg.classList.add("detailsvalidation")
                }
            })
            // http://localhost:80/loginpage.html
            .catch((er) => {
                console.log(er)
            });
    } else {
        document.getElementById("errormsg").innerHTML = "All the fields need to met requirements";
    }

}

//entered password to see and to hide

function myFunction() {
    var x = document.getElementById("password");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}
