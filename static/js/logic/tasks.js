// modal value placeholders
const sectionTasks = document.getElementById('sectionTasks');
const offcanvas = document.getElementById('offcanvasTask');
const newTaskForm = document.forms.newTaskForm;
const taskCtUpdateForm = document.forms.taskCtUpdateForm;
const taskDdUpdateForm = document.forms.taskDdUpdateForm;
const newTaskGroupForm = document.forms.newTaskGroupForm;
const modalTask = document.getElementById('id_task_u_form-task');
const modalDueDate = document.getElementById('id_task_u_form-due_date');
const modalCheck = document.getElementById('id_completed');
const modalCreatedBy = document.getElementById('created_by');
const modalDateCreated = document.getElementById('date_created');
const modalCompletedBy = document.getElementById('completed_by');
const modalDateCompleted = document.getElementById('date_completed');
const modalDeleteTask = document.getElementById('deleteTask');
const assignedToElm = document.getElementById('assignedTo');


/*
window.addEventListener('DOMContentLoaded', () => {
    // https://stackoverflow.com/questions/23593052/format-javascript-date-as-yyyy-mm-dd
    let today = new Date();
    const offset = today.getTimezoneOffset();
    today = new Date(today.getTime() - (offset * 60 * 1000));
    today = today.toISOString().split('T')[0];

    let eventDate = document.getElementById('_eventDate').value;
    eventDate = new Date(eventDate).toISOString().split('T')[0];
    modalDueDate.setAttribute('min', today);
    modalDueDate.setAttribute('max', eventDate);

    // console.log(window.location.pathname);
});
*/

let orgTask = null;
let orgDueDate = null;
let taskCtChanged = false;
let taskDdChanged = false;
let taskStatusChanged = false;

const listenToTaskChange = () => {
    if (orgTask !== modalTask.value)  {
        taskCtUpdateForm.querySelector('[type="submit"]').click();
        taskCtChanged = true;
    }
};

const listenToDateChange = () => {
    if (orgDueDate !== modalDueDate.value)  {
        taskDdUpdateForm.querySelector('[type="submit"]').click();
        taskDdChanged = true;
    }
};

offcanvas.addEventListener('shown.bs.offcanvas', () => {
    orgTask = modalTask.value;
    orgDueDate = modalDueDate.value;
    modalTask.addEventListener('focusout', listenToTaskChange);
    modalDueDate.addEventListener('change', listenToDateChange);
});

offcanvas.addEventListener('hidden.bs.offcanvas', () => {
    modalTask.removeEventListener('focusout', listenToTaskChange);
    modalDueDate.removeEventListener('change', listenToDateChange);
});

/*
newTaskForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const url = window.location.pathname;
    const callback = async (data) => {
        let task = data['task'];
        let msg = data['msg'];
        createTaskElm(task);
        hideBSPopup('newTaskModal');
        notifyAutoHide(msg.content, msg.tag);
    };
    const formData = new FormData(newTaskForm);
    const task = loadFormData(formData);
    _fetch(url, callback, 'POST', task);
});
*/

[taskCtUpdateForm, taskDdUpdateForm].forEach(form => {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const taskId = form.dataset.taskId;
        let formData = new FormData(form);
        formData.append('task_id', taskId);
        let data = loadFormData(formData);
        const url = window.location.pathname;
        const callback = async (msg) => {
            notifyAutoHide(msg.content, msg.tag);
            updateTaskUI(taskId);
        }
        _fetch(url, callback, 'POST', data);
    });
});

/*
newTaskGroupForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const url = window.location.pathname;
    const callback = async (msg) => {
        hideBSPopup('taskGroupModal');
        notifyAutoHide(msg.content, msg.tag);
    };
    const formData = new FormData(newTaskGroupForm);
    const taskGroup = loadFormData(formData);
    _fetch(url, callback, 'POST', taskGroup);
});
*/

async function taskDetails(taskId) {
    const url = `/organizer/tasks/${taskId}/details/`;
    const callback = async (task) => {
        fillOffcanvas(task);
        if (!offcanvas.classList.contains('show')) showBSPopup('offcanvasTask');
    }
    _fetch(url, callback);
}

async function changeTaskStatus(taskId, fromModal = false) {
    const url = `/organizer/tasks/${taskId}/complete/`;
    const callback = async (msg) => {
        notifyAutoHide(msg.content, msg.tag);
        taskDetails(taskId);
        if (fromModal) {
            taskStatusChanged = true;
            updateTaskUI(taskId);
        }
    }
    _fetch(url, callback);
}

async function assignTaskTo(memberId) {
    const taskId = taskCtUpdateForm.dataset.taskId;
    const url = `/organizer/tasks/${taskId}/assign/${memberId}`;
    const callback = async (msg) => {
        notifyAutoHide(msg.content, msg.tag);
        taskDetails(taskId);
        hideBSPopup('assignTaskModal');
    }
    _fetch(url, callback);
}

async function assignTaskToRemove(taskId) {
    const url = `/organizer/tasks/${taskId}/assign/remove/`;
    const callback = async (msg) => {
        notifyAutoHide(msg.content, msg.tag);
        taskDetails(taskId);
    }
    _fetch(url, callback);
}

async function deleteTask(taskId) {
    const url = `/organizer/tasks/${taskId}/delete/`;
    const callback = async (msg) => {
        const taskElm = sectionTasks.querySelector(`[data-task-id="${taskId}"]`);
        sectionTasks.removeChild(taskElm);
        hideBSPopup('offcanvasTask');
        notifyAutoHide(msg.content, msg.tag);
    }
    _fetch(url, callback);
}

function updateTaskUI(taskId) {
    const taskElm = sectionTasks.querySelector(`[data-task-id="${taskId}"]`);
    if (taskCtChanged) {
        const valueTask = taskElm.querySelector('[data-value="task"]');
        valueTask.innerHTML = modalTask.value;
    }
    if (taskDdChanged) {
        const valueDueDate = taskElm.querySelector('[data-value="due-date"]');
        valueDueDate.innerHTML = formatDate(modalDueDate.value);
    }
    if (taskStatusChanged) {
        const checkbox = taskElm.querySelector('input[type="checkbox"]');
        if (modalCheck.checked) checkbox.checked = true;
        else checkbox.checked = false;
    }
}