$(function () {
    var $username = $("#username_input");
    $username.change(function () {
        var username = $username.val().trim();
        if (username.length) {
            $.getJSON('/axf/checkuser/', {'username': username}, function (data) {
                console.log(data);

                var $username_info = $("#username_info");
                if (data['status'] ===200){
                    $username_info.html('用户名可用').css('color','green');
                }else if(data['status']===901){
                    $username_info.html('用户名已存在或不可用').css('color','red');
                }

            })
        }
    })

})

function check() {
    var $username = $("#username_input");
    var username = $username.val().trim();
    if (!username){
        return false
    }
    var $info_color = $("#username_info").css('color');
    console.log($info_color);
    if ($info_color == 'rgb(255,0,0)'){
        return false
    }

    var $password_input = $("#password_input");
    var password = $password_input.val().trim();
    $password_input.val(md5(password));

    return true
}