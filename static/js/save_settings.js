$('#settings-form').on('submit',function (event) {
    event.preventDefault();
    $.ajax({
        type:'POST',
        url:'/save_settings/',
        data:{
            login:$('#login_input').val(),
            email:$('#email_input').val(),
            nickname:$('#nick_input').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success:function (response) {
            if(response == 200) {
                location.href = "/settings/";
            }
        }

    })
});