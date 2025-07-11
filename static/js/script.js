document.addEventListener('DOMContentLoaded', () => {
    const rankingData = [
        { name: "Bianca Silva", indications: 705 },
        { name: "Letícia Souza", indications: 663 },
        { name: "Wesdenis Santos", indications: 640 },
        { name: "Carlos Pereira", indications: 590 },
        { name: "Ana Rodrigues", indications: 540 },
        { name: "Lucas Fernandes", indications: 480 },
        { name: "Mariana Costa", indications: 450 },
        { name: "Rafael Almeida", indications: 410 },
        { name: "Julia Carvalho", indications: 390 },
        { name: "Pedro Rocha", indications: 350 },
        { name: "Sofia Gomes", indications: 320 }
    ];

    const rankingListContainer = document.querySelector('main .main-content');

    const hamburgerMenu = document.querySelector('.hamburger-menu');
    // Selecting the main nav element, which now functions as the universal menu
    const mainNav = document.querySelector('.main-nav');

    // Populate ranking list
    rankingData.forEach((player, index) => {
        const rank = index + 1;
        const rankingItem = document.createElement('div');
        rankingItem.classList.add('ranking-item');

        let rankClass = '';
        if (rank === 1) {
            rankClass = 'gold';
        } else if (rank === 2) {
            rankClass = 'silver';
        } else if (rank === 3) {
            rankClass = 'bronze';
        }

        if (rankClass) {
            rankingItem.classList.add(rankClass);
        }

        rankingItem.innerHTML = `
            <div class="rank-circle">${rank}</div>
            <div class="user-info">
                <h3>${player.name}</h3>
                <p>${player.indications} indicações</p>
            </div>
        `;
        rankingListContainer.appendChild(rankingItem);
    });

    // Hamburger menu toggle functionality
    if (hamburgerMenu && mainNav) { // Ensure elements exist before adding event listeners
        hamburgerMenu.addEventListener('click', () => {
            hamburgerMenu.classList.toggle('active');
            mainNav.classList.toggle('active');
            document.body.classList.toggle('no-scroll'); // Optional: Disable body scroll when menu is open
        });

        // Close mainNav when a link is clicked (or anywhere outside, if you add an overlay)
        mainNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                hamburgerMenu.classList.remove('active');
                mainNav.classList.remove('active');
                document.body.classList.remove('no-scroll');
            });
        });
    }
});

/* Optional CSS for no-scroll class (add this to style.css if you want to prevent body scroll) */
/*
.no-scroll {
    overflow: hidden;
}
*/