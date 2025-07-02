document.addEventListener('DOMContentLoaded', () => {
    // ===== BOTÃO COPIAR LINK DE INDICAÇÃO =====
    const shareLinkButton = document.querySelector('.share-link-button');
    if (shareLinkButton) {
        shareLinkButton.addEventListener('click', () => {
            const dummyLink = shareLinkButton.getAttribute("data-link");
            navigator.clipboard.writeText(dummyLink).then(() => {
                const originalHTML = shareLinkButton.innerHTML;
                shareLinkButton.textContent = 'Copiado!';
                shareLinkButton.classList.add('copied');
                setTimeout(() => {
                    shareLinkButton.innerHTML = originalHTML;
                    shareLinkButton.classList.remove('copied');
                }, 2000);
            }).catch(err => {
                console.error('Erro ao copiar link: ', err);
                alert('Não foi possível copiar o link. Tente manualmente: ' + dummyLink);
            });
        });
    }

});



document.getElementById('download-qr-btn').addEventListener('click', function() {
    const link = document.createElement('a');
    link.href = "{{ qrcode.url }}";
    link.download = "qr_{{ request.user.username }}.png";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});
// Exibe o hamburger no mobile
function toggleMenu() {
    document.querySelector('.main-nav').classList.toggle('active');
    document.getElementById('hamburger-menu').classList.toggle('active');
    document.body.classList.toggle('no-scroll');
}
document.getElementById('hamburger-menu').addEventListener('click', toggleMenu);

// Fecha o menu ao clicar em um link (opcional)
document.querySelectorAll('.main-nav a').forEach(link => {
    link.addEventListener('click', function() {
        document.querySelector('.main-nav').classList.remove('active');
        document.getElementById('hamburger-menu').classList.remove('active');
        document.body.classList.remove('no-scroll');
    });
});

// Mostra o hamburger só em telas pequenas
function checkHamburger() {
    if(window.innerWidth <= 991) {
        document.getElementById('hamburger-menu').style.display = 'flex';
    } else {
        document.getElementById('hamburger-menu').style.display = 'none';
        document.querySelector('.main-nav').classList.remove('active');
        document.getElementById('hamburger-menu').classList.remove('active');
        document.body.classList.remove('no-scroll');
    }
}
window.addEventListener('resize', checkHamburger);
window.addEventListener('DOMContentLoaded', checkHamburger);
