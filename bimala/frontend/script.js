// Clean script for native form handling

document.addEventListener('DOMContentLoaded', () => {
    // We only need basic DOM manipulation here since Flask handles rendering and routing.
    
    // Auto-hide flash messages after 3 seconds
    const flashes = document.querySelectorAll('.flash-messages');
    if (flashes.length > 0) {
        setTimeout(() => {
            flashes.forEach(flash => flash.style.display = 'none');
        }, 3000);
    }
});
