// Debounce para scroll
function debounce(func, delay) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

// Menu mobile
const navToggle = document.querySelector('.nav-toggle');
const mainNav = document.querySelector('.main-nav');
if (navToggle && mainNav) {
    navToggle.addEventListener('click', () => {
        mainNav.classList.toggle('open');
        const icon = navToggle.querySelector('i');
        if (icon) {
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-xmark');
        }
    });
    mainNav.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', () => mainNav.classList.remove('open'));
    });
}

// Scroll suave seguro - previne open redirect e valida alvo
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (!targetId || targetId === '#' || targetId.length > 100) return;
        if (!/^#[a-zA-Z0-9_-]+$/.test(targetId)) return;
        const target = document.querySelector(targetId);
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
});

// Animação de seções + backToTop
const handleScroll = debounce(() => {
    const sections = document.querySelectorAll('.section, .hero');
    sections.forEach(section => {
        const position = section.getBoundingClientRect().top;
        if (position < window.innerHeight - 80) {
            section.classList.add('visible');
        }
    });
    const backToTopButton = document.getElementById('backToTop');
    if (!backToTopButton) return;
    if (document.documentElement.scrollTop > 320) {
        backToTopButton.classList.add('show');
    } else {
        backToTopButton.classList.remove('show');
    }
}, 80);

window.addEventListener('scroll', handleScroll);
window.addEventListener('load', handleScroll);
handleScroll();

// Botão topo
const backBtn = document.getElementById('backToTop');
if (backBtn) {
    backBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

// Ofuscação de e-mail (P2) e avatar fallback sem inline JS (CSP-safe)
(function initObfuscatedEmail(){
    const enc = "Z2FicmllbF9iYXJkb0Bob3RtYWlsLmNvbQ==";
    let email = "";
    try { email = atob(enc); } catch(e) { return; }
    document.querySelectorAll('.obfuscated-email').forEach(el => {
        el.setAttribute('href', 'mailto:' + email);
        const txt = el.querySelector('.email-text');
        if (txt) txt.textContent = email;
        else {
            // fallback se não houver span
            const last = el.lastChild;
            if (last && last.nodeType === 3) last.textContent = email;
        }
    });
    // expõe para uso no form mailto
    window.__contactEmail = email;
})();
(function initAvatarFallback(){
    const img = document.getElementById('heroAvatar');
    const fallback = document.getElementById('avatarFallback');
    if (img && fallback) {
        img.addEventListener('error', () => {
            img.style.display = 'none';
            fallback.style.display = 'grid';
        });
    }
})();

// Tema escuro / claro - validação estrita
(function initTheme(){
    const html = document.documentElement;
    const btn = document.getElementById('themeToggle');
    const stored = localStorage.getItem('theme');
    const isValidTheme = (v) => v === 'dark' || v === 'light';
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initial = isValidTheme(stored) ? stored : (prefersDark ? 'dark' : 'light');
    html.setAttribute('data-theme', initial);
    updateIcon(initial);
    if (btn) {
        btn.addEventListener('click', () => {
            const current = html.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
            const next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            updateIcon(next);
        });
    }
    function updateIcon(theme){
        if (!btn) return;
        const icon = btn.querySelector('i');
        if (!icon) return;
        icon.className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
        btn.setAttribute('aria-label', theme === 'dark' ? 'Alternar para modo claro' : 'Alternar para modo escuro');
        btn.title = theme === 'dark' ? 'Mudar para modo claro' : 'Mudar para modo escuro';
    }
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            if (localStorage.getItem('theme')) return;
            const next = e.matches ? 'dark' : 'light';
            html.setAttribute('data-theme', next);
            updateIcon(next);
        });
    }
})();

// Form oculto - mantido para CSP-safe via addEventListener (validação e sanitização)
(function initContactForm(){
    const form = document.getElementById('contactForm');
    if (!form) return;
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const nome = (form.nome?.value || '').trim().slice(0, 100);
        const email = (form.email?.value || '').trim().slice(0, 100);
        const assunto = (form.assunto?.value || '').trim().slice(0, 80) || 'Contato via portfolio - Modern Workplace';
        const mensagem = (form.mensagem?.value || '').trim().slice(0, 1000);
        const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        if (!emailValid) {
            alert('Por favor, informe um e-mail válido.');
            return;
        }
        if (mensagem.length < 10) {
            alert('Mensagem muito curta.');
            return;
        }
        // limites endurecidos P2: 1000 chars mensagem, 80 assunto
        const body = `Olá Gabriel,%0D%0A%0D%0A${encodeURIComponent(mensagem.slice(0,1000))}%0D%0A%0D%0A---%0D%0ANome: ${encodeURIComponent(nome)}%0D%0AE-mail: ${encodeURIComponent(email)}`;
        const subject = encodeURIComponent(`[Portfolio] ${assunto.slice(0,80)} - ${nome.slice(0,40)}`);
        const dest = window.__contactEmail || atob("Z2FicmllbF9iYXJkb0Bob3RtYWlsLmNvbQ==");
        window.location.href = `mailto:${dest}?subject=${subject}&body=${body}`;
    });
})();
