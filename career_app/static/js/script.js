 // header
// Select the services menu and its submenu
const servicesMenu = document.querySelector('.services-menu'); // Main services menu
const servicesSubMenu = document.querySelector('.services-submenu'); // Submenu under services

// Function to show submenu on hover
servicesMenu.addEventListener('mouseover', () => {
  servicesSubMenu.style.display = 'block'; // Show submenu
});

// Function to hide submenu when not hovered
servicesMenu.addEventListener('mouseout', () => {
  servicesSubMenu.style.display = 'none'; // Hide submenu
});

// Additional safety for submenu itself to keep it visible when hovered
servicesSubMenu.addEventListener('mouseover', () => {
  servicesSubMenu.style.display = 'block'; // Keep submenu visible
});

servicesSubMenu.addEventListener('mouseout', () => {
  servicesSubMenu.style.display = 'none'; // Hide submenu when mouse leaves
});

// carousel
const bar = document.getElementById("bar");
const nav = document.getElementById("nav");

bar.onclick = (e) => {
    const icon = e.target.getAttribute("class")
    if(icon == "fa-solid fa-bars"){
        e.target.setAttribute("class","fa-solid fa-xmark")

    }else{
        e.target.setAttribute("class","fa-solid fa-bars")
    }
    nav.classList.toggle("showNav")
}


// carousel

const slideCarousel = (index) => {
    allEachCarousel.forEach((carousel, x) => {
        if (x === index) {
            carousel.classList.add("eachCarouselBorder");
            allIndicator[x].classList.add("activeIndicator");
        } else {
            carousel.classList.remove("eachCarouselBorder");
            allIndicator[x].classList.remove("activeIndicator");
        }
    });

    // Calculate the gap dynamically (if applicable)
    const gap = parseInt(getComputedStyle(carouselContainer).gap) || 0;
    carouselContainer.scrollLeft = index * (eachCarousel + gap);
};
