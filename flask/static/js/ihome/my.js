function logout(e) {
    e.preventDefault();
    $.get("/house/logout/", function(data){
        if (200 == data.code) {
            location.href = "../user/login";
        }
    })
}

$(document).ready(function(){
})