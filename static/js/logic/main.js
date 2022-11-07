// Variables

const SERVER = 'http://127.0.0.1:8000';

const alertTypes = {
    INFO: {
        label: 'Info',
        class: 'alert-primary',
        icon: '#info-fill'
    },
    SUCCESS: {
        label: 'Success',
        class: 'alert-success',
        icon: '#check-circle-fill'
    },
    WARNING: {
        label: 'Warning',
        class: 'alert-warning',
        icon: '#exclamation-triangle-fill'
    },
    ERROR: {
        label: 'Error',
        class: 'alert-danger',
        icon: '#exclamation-triangle-fill'
    },
}

const notifyDivSelector = '#notifications .container';

// Event listeners

window.addEventListener('DOMContentLoaded', () => {
    notifySessionMessages();
});

// get csrf token

async function csrfToken() {
    const url = `${SERVER}/csrf-token/`;
    let response = await fetch(url);
    response = await response.json();
    const csrfToken = response.csrf_token;
    console.log('Got csrf token!');
    return csrfToken;
}


// fetch request helper function

async function _fetch(url, callback, method='GET', data) {
    let headers = new Headers({
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
    });

    if (method !== 'GET') {
        headers.set('X-CSRFToken', JSON.parse(data)['csrfmiddlewaretoken']);
    }

    fetch(url, {
        method: method,
        headers: headers,
        body: data
    })
    .then(response => {
        result = response.json();
        status_code = response.status;
        if(status_code != 200) {
            console.log('Error fetching');
            return false;
        }        
        return result
    })
    .then(data => {
        console.log(data);
        callback(data)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function formatDate(dateStr) {
    if (dateStr == null) return '';

    let date = new Date(dateStr);
    let dd = String(date.getDate()).padStart(2, '0');
    let mm = String(date.getMonth() + 1).padStart(2, '0');
    let yyyy = date.getFullYear();

    let formattedDate = `${dd}/${mm}/${yyyy}`;
    return formattedDate;
}


// Notifications

// error

function notifyError(message, autohide=true) {
    if (autohide) notifyAutoHide(message, 'ERROR');
    else notify(message, 'ERROR');
}

// success

function notifySuccess(message, autohide=true) {
    if (autohide) notifyAutoHide(message, 'SUCCESS');
    else notify(message, 'SUCCESS');
}

// info

function notifyInfo(message, autohide=true) {
    if (autohide) notifyAutoHide(message, 'INFO');
    else notify(message, 'INFO');
}

// warning

function notifyWarning(message, autohide=true) {
    if (autohide) notifyAutoHide(message, 'WARNING');
    else notify(message, 'WARNING');
}

// notify autohide

async function notifyAutoHide(message, alertType='INFO', after=3000) {
    await notify(message, alertType);
    setTimeout(() => {
        document.querySelector(notifyDivSelector).querySelector('[data-bs-dismiss="alert"]').click();
    }, after);
}

// notify

async function notify(message, alertType='INFO') {  
    let notification = `
   <div class="alert ${alertTypes[alertType].class} alert-dismissible fade show d-flex shadow mt-1" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="${alertTypes[alertType].label}">
        <use xlink:href="${alertTypes[alertType].icon}"/>
        </svg>
        <div>${message}</div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
   </div>
   `;
    document.querySelector(notifyDivSelector).innerHTML = notification;
}


// Session notifications

function notifySessionMessages() {
    if (document.querySelector('.session-message')) {
        let message = document.querySelector('.session-message');
        notifyAutoHide(
            message.querySelector('[name="message"]').value,
            message.querySelector('[name="alertType"]').value
        )
    }
}


// load form data

function loadFormData(formData) {
    let data = {};
    for (const pair of formData.entries()) {
        data[pair[0]] = pair[1];
    }
    return JSON.stringify(data);
}


// open/close bs popup (modal/offcanvas)
function showBSPopup(id) {
    const toggleSelector = `[data-bs-target="#${id}"]`;
    document.querySelector(toggleSelector).click();
}

function hideBSPopup(id) {
    const popup = document.getElementById(id);
    popup.querySelector('[data-bs-dismiss]').click();
}