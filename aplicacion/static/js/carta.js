const menuHamburger = document.querySelector(".menu-hamburgesa");
const navLinks = document.querySelector(".nav-links");




menuHamburger.addEventListener('click', () =>{
    navLinks.classList.toggle('mobile-menu')
})

window.addEventListener("scroll", function(){
    const scrollNav = this.document.querySelector("nav");
    scrollNav.classList.toggle("abajo",window.scrollY>0);
})


$(document).ready(function () {
    const apiUrl = 'https://api.waifu.im/search';
    $.getJSON(apiUrl, function () {
       console.log("Esperando datos...");
    }
    ).fail(function () {
        console.log("Watioooo!!!");

    }).done(function (data) {
        
        let imagen = data.images[0].url
        
        $("#foto-waifu").attr("src", imagen)
        
    });
});
