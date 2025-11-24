/**
 * Phone Manager - Loads and renders phone products dynamically
 */

class PhoneManager {
    constructor() {
        this.products = [];
        this.container = null;
    }

    /**
     * Initialize the phone manager
     */
    async init() {
        this.container = document.querySelector('.phones-container');
        if (!this.container) {
            console.error('Phones container not found');
            return;
        }

        await this.loadProducts();
        this.renderProducts();
    }

    /**
     * Load products from JSON file
     */
    async loadProducts() {
        try {
            const response = await fetch('/assets/data/products.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            this.products = data.products;
            console.log('Products loaded:', this.products);
        } catch (error) {
            console.error('Error loading products:', error);
        }
    }

    /**
     * Render all products to the DOM
     */
    renderProducts() {
        // Clear existing content
        this.container.innerHTML = '';

        // Render each product
        this.products.forEach(product => {
            const phoneElement = this.createPhoneElement(product);
            this.container.appendChild(phoneElement);
        });

        // Dispatch custom event to notify other scripts that phones are loaded
        const event = new CustomEvent('phonesLoaded', { 
            detail: { count: this.products.length } 
        });
        document.dispatchEvent(event);
        console.log('Phones rendered and event dispatched:', this.products.length);
    }

    /**
     * Create a phone element from product data
     * @param {Object} product - Product data
     * @returns {HTMLElement} - Phone element
     */
    createPhoneElement(product) {
        const phoneDiv = document.createElement('div');
        phoneDiv.className = 'phone';
        phoneDiv.dataset.productId = product.id;

        phoneDiv.innerHTML = `
            <div class="phone-visuals-container">
                <div class="phone-visual">
                    <img src="${product.images.front}" alt="${product.name} - Front">
                    <img src="${product.images.wallpaper}" alt="" class="phone-wallpaper">
                </div>
                <div class="phone-visual phone-visual-back">
                    <img src="${product.images.back}" alt="${product.name} - Back">
                </div>
            </div>
            <div class="phone-info">
                <h2>${product.name}</h2>
                <p>${product.price}</p>
            </div>
        `;

        return phoneDiv;
    }

    /**
     * Get product by ID
     * @param {string} id - Product ID
     * @returns {Object|null} - Product data or null if not found
     */
    getProductById(id) {
        return this.products.find(product => product.id === id) || null;
    }

    /**
     * Get all products
     * @returns {Array} - Array of all products
     */
    getAllProducts() {
        return this.products;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const phoneManager = new PhoneManager();
    phoneManager.init();
    
    // Make phoneManager globally accessible if needed
    window.phoneManager = phoneManager;
});
