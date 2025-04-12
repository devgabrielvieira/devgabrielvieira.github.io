// Função debounce para evitar execução excessiva do código durante o scroll
function debounce(func, delay) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

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
const handleScroll = debounce(() => {
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        const position = section.getBoundingClientRect().top;
        if (position < window.innerHeight - 100) {
            section.classList.add('visible');
        }
    });

    // Lógica para o botão "Voltar ao Topo"
    const backToTopButton = document.getElementById('backToTop');
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none";
    }
}, 100); // Ajuste o delay conforme necessário

window.addEventListener('scroll', handleScroll);

// Botão "Topo"
document.getElementById('backToTop').addEventListener('click', function () {
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

// Fecha o lightbox ao pressionar a tecla "Esc"
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const lightbox = document.getElementById('lightbox');
        if (lightbox) {
            lightbox.remove();
        }
    }
});
