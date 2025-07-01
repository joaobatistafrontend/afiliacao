document.addEventListener('DOMContentLoaded', () => {

    // Hamburger menu toggle
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const mainNav = document.querySelector('.main-nav');

    if (hamburgerMenu && mainNav) {
        hamburgerMenu.addEventListener('click', () => {
            hamburgerMenu.classList.toggle('active');
            mainNav.classList.toggle('active');
            document.body.classList.toggle('no-scroll');
        });

        mainNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                hamburgerMenu.classList.remove('active');
                mainNav.classList.remove('active');
                document.body.classList.remove('no-scroll');
            });
        });
    }
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