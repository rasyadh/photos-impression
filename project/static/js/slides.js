let socket = io.connect('http://localhost:3001/adminSocket');
let id_photos = null;
let result_expression = new Array()
let hasil;
let startTime, currentTime, time;
let photos = new Array();

$('#slideshow').hide();

$(() => {
    $('#play').removeAttr('disabled');
    $('#play').click(() => {
        $('#play').hide();
        $('#slideshow').show();
    
        $('html, body').animate({
            scrollTop: $('#slideshow').offset().top
        }, 1);
    
        startTime = Date.now();
        carousel();
    });
});

let slideindex = 0
socket.on('data', (data) => {
    currentTime = Date.now();
    time = msToSecond(currentTime - startTime);

    let json = JSON.parse(data);

    result = {
        "id_photos": id_photos,
        "time": time,
        "expression": json[0]
    }

    if (id_photos != null) {
        result_expression.push(result);
    }
});

const msToSecond = ((s) => {
    let ms = s % 1000;
    s = (s - ms) / 1000;

    let secs = s % 60;
    s = (s - secs) / 60;

    let mins = s % 60;
    let hrs = (s - mins) / 60;

    return secs + '.' + ms;
});

const carousel = (() => {
    let i;
    let slide = document.getElementsByClassName("image-slide");

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
        $('#slides').attr('src', '');
        $('#slides').removeAttr('src');
        $('#slides').hide();

        let data_json = JSON.stringify(result_expression);
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
                $(document).ready(function () {
                    $('#submit').submit();
                });
            });
    }
});