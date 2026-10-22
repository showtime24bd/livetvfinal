// ============================================================
// MOBILE PERFORMANCE OPTIMIZATION
// ============================================================

(function() {
    'use strict';
    
    // Detect if mobile device
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const isLowEndDevice = navigator.hardwareConcurrency <= 4 || navigator.deviceMemory <= 2;
    
    // Apply mobile-specific optimizations
    if (isMobile || isLowEndDevice) {
        document.documentElement.classList.add('mobile-optimized');
        
        // Disable expensive animations on low-end devices
        if (isLowEndDevice) {
            document.documentElement.classList.add('reduce-animations');
        }
    }
    
    // ============================================================
    // 1. LAZY LOADING IMAGES
    // ============================================================
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                const src = img.dataset.src || img.src;
                
                if (img.dataset.src) {
                    img.src = src;
                    img.removeAttribute('data-src');
                }
                
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    }, {
        rootMargin: '50px 0px',
        threshold: 0.01
    });
    
    // Observe all images
    function observeImages() {
        document.querySelectorAll('img[loading="lazy"]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // ============================================================
    // 2. DEBOUNCE SCROLL EVENTS
    // ============================================================
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // ============================================================
    // 3. REDUCE CAROUSEL ANIMATIONS ON MOBILE
    // ============================================================
    
    if (isMobile) {
        // Disable auto-scroll on mobile to save battery
        const style = document.createElement('style');
        style.textContent = `
            .carousel-track {
                transition: transform 0.3s ease !important;
            }
            
            .channel-card,
            .featured-sports-card {
                transition: transform 0.2s ease !important;
            }
            
            /* Disable expensive 3D transforms on mobile */
            .featured-sports-card {
                transform: none !important;
            }
            
            /* Reduce shadow complexity */
            .channel-card:hover,
            .featured-sports-card:hover {
                box-shadow: 0 4px 12px rgba(0,0,0,.4) !important;
            }
        `;
        document.head.appendChild(style);
    }
    
    // ============================================================
    // 4. OPTIMIZE CAROUSEL FOR MOBILE
    // ============================================================
    
    function optimizeCarousel() {
        const carousel = document.getElementById('sportsCarousel');
        if (!carousel || !isMobile) return;
        
        // Disable auto-scroll interval on mobile
        if (window.autoScrollInterval) {
            clearInterval(window.autoScrollInterval);
        }
        
        // Use passive event listeners for better scroll performance
        const carouselContainer = carousel.parentElement;
        if (carouselContainer) {
            carouselContainer.addEventListener('touchstart', function(e) {
                this.dataset.touchStart = e.touches[0].clientX;
            }, { passive: true });
            
            carouselContainer.addEventListener('touchmove', function(e) {
                // Allow native scrolling
            }, { passive: true });
        }
    }
    
    // ============================================================
    // 5. DEFER NON-CRITICAL SCRIPTS
    // ============================================================
    
    function deferNonCritical() {
        // Defer heavy animations until page is fully loaded
        if (document.readyState === 'complete') {
            enableAnimations();
        } else {
            window.addEventListener('load', enableAnimations);
        }
    }
    
    function enableAnimations() {
        // Delay enabling animations by 500ms after load
        setTimeout(() => {
            document.body.classList.add('animations-ready');
        }, 500);
    }
    
    // ============================================================
    // 6. REDUCE INTERSECTION OBSERVER FREQUENCY
    // ============================================================
    
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: isMobile ? 0.05 : 0.1,
        rootMargin: isMobile ? '100px 0px' : '50px 0px'
    });
    
    // ============================================================
    // 7. OPTIMIZE CHANNEL GRID RENDERING
    // ============================================================
    
    function optimizeChannelGrid() {
        const grid = document.getElementById('channelsGrid');
        if (!grid) return;
        
        // Use requestAnimationFrame for smooth rendering
        const cards = grid.querySelectorAll('.channel-card');
        
        if (isMobile && cards.length > 20) {
            // Virtual scrolling for large lists on mobile
            let visibleCards = new Set();
            
            const gridObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        visibleCards.add(entry.target);
                        entry.target.classList.add('visible');
                        entry.target.style.visibility = 'visible';
                    } else {
                        visibleCards.delete(entry.target);
                        // Keep rendered but make invisible to save GPU
                        if (visibleCards.size > 30) {
                            entry.target.style.visibility = 'hidden';
                        }
                    }
                });
            }, {
                rootMargin: '200px 0px'
            });
            
            cards.forEach(card => gridObserver.observe(card));
        } else {
            // Normal observation for smaller lists
            cards.forEach(card => cardObserver.observe(card));
        }
    }
    
    // ============================================================
    // 8. THROTTLE RESIZE EVENTS
    // ============================================================
    
    const throttledResize = debounce(() => {
        // Recalculate layouts only when needed
        optimizeChannelGrid();
    }, 250);
    
    window.addEventListener('resize', throttledResize, { passive: true });
    
    // ============================================================
    // 9. PRELOAD CRITICAL RESOURCES
    // ============================================================
    
    function preloadCriticalResources() {
        // Preload first few channel images
        const firstImages = document.querySelectorAll('.channel-card img, .carousel-card img');
        const limit = isMobile ? 3 : 6;
        
        Array.from(firstImages).slice(0, limit).forEach(img => {
            if (img.dataset.src) {
                const link = document.createElement('link');
                link.rel = 'preload';
                link.as = 'image';
                link.href = img.dataset.src;
                document.head.appendChild(link);
            }
        });
    }
    
    // ============================================================
    // 10. MEMORY MANAGEMENT
    // ============================================================
    
    function cleanupUnusedElements() {
        // Remove elements that are far off-screen on mobile
        if (!isMobile) return;
        
        const allCards = document.querySelectorAll('.channel-card, .featured-sports-card');
        const viewportHeight = window.innerHeight;
        
        allCards.forEach(card => {
            const rect = card.getBoundingClientRect();
            const distanceFromViewport = Math.abs(rect.top - viewportHeight);
            
            // If more than 3 screens away, reduce complexity
            if (distanceFromViewport > viewportHeight * 3) {
                card.classList.add('far-offscreen');
            } else {
                card.classList.remove('far-offscreen');
            }
        });
    }
    
    // Run cleanup every 2 seconds on mobile
    if (isMobile) {
        setInterval(cleanupUnusedElements, 2000);
    }
    
    // ============================================================
    // 11. DISABLE EXPENSIVE CSS ON LOW-END DEVICES
    // ============================================================
    
    if (isLowEndDevice) {
        const style = document.createElement('style');
        style.textContent = `
            /* Disable expensive effects */
            * {
                backdrop-filter: none !important;
                filter: none !important;
            }
            
            .channel-card,
            .featured-sports-card,
            .carousel-card {
                box-shadow: 0 2px 8px rgba(0,0,0,.3) !important;
                transition: transform 0.15s ease !important;
            }
            
            /* Disable blur effects */
            .loading-overlay,
            #channelSelectorOverlay,
            #channelChangeNotification {
                backdrop-filter: none !important;
                background: rgba(17, 24, 39, 0.98) !important;
            }
            
            /* Simplify animations */
            @keyframes fadeInUp,
            @keyframes slideInRight,
            @keyframes pulseGlow {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }
    
    // ============================================================
    // 12. OPTIMIZE VIDEO PLAYER LOADING
    // ============================================================
    
    if (isMobile && window.location.pathname.includes('/watch')) {
        // Reduce video.js features on mobile
        window.mobileVideoOptimizations = {
            controlBar: {
                children: [
                    'playToggle',
                    'progressControl',
                    'volumePanel',
                    'fullscreenToggle'
                ]
            },
            html5: {
                vhs: {
                    enableLowInitialPlaylist: true,
                    smoothQualityChange: false,
                    overrideNative: !isMobile // Use native on mobile when possible
                }
            }
        };
    }
    
    // ============================================================
    // INITIALIZATION
    // ============================================================
    
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }
        
        // Run optimizations
        observeImages();
        optimizeCarousel();
        optimizeChannelGrid();
        deferNonCritical();
        
        if (isMobile) {
            preloadCriticalResources();
        }
        
        // Log optimization status
        console.log('Mobile Optimizations:', {
            isMobile,
            isLowEndDevice,
            cores: navigator.hardwareConcurrency,
            memory: navigator.deviceMemory + 'GB'
        });
    }
    
    // Start initialization
    init();
    
    // ============================================================
    // EXPOSE UTILITIES
    // ============================================================
    
    window.MobileOptimizer = {
        isMobile,
        isLowEndDevice,
        debounce,
        cleanupUnusedElements
    };
    
})();
