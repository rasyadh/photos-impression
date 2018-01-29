let slideIndex = 0;
$('#slideshow').hide();

$(() => {
    carousel = (() => {
        let slide = $('.image-slide');

        for (let i = 0; i < slide.length; i++) {
            slide[i].style.display = 'none';
        }

        slideIndex++;
        if (slideIndex <= slide.length) {
            slide[slideIndex - 1].style.display = "block";
            setTimeout(carousel, 5000);
        }
        else {
            swal({
                title: "Selesai",
                text: "Deteksi ekspresi wajah selesai dilakukan",
                icon: "success",
                button: "Next",
            })
                .then((value) => {
                    window.location.href = '/detect_result';
                });
        }
    });

    $('#play').click(() => {
        $('#start').hide();
        $('#slideshow').show();
        carousel();
    });
});