// ============================================================
// ANDROID TV REMOTE CONTROL SUPPORT
// ============================================================

// Channel list for quick access
let channelList = [];
let currentChannelIndex = -1;

// Initialize channel list from sidebar
function initChannelList() {
    const channelItems = document.querySelectorAll('.sidebar-channel-item');
    channelList = Array.from(channelItems).map(item => ({
        id: parseInt(item.dataset.channelId),
        name: item.dataset.channelName,
        element: item
    }));
    
    // Find current channel index
    const activeItem = document.querySelector('.sidebar-channel-item.active');
    if (activeItem) {
        currentChannelIndex = channelList.findIndex(ch => ch.id === parseInt(activeItem.dataset.channelId));
    }
}

// Channel selector overlay for number pad
let channelSelectorTimeout = null;
let selectedChannelNumber = '';

function showChannelSelector(number) {
    // Create or get overlay
    let overlay = document.getElementById('channelSelectorOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'channelSelectorOverlay';
        overlay.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(17, 24, 39, 0.95);
            backdrop-filter: blur(10px);
            border: 2px solid #3b82f6;
            border-radius: 16px;
            padding: 32px 48px;
            z-index: 99999;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
            min-width: 300px;
            text-align: center;
            transition: all 0.3s ease;
        `;
        
        const numberDisplay = document.createElement('div');
        numberDisplay.id = 'channelNumberDisplay';
        numberDisplay.style.cssText = `
            font-size: 4rem;
            font-weight: 700;
            color: #3b82f6;
            margin-bottom: 16px;
            letter-spacing: 0.1em;
            text-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
        `;
        
        const label = document.createElement('div');
        label.style.cssText = `
            font-size: 1rem;
            color: #a8bcd4;
            font-weight: 500;
        `;
        label.textContent = 'Channel Number';
        
        const channelName = document.createElement('div');
        channelName.id = 'channelPreviewName';
        channelName.style.cssText = `
            font-size: 1.2rem;
            color: #60a5fa;
            margin-top: 16px;
            font-weight: 600;
            min-height: 32px;
        `;
        
        overlay.appendChild(numberDisplay);
        overlay.appendChild(label);
        overlay.appendChild(channelName);
        document.body.appendChild(overlay);
    }
    
    const numberDisplay = document.getElementById('channelNumberDisplay');
    const channelName = document.getElementById('channelPreviewName');
    
    selectedChannelNumber = number;
    numberDisplay.textContent = selectedChannelNumber;
    
    // Show channel name if exists
    const channelIndex = parseInt(selectedChannelNumber) - 1;
    if (channelIndex >= 0 && channelIndex < channelList.length) {
        channelName.textContent = channelList[channelIndex].name;
    } else {
        channelName.textContent = '';
    }
    
    overlay.style.display = 'block';
    
    // Auto-hide and switch after 2 seconds
    clearTimeout(channelSelectorTimeout);
    channelSelectorTimeout = setTimeout(() => {
        hideChannelSelector();
        switchToChannelNumber(parseInt(selectedChannelNumber));
    }, 2000);
}

function hideChannelSelector() {
    const overlay = document.getElementById('channelSelectorOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
    selectedChannelNumber = '';
}

function switchToChannelNumber(number) {
    const index = number - 1;
    if (index >= 0 && index < channelList.length) {
        const channel = channelList[index];
        if (typeof loadChannel === 'function') {
            loadChannel(channel.id);
        }
    }
}

// Navigate channels with remote
function navigateChannel(direction) {
    if (channelList.length === 0) return;
    
    if (direction === 'next') {
        currentChannelIndex = (currentChannelIndex + 1) % channelList.length;
    } else if (direction === 'prev') {
        currentChannelIndex = currentChannelIndex - 1;
        if (currentChannelIndex < 0) currentChannelIndex = channelList.length - 1;
    }
    
    const channel = channelList[currentChannelIndex];
    if (channel && typeof loadChannel === 'function') {
        showChannelChangeNotification(channel.name, direction);
        loadChannel(channel.id);
    }
}

// Show channel change notification
function showChannelChangeNotification(channelName, direction) {
    let notification = document.getElementById('channelChangeNotification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'channelChangeNotification';
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 24px;
            background: rgba(17, 24, 39, 0.95);
            backdrop-filter: blur(10px);
            border: 2px solid #3b82f6;
            border-radius: 12px;
            padding: 16px 24px;
            z-index: 99998;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
            display: none;
            min-width: 250px;
            transition: all 0.3s ease;
        `;
        document.body.appendChild(notification);
    }
    
    const arrow = direction === 'next' ? '▼' : '▲';
    const position = `${currentChannelIndex + 1}/${channelList.length}`;
    
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="font-size: 1.5rem; color: #3b82f6;">${arrow}</div>
            <div style="flex: 1;">
                <div style="font-size: 0.75rem; color: #a8bcd4; margin-bottom: 4px;">
                    Channel ${position}
                </div>
                <div style="font-size: 1rem; color: #fff; font-weight: 600;">
                    ${channelName}
                </div>
            </div>
        </div>
    `;
    
    notification.style.display = 'block';
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            notification.style.display = 'none';
            notification.style.opacity = '1';
        }, 300);
    }, 3000);
}

// Remote control key handler
function handleRemoteKey(event) {
    // Ignore if typing in input
    const tag = document.activeElement.tagName;
    if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return;
    
    const key = event.key;
    const keyCode = event.keyCode;
    
    // Number keys (0-9) for direct channel selection
    if (key >= '0' && key <= '9') {
        event.preventDefault();
        
        // Handle multi-digit channel numbers
        if (selectedChannelNumber.length < 3) {
            showChannelSelector(selectedChannelNumber + key);
        }
        return;
    }
    
    // Android TV remote keys
    switch(keyCode) {
        // Channel Up (Page Up or specific Android TV key)
        case 33: // Page Up
        case 166: // Media Previous Track (some remotes)
            event.preventDefault();
            navigateChannel('next');
            break;
            
        // Channel Down (Page Down or specific Android TV key)
        case 34: // Page Down
        case 167: // Media Next Track (some remotes)
            event.preventDefault();
            navigateChannel('prev');
            break;
            
        // Arrow Up - Previous channel
        case 38: // Arrow Up
            // Only if not in fullscreen
            if (!document.fullscreenElement && !vjsPlayer?.isFullscreen()) {
                event.preventDefault();
                navigateChannel('prev');
            }
            break;
            
        // Arrow Down - Next channel
        case 40: // Arrow Down
            // Only if not in fullscreen
            if (!document.fullscreenElement && !vjsPlayer?.isFullscreen()) {
                event.preventDefault();
                navigateChannel('next');
            }
            break;
            
        // OK/Enter - Open channel list
        case 13: // Enter
            if (!document.fullscreenElement) {
                event.preventDefault();
                if (typeof toggleSidebar === 'function') {
                    toggleSidebar();
                }
            }
            break;
            
        // Back button - Close sidebar or exit fullscreen
        case 27: // Escape
        case 8: // Backspace (Android TV back)
            event.preventDefault();
            const sidebar = document.getElementById('channelsSidebar');
            if (sidebar && sidebar.classList.contains('open')) {
                if (typeof closeSidebar === 'function') {
                    closeSidebar();
                }
            } else if (document.fullscreenElement || vjsPlayer?.isFullscreen()) {
                if (vjsPlayer) {
                    vjsPlayer.exitFullscreen();
                }
            }
            break;
            
        // Play/Pause
        case 32: // Space
        case 179: // Media Play/Pause
            event.preventDefault();
            if (vjsPlayer) {
                if (vjsPlayer.paused()) {
                    vjsPlayer.play();
                } else {
                    vjsPlayer.pause();
                }
            }
            break;
    }
}

// Initialize remote control support
function initRemoteControl() {
    // Initialize channel list
    initChannelList();
    
    // Add keyboard event listener
    document.addEventListener('keydown', handleRemoteKey);
    
    // Re-initialize channel list when channels are updated
    const observer = new MutationObserver(() => {
        initChannelList();
    });
    
    const sidebar = document.getElementById('sidebarChannelsList');
    if (sidebar) {
        observer.observe(sidebar, { childList: true, subtree: true });
    }
    
    console.log('Android TV Remote Control initialized');
    console.log(`Total channels: ${channelList.length}`);
}

// Video Player Helper Functions
function retryStream(player, streamUrl, streamType) {
    console.log('Retrying stream...');
    player.src({
        src: streamUrl,
        type: streamType
    });
    player.load();
    player.play().catch(function(error) {
        console.error('Retry failed:', error);
    });
}

function handleStreamError(player, retryCallback) {
    const error = player.error();
    if (error) {
        console.error('Stream error code:', error.code);
        console.error('Stream error message:', error.message);
        
        // Common error codes
        switch(error.code) {
            case 2: // MEDIA_ERR_NETWORK
                console.log('Network error - stream may be unavailable');
                break;
            case 3: // MEDIA_ERR_DECODE
                console.log('Decode error - stream format may be incompatible');
                break;
            case 4: // MEDIA_ERR_SRC_NOT_SUPPORTED
                console.log('Source not supported - check stream URL and format');
                break;
            default:
                console.log('Unknown error');
        }
        
        if (retryCallback) {
            retryCallback();
        }
    }
}

// Export for use in templates
window.VideoPlayerHelpers = {
    retryStream,
    handleStreamError,
    initRemoteControl,
    navigateChannel,
    switchToChannelNumber
};
