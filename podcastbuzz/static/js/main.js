// search function
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

// add comment function
function addComment() {
    let userId = document.getElementById("user-id");
    let podcastId = document.getElementById("podcast-id");
    let thisComment = document.getElementById("add-comment");

    // check to see if a comment has contents, else create it
    if($("#add-comment").val().trim().length < 1){
        alert("Add your comment first");
        thisComment.focus();
    }else{ 
        userId = userId.innerHTML;
        podcastId = podcastId.innerHTML;
        thisComment = thisComment.value;

        let data = {
            "user_id": userId,
            "podcast_id": podcastId,
            "comment_text": thisComment
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
            let c_id = response.commentID;
            // build the comment HTML
            if(check == "200"){
                let html = '<div  style="border: 2px #2e284f; padding:20px 30px; margin-top:10px ; "id="div_' + c_id + '">'
                    + '<div class="row"><h5> Username:' + user_name + ' </h5></div> '
                    + '<div class="row"> <h5> Comment: <span id="c_' + c_id + '">' + text + ' </h5></div> '
                    + '<div class="row"><h5> Date: ' + date + '</h5></div> '
                    + '<div class="row">'
                    + '<div><button onclick="getComment(this)" class="form-control" id="' + c_id + '"'
                    + 'style="background-color: #001539;color:#f2e4e5 ;border-radius: 50px;"'
                    + 'data-toggle="modal" data-target="#myModal">Edit</button>'
                    + '<button onclick="deleteComment(this)" class="form-control" id="' + c_id + '"'
                    + 'style="background-color: #001539;color:#f2e4e5 ;border-radius: 50px;">Delete</button>'
                    + '</div>'
                    + '</div>'
                    + '<div class="modal fade" id="myModal" role="dialog">'
                    + '<div class="modal-dialog">'
                    + '<!-- Modal content-->'
                    + '<div class="modal-content">'
                    + '<div class="modal-header">'
                    + '<button type="button" class="close" data-dismiss="modal">&times;</button>'
                    + '</div>'
                    + '<div class="modal-body">'
                    + '<textarea class="form-control" id="edit-comment-textarea-id"></textarea>'
                    + '</div>'
                    + '<div class="modal-footer">'
                    + '<button class="btn btn-info" onclick="editComment(this)" id="' + c_id + '">Edit</button>'
                    + '</div>'
                    + '</div>'
                    + '</div>'
                    + '</div>'
                    + '</div>';
                $("#comments-container").append(html);
                document.getElementById("add-comment").value = "";
                alert("Thanks for your comment!");
            }else{
                alert('An error occurred. Please try again');
            }
        });
    }
}

// delete comment function
function deleteComment(e) {
    let commentId = e.id;
    let divId = "div_" + e.id;
    let div1 = document.getElementById(divId);
    let confirmation = confirm("Are you sure you want to delete this comment?");
    if (confirmation) {
        let data = {
            "commentId": commentId
        }
        let settings = {
            "url": "http://localhost:5000/delete_comment",
            "method": "POST",
            "timeout": 0,
            "headers": {
                "Content-Type": "application/javascript"
            },
            "data": JSON.stringify(data)
        };
        $.ajax(settings).done(function (response) {
            console.log(response);
            console.log(divId)
            div1.parentNode.removeChild(div1);
        });
    } else {
        return false;
    }
}

// get comment function
function getComment(e) {
    let commentId = e.id;
    let oldComment = document.getElementById("c_" + commentId).innerHTML;
    document.getElementById("edit-comment-textarea-id").value = oldComment;
}

// edit comment function
function editComment(e) {
    let commentId = e.id;
    let newComment = document.getElementById("edit-comment-textarea-id").value;
    let data = {
        "commentId": commentId,
        "text": newComment
    }
    let settings = {
        "url": "http://localhost:5000/edit_comment",
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/javascript"
        },
        "data": JSON.stringify(data)
    };
    $.ajax(settings).done(function (response) {
        console.log(response);
        location.reload();
    });
}