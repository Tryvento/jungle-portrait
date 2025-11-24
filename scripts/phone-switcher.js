// Phone Carousel System
// Cycles through .phone elements and their .phone-visual children

document.addEventListener('DOMContentLoaded', () => {
    const phones = document.querySelectorAll('.phone');
    
    if (phones.length === 0) return;
    
    let currentPhoneIndex = 0;
    const phoneVisualIntervals = new Map(); // Store interval IDs for each phone
    
    // Timing configuration
    const VISUAL_SWITCH_INTERVAL = 3000; // 3 seconds per visual
    const PHONE_SWITCH_INTERVAL = 9000; // 9 seconds per phone
    
    // Initialize: hide all phones and visuals except the first
    phones.forEach((phone, phoneIndex) => {
        const visuals = phone.querySelectorAll('.phone-visual');
        
        if (phoneIndex === 0) {
            phone.classList.add('active');
            // Show first visual of first phone
            if (visuals.length > 0) {
                visuals[0].classList.add('active');
            }
        }
        
        // Hide all other visuals
        visuals.forEach((visual, visualIndex) => {
            if (phoneIndex !== 0 || visualIndex !== 0) {
                visual.classList.remove('active');
            }
        });
    });
    
    // Function to cycle through phone-visual elements within a phone
    function startVisualCycle(phone) {
        const visuals = phone.querySelectorAll('.phone-visual');
        
        if (visuals.length <= 1) return null; // No need to cycle if only one visual
        
        let currentVisualIndex = 0;
        
        const intervalId = setInterval(() => {
            // Hide current visual
            visuals[currentVisualIndex].classList.remove('active');
            
            // Move to next visual
            currentVisualIndex = (currentVisualIndex + 1) % visuals.length;
            
            // Show next visual
            visuals[currentVisualIndex].classList.add('active');
        }, VISUAL_SWITCH_INTERVAL);
        
        return intervalId;
    }
    
    // Function to switch to a specific phone
    function switchToPhone(index) {
        // Stop visual cycling for current phone
        const currentIntervalId = phoneVisualIntervals.get(currentPhoneIndex);
        if (currentIntervalId) {
            clearInterval(currentIntervalId);
            phoneVisualIntervals.delete(currentPhoneIndex);
        }
        
        // Hide current phone
        phones[currentPhoneIndex].classList.remove('active');
        
        // Reset all visuals of current phone
        const currentVisuals = phones[currentPhoneIndex].querySelectorAll('.phone-visual');
        currentVisuals.forEach(visual => visual.classList.remove('active'));
        
        // Update index
        currentPhoneIndex = index;
        
        // Show new phone
        phones[currentPhoneIndex].classList.add('active');
        
        // Show first visual of new phone
        const newVisuals = phones[currentPhoneIndex].querySelectorAll('.phone-visual');
        if (newVisuals.length > 0) {
            newVisuals[0].classList.add('active');
        }
        
        // Start visual cycling for new phone
        const newIntervalId = startVisualCycle(phones[currentPhoneIndex]);
        if (newIntervalId) {
            phoneVisualIntervals.set(currentPhoneIndex, newIntervalId);
        }
    }
    
    // Start visual cycling for the first phone
    const firstIntervalId = startVisualCycle(phones[0]);
    if (firstIntervalId) {
        phoneVisualIntervals.set(0, firstIntervalId);
    }
    
    // Start phone switching cycle
    setInterval(() => {
        const nextPhoneIndex = (currentPhoneIndex + 1) % phones.length;
        switchToPhone(nextPhoneIndex);
    }, PHONE_SWITCH_INTERVAL);
});
