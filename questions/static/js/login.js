$('#sign_in_form').on('submit',function (event) {
    event.preventDefault();
    // $('#sign_in_form').validate({
    //     login_input:  {
    //         required:true,
    //     }
    // })
    $.ajax({
        type: 'POST',
        url: '/sign_in/',
        data:{
            login:$('#login_input').val(),
            password:$('#password_input').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success:function (response) {
            if(response == 200) {
                location.href = "/";
            }
        }
    })
});