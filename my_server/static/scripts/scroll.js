const translate = document.querySelectorAll(".translate");
const shadow = document.querySelector(".shadow");
const section = document.querySelector("section");
const opacity = document.querySelectorAll(".opacity");
let section_height = section.offsetHeight;
var x = window.matchMedia("(max-width: 1000px)");
const popup = document.querySelector('.full-screen');

if(x.matches) {
    $('.timeline').height($(this).data('done') + "%");
} else {
    $('.timeline').width($(this).data('done') + "%");
}
$('.timeline').css('opacity', '1');

window.addEventListener('scroll', () => {
    let scroll = window.pageYOffset;
    let sectionY = section.getBoundingClientRect();
    
    translate.forEach(element => {
        let speed = element.dataset.speed;
        element.style.transform = x.matches ? `translate(-38%, ${scroll * speed}px)` : `translateY(${scroll * speed}px)`;
    });

    opacity.forEach(element => {
        element.style.opacity = scroll / (sectionY.top+ section_height);
    })
})


function togglePopup(){
    popup.classList.toggle('hidden');
}