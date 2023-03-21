$(document).ready(function(){
          
    $("#confirm_password").bind('keyup change', function(){

      check_Password( $("#password").val(), $("#confirm_password").val() )
      
      
    })

    $("#sign_in_btn").click(function(){

      check_Password( $("#password").val(), $("#confirm_password").val() )

    })
  })

  function check_Password( Pass, Con_Pass){

    if(Pass === ""){

      

    }else if( Pass === Con_Pass){

      $("#sign_in_btn").removeAttr("onclick")
      $('#confirm_password_msg').show()
      $("#confirm_password_msg").html('<div style="margin-top: 17px" class="alert alert-success">Password matched</div>')

      setTimeout(function() {
          $('#confirm_password_msg').fadeOut('slow');
      }, 3000);

    }else{
      $("#confirm_password").focus()
      $('#confirm_password_msg').show()
      $("#confirm_password_msg").html('<div style="margin-top: 17px" class="alert alert-danger">Password didnot matched</div>')

      setTimeout(function() {
          $('#confirm_password_msg').fadeOut('slow');
      }, 3000);

    }

  }

  
  function validateForm() {
event.preventDefault(); // prevent form submit
var form = document.forms["myForm"]; // storing the form
swal({
       title: "Are you sure?",
       text: "Once deleted, you will not be able to recover this imaginary file!",
       icon: "warning",
       buttons: true,
       dangerMode: true,
     })
    .then((willDelete) => {
         if (willDelete) {
               form.submit();
         } else {
                swal("Your imaginary file is safe!");
     }
  });
}

$(document).ready(function() {
    $("#register-form").submit(function(event) {
        event.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            url: "/register",
            type: "POST",
            data: formData,
            success: function(response) {
                swal("Success", "Registration successful", "success");
            },
            error: function(xhr, status, error) {
                if (xhr.status == 409) {
                    swal("Error", "Email already exists", "error");
                } else {
                    swal("Error", "Registration failed", "error");
                }
            }
        });
    });
});