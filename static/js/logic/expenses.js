
async function expenseDetails(id) {
    const url = `/organizer/expenses/${id}/details/`
    const callback = async (exp) => {
        fillOffcanvas(exp)
        showBSPopup('offcanvasExpense')
    }
    _fetch(url, callback)
}


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