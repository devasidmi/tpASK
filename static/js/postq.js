$('#ask_form').on('submit',function (event) {
    event.preventDefault()
    $.ajax({
        type:'POST',
        url:"/question/post/",
        data:{
            title:$('#title_input').val(),
            text:$('#text_input').val(),
            tags:$('#tags_input').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function (response) {
            if(response == 200) {
                location.href = "/";
            }
        }
    })
});