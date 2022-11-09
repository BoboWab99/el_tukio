const chatFormWrapper = document.getElementById('chatFormWrapper')
let chatMessageForm = document.forms.chatMessageForm

/**
 * Fills the hidden 'reference' input with original message id and displays its preview
 * @param {Number} id id of the message to reply to
 * @param {HTMLDivElement} target option clicked on
 */
function replyTo(id, target) {
    const form = chatMessageForm
    const wrapper = chatFormWrapper
    form.elements['reference'].value = id
    let msgElm = target.closest('.chat-message')
    let data = msgElm.querySelector('.chat-message-content').outerHTML
    let popup = createPopup(data)
    if ((_alert = wrapper.querySelector('.alert'))) wrapper.removeChild(_alert)
    wrapper.insertBefore(popup, form)
}

/**
 * Creates popup containing the content of the message to reply to
 * @param {String} data html formatted string containing the message content
 * @returns bs alert element
 */
function createPopup(data) {
    const html = `
    <div class="chat-message-wrapper">
        <small class="d-block mb-2">Replying to:</small>
        <div class="chat-message-inner incoming">${data}</div>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" onclick="emptyRef()"></button>`
    const popup = document.createElement('div')
    popup.setAttribute('role', 'alert')
    popup.setAttribute('class', 'alert alert-success alert-dismissible fade show position-absolute start-0 end-0 bottom-100')
    popup.innerHTML = html
    return popup
}

/**
 * Empties the value of the 'reference' input of the message to reply to.
 */
function emptyRef() {
    chatMessageForm.elements['reference'].value = ''
}