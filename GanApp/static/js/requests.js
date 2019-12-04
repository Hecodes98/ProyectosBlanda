$(function(){

    function send_image(){
        var canvas = $("#realCanvas");
        var dataURL = canvas[0].toDataURL("image/jpg");
        //console.log(dataURL);

        $.ajax({
            type: 'POST',
            url: '/image',
            data: {
                imgBase64: dataURL
            },
            success: function(response){
                //console.log(response);
                if(response!="false")
                    $("#generated_image").attr("src", response);
            },
            error: function(error){
                console.log(error);
            }
        });
    }

    setInterval(send_image, 1000)

});
