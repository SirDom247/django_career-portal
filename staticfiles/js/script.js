// header

bar.onclick = (e) => {
    const currentClass = bar.classList.contains("fa-bars") ? "fa-bars" : "fa-xmark";
    const newClass = currentClass === "fa-bars" ? "fa-xmark" : "fa-bars";
    bar.classList.replace(currentClass, newClass);
    nav.classList.toggle("showNav");
};


// const bar = document.getElementById("bar");
// const nav = document.getElementById("nav");

// bar.onclick = (e) => {
//     const icon = e.target.getAttribute("class")
//     if(icon == "fa-solid fa-bars"){
//         e.target.setAttribute("class","fa-solid fa-xmark")

//     }else{
//         e.target.setAttribute("class","fa-solid fa-bars")
//     }
//     nav.classList.toggle("showNav")
// }


// carousel
const carouselContainer = document.querySelector(".carouselContainer");
const eachCarousel = document.querySelector(".eachCarousel").clientWidth;
const allEachCarousel = document.querySelectorAll(".eachCarousel");
const allIndicator = document.querySelectorAll(".indicator");

const slideCarousel = (index) => {
    for(let x = 0; x<allEachCarousel.length;x++){
        if(x === index){
            allEachCarousel[x].classList.add("eachCarouselBorder")
            allIndicator[x].classList.add("activeIndicator")
        }else{
            allEachCarousel[x].classList.remove("eachCarouselBorder")
            allIndicator[x].classList.remove("activeIndicator")
        }
    }
   carouselContainer.scrollLeft = (index * (eachCarousel + 10))
   console.log(carouselContainer.scrollLeft)
}


// // JavaScript for Dropdown Menu
// document.querySelectorAll('.dropdown-link').forEach(dropdown => {
//     dropdown.addEventListener('click', function (e) {
//         e.preventDefault();
//         const menu = this.nextElementSibling;
//         menu.classList.toggle('hidden');
//     });
// });

// // JavaScript for Carousel Functionality
// let currentSlide = 0;
// const slides = document.querySelectorAll('.eachCarousel');
// const indicators = document.querySelectorAll('.indicator');

// function updateCarousel() {
//     slides.forEach((slide, index) => {
//         slide.style.display = index === currentSlide ? 'block' : 'none';
//     });

//     indicators.forEach((indicator, index) => {
//         indicator.classList.toggle('activeIndicator', index === currentSlide);
//     });
// }

// function slideCarousel(slideIndex) {
//     currentSlide = slideIndex;
//     updateCarousel();
// }

// // Auto-rotate Carousel
// setInterval(() => {
//     currentSlide = (currentSlide + 1) % slides.length;
//     updateCarousel();
// }, 5000); // Change slide every 5 seconds

// // Initialize Carousel
// updateCarousel();

// // JavaScript for Mobile Menu Toggle
// const bar = document.getElementById('bar');
// const nav = document.getElementById('nav');

// bar.addEventListener('click', () => {
//     nav.classList.toggle('hidden');
// });
