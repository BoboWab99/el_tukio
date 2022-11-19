// vars

const alertTypes = {
    INFO: {
        label: 'Info',
        class: 'bg-primary text-white',
        icon: '#info-fill'
    },
    SUCCESS: {
        label: 'Success',
        class: 'bg-success text-white',
        icon: '#check-circle-fill'
    },
    WARNING: {
        label: 'Warning',
        class: 'bg-warning text-dark',
        icon: '#exclamation-triangle-fill'
    },
    ERROR: {
        label: 'Error',
        class: 'bg-danger text-white',
        icon: '#exclamation-triangle-fill'
    },
}

const notifyDivSelector = '#notifications .content'


// Event listeners

window.addEventListener('DOMContentLoaded', () => {
    notifySessionMessages()
})

// focus on first modal input
document.querySelectorAll('.modal').forEach(modal => {
    if (modal.querySelector('.form-control')) {
        modal.addEventListener('shown.bs.modal', () => {
            modal.querySelector('.form-control').focus();
        });
    }
})

// Notifications

/**
 * Notify error
 * @param {String} message Message to display
 * @param {Boolean} autohide default-True
 */
function notifyError(message, autohide = true) {
    if (autohide) notifyAutoHide(message, 'ERROR');
    else notify(message, 'ERROR');
}

/**
 * Notify success
 * @param {String} message Message to display
 * @param {Boolean} autohide default-True
 */
function notifySuccess(message, autohide = true) {
    if (autohide) notifyAutoHide(message, 'SUCCESS');
    else notify(message, 'SUCCESS');
}

/**
 * Notify info
 * @param {String} message Message to display
 * @param {Boolean} autohide default-True
 */
function notifyInfo(message, autohide = true) {
    if (autohide) notifyAutoHide(message, 'INFO');
    else notify(message, 'INFO');
}

/**
 * Notify warning
 * @param {String} message Message to display
 * @param {Boolean} autohide default-True
 */
function notifyWarning(message, autohide = true) {
    if (autohide) notifyAutoHide(message, 'WARNING');
    else notify(message, 'WARNING');
}

/**
 * Notify autohide after n seconds
 * @param {String} message Message to display
 * @param {String} alertType choices: INFO, ERROR, WARNING, SUCCESS
 * @param {Number} after number of seconds
 */
async function notifyAutoHide(message, alertType='INFO', after=3000) {
    await notify(message, alertType);
    setTimeout(() => {
        document.querySelector(notifyDivSelector).querySelector('[data-bs-dismiss="alert"]').click();
    }, after);
}

/**
 * Notify message
 * @param {String} message Message to display
 * @param {String} alertType choices: INFO, ERROR, WARNING, SUCCESS
 */
async function notify(message, alertType = 'INFO') {
    let closeBtnClass = 'btn-close'
    if (alertType != 'WARNING') {
        closeBtnClass += ' btn-close-white'
    }
    let notification = `
   <div class="alert ${alertTypes[alertType].class} alert-dismissible fade show d-inline-flex align-items-center shadow-lg ms-3 mb-4" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="21" height="21" role="img" aria-label="${alertTypes[alertType].label}">
        <use xlink:href="${alertTypes[alertType].icon}"/>
        </svg>
        <div>${message}</div>
        <button type="button" class="${closeBtnClass}" data-bs-dismiss="alert" aria-label="Close"></button>
   </div>`
    document.querySelector(notifyDivSelector).innerHTML = notification
}


/**
 * Alerts session notifications
 */
function notifySessionMessages() {
    if (document.querySelector('.session-message')) {
        let message = document.querySelector('.session-message')
        notifyAutoHide(
            message.querySelector('[name="message"]').value,
            message.querySelector('[name="alertType"]').value
        )
    }
}

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