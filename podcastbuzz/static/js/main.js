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