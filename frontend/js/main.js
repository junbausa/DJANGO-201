$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;


            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');

                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);

                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }

            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});

$(document)
    .on("click", '.js-toggle-modal', function(e){
        e.preventDefault()
        
        // This is for the modal popping up
        const $post = $(".js-modal") 
        $post.toggleClass("hidden")
    })

    .on("click", '.js-submit', function(e){
        e.preventDefault()

        const $text = $(".js-post-text").val().trim()
        const $btn = $(this)

        if(!$text.length) {
            return false
        }
        
        $btn.prop("disabled", true).text("Posting!")

        // Sample Ajax post request
        $.ajax({
            type: 'POST',
            // from text-area in html with class data-post-url and jst-post-text
            url: $(".js-post-text").data("post-url"),
            data: {
            // actual data mapping key values vs table values in django model                
                text: $text
            },
            // what happens after AJAX Post request
            success: (dataHtml) => {
                $(".js-modal").addClass("hidden");
                $("#posts-container").prepend(dataHtml);
                $btn.prop("disabled", false).text("New Post");
                $(".js-post-text").val('')
            },
            // what happens when error
            error: (error) => {
                console.warn(error)
                $btn.prop("disabled", false).text("Error");
            }
        });
        
    })

    .on("click", '.js-follow', function(e){
        e.preventDefault()

        const $action = $(this).attr("data-action")

        // Sample Ajax post request
        $.ajax({
            type: 'POST',
            // from text-area in html with class data-post-url and jst-post-text
            url: $(this).data("url"),
            data: {
            // actual data mapping key values vs table values in django model                
                // .data() will not work is cached in ajax
                // action: $(".js-follow").data("action"),
                action: $action,
                username: $(this).attr("data-username")
            },
            // what happens after AJAX Post request
            success: (data) => {
                $(".js-follow-text").text(data.wording)
                if ($action == "follow"){
                    $(this).attr("data-action", "unfollow")
                } else {
                    $(this).attr("data-action", "follow")
                }

            },
            // what happens when error
            error: (error) => {
                console.warn(error) 
            }
        });
        
    })