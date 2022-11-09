/**
 * [logic] Fetches expense details
 * @param {Number} id - expense id
 */
async function expenseDetails(id) {
    const url = `/organizer/expenses/${id}/details/`
    const callback = async (exp) => {
        fillOffcanvas(exp)
        showBSPopup('offcanvasExpense')
    }
    _fetch(url, callback)
}

/**
 * [logic] Updates expense record
 * @param {Number} id - expense id
 * @param {FormData} formData - expense update form data
 */
async function updateExpense(id, formData) {
    formData.append('expense_id', id)
    const data = loadFormData(formData)
    const url = window.location.pathname
    const callback = async (msg) => {
        notifyAutoHide(msg.content, msg.tag)
        updateExpenseUI(id)
    }
    _fetch(url, callback, 'POST', data)
}


/**
 * [logic] Deletes expense record
 * @param {Number} id - expense id
 */
async function deleteExpense(id) {
    const url = `/organizer/expenses/${id}/delete/`
    const callback = async (msg) => {
        removeExpenseRowUI(id)
        hideBSPopup('offcanvasExpense')
        notifyAutoHide(msg.content, msg.tag)
    }
    _fetch(url, callback)
}