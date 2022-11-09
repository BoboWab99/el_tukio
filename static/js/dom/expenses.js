const offcanvas = document.getElementById('offcanvasExpense')
const offcanvasDescription = document.getElementById('id_exp_u_form-description')
const offcanvasTotalCost = document.getElementById('id_exp_u_form-total_cost')
const offcanvasTotalPaid = document.getElementById('id_exp_u_form-total_paid')
const offcanvasBudgetedBy = document.getElementById('budgetedBy')
const offcanvasDateBudgeted = document.getElementById('dateBudgeted')
const offcanvasDeleteExpenseBtn = document.getElementById('deleteExpense')
const newExpenseForm = document.forms.newExpenseForm
const expenseUpdateForm = document.forms.expenseUpdateForm
const expensesTable = document.querySelector('#expensesTable tbody')


offcanvas.addEventListener('shown.bs.offcanvas', () => {
    expenseUpdateForm.addEventListener('change', submitForm)
})

offcanvas.addEventListener('hidden.bs.offcanvas', () => {
    expenseUpdateForm.removeEventListener('change', submitForm)
})

expenseUpdateForm.addEventListener('submit', (e) => {
    e.preventDefault()
    let _this = expenseUpdateForm
    updateExpense(_this.dataset.expId, new FormData(_this))
})

offcanvasDeleteExpenseBtn.addEventListener('click', () => {
    deleteExpense(expenseUpdateForm.dataset.expId)
})

/**
 * [ui] Submits expenseUpdateForm
 */
function submitForm() {
    expenseUpdateForm.querySelector('[type="submit"]').click()
}

/**
 * [ui] Removes table row containing deleted expense details
 * @param {NUmber} id - expense id
 */
function removeExpenseRowUI(id) {
    const elm = expensesTable.querySelector(`tr[data-exp-id="${id}"]`)
    expensesTable.removeChild(elm)
}

/**
 * [ui] Fills offcanvas on 'expensesTable' row click
 * @param {Object} expense - expense data
 */
function fillOffcanvas(expense) {
    const xp = expense
    expenseUpdateForm.setAttribute('data-exp-id', xp.id)
    offcanvasDescription.value = xp.description
    offcanvasTotalCost.value = xp.total_cost
    offcanvasTotalPaid.value = xp.total_paid
    offcanvasBudgetedBy.innerHTML = `${xp.budgeted_by_fname} ${xp.budgeted_by_lname}`
    offcanvasDateBudgeted.innerHTML = formatDate(xp.date_budgeted)
}

/**
 * [ui] Updates the 'expensesTable' row containing updated expense's details
 * @param {Number} id - expense id
 */
function updateExpenseUI(id) {
    const elm = expensesTable.querySelector(`tr[data-exp-id="${id}"]`)
    elm.querySelector('[data-value="description"]').innerHTML = offcanvasDescription.value
    elm.querySelector('[data-value="total-cost"]').innerHTML = offcanvasTotalCost.value
    elm.querySelector('[data-value="total-paid"]').innerHTML = offcanvasTotalPaid.value
}