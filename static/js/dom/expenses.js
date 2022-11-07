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

class FormWatcher {
    formElements = []
    initialValues = []

    constructor(form) {
        this.form = form
        this.initializeValues()
    }

    // formElements() {
    //     return Array.from(this.form.elements).filter((ff) => ff.type !== 'submit')
    // }

    initializeValues() {
        this.formElements =  Array.from(this.form.elements).filter((ff) => ff.type !== 'submit')
        const ffs = this.formElements
        ffs.forEach(ff => {
            this.initialValues.push(ff.value)
        })
    }

    hasFormChanged() {
        let hasChanged = false
        let ffs = this.formElements

        this.initialValues.forEach(element => {
            console.log(element)
        });

        ffs.forEach(element => {
            console.log(element.value)
        }); 

        for (let i = 0; i < ffs.length; i++) {
            // console.log(this.initialValues[i])
            // console.log(ffs[i].value)
            // console.log(`changed: ${ffs[i].id}`)

            if (ffs[i].value != this.initialValues[i]) {
                hasChanged = true
                break
            }
        }
        return hasChanged
    }

    watch(callback) {
        this.formElements.forEach(ff => {
            ff.addEventListener('focusout', callback)
        })
    }

    stopWatch(callback) {
        this.formElements.forEach(ff => {
            ff.removeEventListener('focusout', callback)
        })
    }
}

let watcher = null;

offcanvas.addEventListener('shown.bs.offcanvas', () => {
    // watcher = new FormWatcher(expenseUpdateForm)
    // watcher.watch(handleUpdate)
    expenseUpdateForm.addEventListener('change', submitForm)
})

offcanvas.addEventListener('hidden.bs.offcanvas', () => {
    // watcher.stopWatch(handleUpdate)
    // watcher = null
    expenseUpdateForm.removeEventListener('change', submitForm)
})

expenseUpdateForm.addEventListener('submit', (e) => {
    e.preventDefault()
    let _this = expenseUpdateForm
    updateExpense(_this.dataset.expId, new FormData(_this))
    // console.log('Form submitted!')
})


function submitForm() {
    expenseUpdateForm.querySelector('[type="submit"]').click()
}


function handleUpdate() {
    if(watcher.hasFormChanged()) {
        // expenseUpdateForm.submit()
        console.log("form changed!")
    } else {
        console.log("form NOT changed!")
    }
}


function listenToFormChanges(form) {

}


function fillOffcanvas(expense) {
    const xp = expense
    expenseUpdateForm.setAttribute('data-exp-id', xp.id)
    offcanvasDescription.value = xp.description
    offcanvasTotalCost.value = xp.total_cost
    offcanvasTotalPaid.value = xp.total_paid
    offcanvasBudgetedBy.innerHTML = `${xp.budgeted_by_fname} ${xp.budgeted_by_lname}`
    offcanvasDateBudgeted.innerHTML = xp.date_budgeted
}

function updateExpenseUI(expenseID) {
    const elm = expensesTable.querySelector(`[data-exp-id="${expenseID}"]`)
    elm.querySelector('[data-value="description"]').innerHTML = offcanvasDescription.value
    elm.querySelector('[data-value="total-cost"]').innerHTML = offcanvasTotalCost.value
    elm.querySelector('[data-value="total-paid"]').innerHTML = offcanvasTotalPaid.value
}