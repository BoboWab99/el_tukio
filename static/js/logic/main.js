// vars
/**
 * Server
 */
const SERVER = 'http://127.0.0.1:8000'


/**
 * Retrieves csrf token
 * @returns token string
 */
async function csrfToken() {
    const url = `${SERVER}/csrf-token/`;
    let response = await fetch(url);
    response = await response.json();
    const csrfToken = response.csrf_token;
    console.log('Got csrf token!');
    return csrfToken;
}

/**
 * Fetch API helper function
 * @param {String} url target url
 * @param {Function} callback executed on success - takes in the data param
 * @param {String} method HTTP request method
 * @param {String} data JSON string
 */
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

/**
 * format date string to 'dd/mm/yyyy' EG: '25/12/2000'
 * @param {String} dateStr - date string
 * @returns formtted date string
 */
function formatDate(dateStr) {
    if (dateStr == null) return '';

    let date = new Date(dateStr);
    let dd = String(date.getDate()).padStart(2, '0');
    let mm = String(date.getMonth() + 1).padStart(2, '0');
    let yyyy = date.getFullYear();

    let formattedDate = `${dd}/${mm}/${yyyy}`;
    return formattedDate;
}

/**
 * Get JSON string containing submitted form data
 * @param {FormData} formData  - form data instance from html form
 * @returns {String} JSON string
 */
function loadFormData(formData) {
    let data = {};
    for (const pair of formData.entries()) {
        data[pair[0]] = pair[1];
    }
    return JSON.stringify(data);
}