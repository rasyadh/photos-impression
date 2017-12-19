var slideIndex = 1;
showSlides(slideIndex);

function nextSlide(index) {
    showSlides(slideIndex += index);
}

function showSlides(slideIndex) {
    var i;
    var slides = document.getElementsByClassName("image-slide");
    var next = document.getElementById("next");

    if (slideIndex == slides.length) {
        next.innerHTML = "Finish";
    }

    if (slideIndex > slides.length) {
        next.classList.add('disabled');
        alert("Facial expression detection complete");
        window.location.href = '/detect_result';
    }

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }

    slides[slideIndex-1].style.display = "block"; 
}