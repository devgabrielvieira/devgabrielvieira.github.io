// Scroll suave ao clicar nos links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Animação ao rolar para tornar as seções visíveis
window.addEventListener('scroll', function () {
    const sections = document.querySelectorAll('section'); // ajustado para selecionar diretamente todas as seções
    sections.forEach(section => {
        const position = section.getBoundingClientRect().top;
        if (position < window.innerHeight) {
            section.classList.add('visible');
        }
    });
});

// Botão "Topo"
const backToTopButton = document.getElementById('backToTop');

window.onscroll = function () {
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none";
    }
};

backToTopButton.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
