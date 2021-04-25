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

let rangeInput = document.querySelector(".range-input input");
let rangeValue = document.querySelector(".range-input .value div");
let totalValue = document.querySelector(".sliderAmount div")
 
let start = 1;
let end = parseFloat(rangeInput.max);
let step = parseFloat(rangeInput.step);
 
for(let i=start;i<=end;i+=step){
  rangeValue.innerHTML += '<div>'+"X"+i+'</div>';
}

rangeInput.addEventListener("input",function(){
  let top = ((parseFloat(rangeInput.value)/step)-1) * -40;
  rangeValue.style.marginTop = top+"px";

  totalValue.innerHTML = (rangeInput.value*0.06).toFixed(2);
});


function togglePopup(){
    popup.classList.toggle('hidden');
}