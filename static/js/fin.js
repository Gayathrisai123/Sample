$(".info-item .btn").click(function(){
    $(".container").toggleClass("log-in");
  });
  $(".container-form .btn").click(function(){
    // $(".container").addClass("active");
  });

 
//   document.getElementById("my_captcha_form").addEventListener("submit",function(evt)
//   {

//   var response = grecaptcha.getResponse();
//   //alert( response+"please verify you are humann!");
//   if(response.length == 0)
//   {
  
//     //reCaptcha not verified
//     Swal.fire("please verify the captcha!");
//     evt.preventDefault();
//     // document.getElementById("button1").disabled = false;
//     return false;
//   }

// });
// $(document).ready(function() {
//   $("#my_captcha_form").submit(function(event) {
//       event.preventDefault();
//       var response = grecaptcha.getResponse();
//       if(response.length == 0)
//       {
//         //reCaptcha not verified
//         Swal.fire("please verify the captcha!");
//         evt.preventDefault();
//         // document.getElementById("button1").disabled = false;
//         return false;
//       }

//   });
// });

// document.getElementById('b5').onclick = function(){
// 	swal({
// 		title: "Are you sure?",
// 		text: "You will not be able to recover this imaginary file!",
// 		type: "warning",
// 		showCancelButton: true,
// 		confirmButtonColor: '#DD6B55',
// 		confirmButtonText: 'Yes, delete it!',
// 		cancelButtonText: "No, cancel plx!",
// 		closeOnConfirm: false,
// 		closeOnCancel: false
// 	},
// 	function(isConfirm){
//     if (isConfirm){
//       swal("Deleted!", "Your imaginary file has been deleted!", "success");
//     } else {
//       swal("Cancelled", "Your imaginary file is safe :)", "error");
//     }
// 	});
// };