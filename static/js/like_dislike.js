$('*#likebtn').on('click',function (event) {
    event.preventDefault();
    var question_id = null;
    question_id = jQuery(this).attr('q-id');

    $.ajax({
        type:'POST',
        url:'/post/likedislike/',
        data:{
            post_id: question_id,
            action:1,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function (response) {
            // console.log($("[post-rating-id="+question_id+"]").text());
            $("[post-rating-id="+question_id+"]").text(""+response)
        }
    })

});

$('*#dislikebtn').on('click',function (event) {
    event.preventDefault();
    var question_id = null;
    question_id = jQuery(this).attr('q-id');

    $.ajax({
        type:'POST',
        url:'/post/likedislike/',
        data:{
            post_id: question_id,
            action:-1,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function (response) {
            // console.log($("[post-rating-id="+question_id+"]").text());
            $("[post-rating-id="+question_id+"]").text(""+response)
        }
    })

});