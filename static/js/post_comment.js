$('#post-comment-form').on('submit',function (event) {
    event.preventDefault();
    $.ajax({
        type:'POST',
        url:'/comment_POST/',
        data:{
            post_id_data: window.location.pathname,
            comment_text: $('#comment_text').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success:function (response) {
            if(response == 200) {
                location.reload();
            }
        }
    })
})