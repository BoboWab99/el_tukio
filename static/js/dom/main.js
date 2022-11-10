// focus on first modal input
document.querySelectorAll('.modal').forEach(modal => {
    if (modal.querySelector('.form-control')) {
        modal.addEventListener('shown.bs.modal', () => {
            modal.querySelector('.form-control').focus();
        });
    }
});

/**
 * Show bootstrap popup (EG: modal, offcanvas) element
 * @param {String} id - popup element ID
 */
function showBSPopup(id) {
    const toggleSelector = `[data-bs-target="#${id}"]`;
    document.querySelector(toggleSelector).click();
}

/**
 * Hide bootstrap popup (EG: modal, offcanvas) element
 * @param {String} id - popup element ID
 */
function hideBSPopup(id) {
    const popup = document.getElementById(id);
    popup.querySelector('[data-bs-dismiss]').click();
}