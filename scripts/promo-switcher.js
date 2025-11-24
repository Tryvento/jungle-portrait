// Social Media Carousel System
// Cycles through .promo elements

document.addEventListener('promosLoaded', () => {
    const promoItems = document.querySelectorAll('.promo');
    
    if (promoItems.length === 0) return;
    
    let currentIndex = 0;
    
    // Timing configuration
    const PROMO_SWITCH_INTERVAL = 3000; // 3 seconds per promo
    const VIDEO_EXTRA_DURATION = 10000; // 10 seconds extra for videos
    
    // Initialize: hide all promo items except the first
    promoItems.forEach((item, index) => {
        if (index === 0) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });

    // Function to schedule the next switch
    function scheduleNextSwitch() {
        const currentItem = promoItems[currentIndex];
        const isVideo = currentItem.querySelector('video') !== null;
        
        let duration = PROMO_SWITCH_INTERVAL;
        if (isVideo) {
            duration += VIDEO_EXTRA_DURATION;
            
            // Optional: If it's a video, we might want to ensure it plays
            const video = currentItem.querySelector('video');
            if (video) {
                video.currentTime = 0;
                video.play().catch(e => console.log('Autoplay prevented:', e));
            }
        }
        
        setTimeout(switchToNext, duration);
    }
    
    // Function to switch to next promo item
    function switchToNext() {
        // Hide current item
        const currentItem = promoItems[currentIndex];
        currentItem.classList.remove('active');
        
        // Pause video if current item was a video
        const currentVideo = currentItem.querySelector('video');
        if (currentVideo) {
            currentVideo.pause();
        }
        
        // Move to next item
        currentIndex = (currentIndex + 1) % promoItems.length;
        
        // Show next item
        promoItems[currentIndex].classList.add('active');
        
        // Schedule next switch
        scheduleNextSwitch();
    }
    
    // Start promo switching cycle
    scheduleNextSwitch();
});
