document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('#ranking-list');
    const items = Array.from(container.querySelectorAll('.ranking-item'));

    // Ordenar pela quantidade de indicações (desc)
    items.sort((a, b) => {
        const aInd = parseInt(a.dataset.indications, 10);
        const bInd = parseInt(b.dataset.indications, 10);
        return bInd - aInd;
    });

    // Limpa e reanexa os itens ordenados com rank + cor
    container.innerHTML = '';

    items.forEach((item, index) => {
        const rank = index + 1;
        const rankCircle = document.createElement('div');
        rankCircle.classList.add('rank-circle');
        rankCircle.textContent = rank;

        let rankClass = '';
        if (rank === 1) {
            rankClass = 'gold';
        } else if (rank === 2) {
            rankClass = 'silver';
        } else if (rank === 3) {
            rankClass = 'bronze';
        }

        if (rankClass) {
            item.classList.add(rankClass);
        }

        item.prepend(rankCircle);
        container.appendChild(item);
    });

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
});
