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
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        const position = section.getBoundingClientRect().top;
        if (position < window.innerHeight - 100) { // Ajustado para um efeito mais suave
            section.classList.add('visible');
        }
    });
});

// Botão "Topo"
const backToTopButton = document.getElementById('backToTop');

window.addEventListener('scroll', function () {
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none";
    }
});

backToTopButton.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Seleciona todas as imagens dos projetos
document.querySelectorAll('.project-item img').forEach(img => {
    img.addEventListener('click', function () {
        // Cria o lightbox e o conteúdo da imagem
        const lightbox = document.createElement('div');
        lightbox.id = 'lightbox';
        lightbox.innerHTML = `
            <div id="lightbox-content">
                <img src="${img.src}" alt="${img.alt}">
                <button id="close-lightbox">Fechar</button>
            </div>
        `;
        document.body.appendChild(lightbox);
        
        // Adiciona a funcionalidade de fechar ao clicar fora da imagem
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) {
                lightbox.remove(); // Fecha o lightbox ao clicar fora da imagem
            }
        });
        
        // Fecha o lightbox ao clicar no botão de fechar
        document.getElementById('close-lightbox').addEventListener('click', () => {
            lightbox.remove();
        });
    });
});
