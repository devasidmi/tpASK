$('#new_q_btn').on('click',function (event) {
    event.preventDefault();

    $.ajax({
        type:'POST',
        url:'/q/new/',
        data:{
            qfilter:'new',
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success:function (response) {
            if(response == "reload"){
                location.href = '/';
            }
        }
    });
});

$('#trend_q_btn').on('click',function (event) {
    event.preventDefault();

    $.ajax({
        type:'POST',
        url:'/q/trends/',
        data:{
            qfilter:'trend',
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success:function (response) {
            if(response == "reload"){
                location.href = "/";
            }
        }
    });
});