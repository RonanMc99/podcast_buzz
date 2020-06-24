function searchResult() {
    let query = document.getElementById("search_query");
    if (query.value == "") {
        alert("Nothing to search!");
        query.focus();
        return false;
    } else {
        document.getElementById('response-id').innerHTML = "";
        let queryUrl = "http://localhost:5000/search?q=" + query.value;
        $.ajax({
            url: queryUrl,
            type: 'GET',
            dataType: 'json',
            success: function (res) {
                let count = res.count;
                for (let index = 0; index < count; index++) {
                    let title = res.results[index].podcast_title_original;
                    let description = res.results[index].description_original;
                    let image = res.results[index].image;
                    let infoUrl = res.results[index].info_url;
                    let html = '<div class="row" style="margin-top:10px" >'
                        + '<div class="col-lg-3">'
                        + '<a class="link-class" href="' + infoUrl + '"><img src="' + image + '"  alt="as" width="200" height="200px"></a>'
                        + '</div>'
                        + '<div class="col-lg-8">'
                        + '<a class="link-class" href="' + infoUrl + '"><h3>' + title + '</h3></a>'
                        + '<h6>' + description + ' </h6>'
                        + ' </div>'
                        + '</div>'
                    $("#response-id").append(html);
                }
            }
        });
    }
}


function addComment() {
    let userId = document.getElementById("user-id");
    let podcastId = document.getElementById("podcast-id");
    let addComment = document.getElementById("add-comment");

    // check to see if a comment has contents, else create it
    if($("add-comment").val().trim().length < 1){
        alert("Add your comment first");
        addComment.focus();
    }else{ 
        userId = userId.innerHTML;
        podcastId = podcastId.innerHTML;
        addComment = addComment.value;

        let data = {
            "user_id": userId,
            "podcast_id": podcastId,
            "comment_text": addComment
        };

        let settings = {
            "url": "http://localhost:5000/add_comment",
            "method": "POST",
            "timeout": 0,
            "headers": {
                "Content-Type": "application/javascript"
            },
            "data": JSON.stringify(data)
        };
        // Use request to build comment
        $.ajax(settings).done(function (response) {
            let check = response.status;
            let date = response.date;
            let text = response.text;
            let user_name = response.user_name;

            if(check == "200"){
                let html = '<div class="container">'
                    + '<div class="row"><h5> Username:' + user_name + ' </h5></div>'
                    + '<div class="row"><h5> Comment:' + text + ' </h5></div>'
                    + '<div class="row"><h5> Date: ' + date + ' </h5></div>'
                    + '</div>';
                $("#comments-div").append(html);
                document.getElementById("add-comment").value = "";
                alert("Thanks for your comment!");
            }else{
                alert('An error occurred. Please try again');
            }
        });
    }
}