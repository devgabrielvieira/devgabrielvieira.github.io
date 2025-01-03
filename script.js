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

// Seleciona todas as imagens dos projetos
document.querySelectorAll('.project-item img').forEach(img => {
    img.addEventListener('click', function() {
        // Cria o lightbox e o conteúdo da imagem
        const lightbox = document.createElement('div');
        lightbox.id = 'lightbox';
        lightbox.innerHTML = `<img src="${img.src}" alt="${img.alt}">`;
        document.body.appendChild(lightbox);
        lightbox.addEventListener('click', () => {
            lightbox.remove(); // Fecha o lightbox ao clicar fora da imagem
        });
    });
});

// Fecha o lightbox ao clicar no botão de fechar
document.getElementById('close-lightbox').addEventListener('click', () => {
    document.getElementById('lightbox').remove();
});
