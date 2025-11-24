/**
 * Promo Manager
 * Fetches promo data from JSON and renders it to the DOM.
 */

document.addEventListener('DOMContentLoaded', async () => {
    const promoContainer = document.querySelector('footer');
    const PROMO_DATA_URL = 'assets/data/promo.json';

    try {
        const response = await fetch(PROMO_DATA_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const promos = await response.json();

        promos.forEach(promo => {
            const promoDiv = document.createElement('div');
            promoDiv.classList.add('promo');

            if (promo.type === 'video') {
                const video = document.createElement('video');
                video.src = promo.src;
                video.alt = promo.alt;
                video.autoplay = true;
                video.loop = true;
                video.muted = true;
                promoDiv.appendChild(video);
            } else {
                const img = document.createElement('img');
                img.src = promo.src;
                img.alt = promo.alt;
                promoDiv.appendChild(img);
            }

            promoContainer.appendChild(promoDiv);
        });

        // Dispatch event to signal that promos are loaded and ready
        const event = new CustomEvent('promosLoaded');
        document.dispatchEvent(event);
        console.log('Promos loaded and rendered.');

    } catch (error) {
        console.error('Error loading promos:', error);
    }
});
