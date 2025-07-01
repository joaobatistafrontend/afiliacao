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
