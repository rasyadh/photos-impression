var socket = io.connect('http://localhost:3001/adminSocket');
var id_photos = null;
var result_expression = new Array()
var hasil;
var startTime, currentTime, time;
var photos = new Array();

$(document).ready(function () {
    $('#slideshow').hide();
});

var slideindex = 0
socket.on('data', function (data) {
    currentTime = Date.now();
    time = msToSecond(currentTime - startTime);

    var json = JSON.parse(data);
    
    result = { 
        "id_photos": id_photos, 
        "time": time, 
        "expression": json[0]
    }

    if (id_photos != null) {
        result_expression.push(result);
    }
});

$('#play').click(() => {
    $('#play').hide();
    $('#slideshow').show();

    startTime = Date.now();
    carousel();
});

function msToSecond(s) {
    var ms = s % 1000;
    s = (s - ms) / 1000;

    var secs = s % 60;
    s = (s - secs) / 60;

    var mins = s % 60;
    var hrs = (s - mins) / 60;

    return secs + '.' + ms;
}

function carousel() {
    var i;
    var slide = document.getElementsByClassName("image-slide");

    for (i = 0; i < slide.length; i++) {
        slide[i].style.display = "none";
    }

    slideindex++;
    if (slideindex <= slide.length) {
        slide[slideindex - 1].style.display = "block";
        setTimeout(carousel, 2000); screenTop

        id_photos = document.getElementsByClassName("slide")[slideindex - 1].getAttribute("id")
        photos.push(id_photos)
        console.log(result_expression)
    }
    else {
        document.getElementsByClassName('video_frame').display = 'none';
        document.getElementsByClassName('video_frame').src = "";

        var data_json = JSON.stringify(result_expression);
        document.getElementById('datajson').value = data_json;
        document.getElementById('photosjson').value = JSON.stringify(photos)
        console.log(data_json)
        console.log(photos)

        swal({
            title: "Selesai",
            text: "Deteksi ekspresi wajah selesai dilakukan",
            icon: "success",
            button: "Next",
        })
            .then((value) => {
                $(document).ready(function(){
                    $('#submit').submit();
                });
            });
    }
}