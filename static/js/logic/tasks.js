// vars
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

/**
 * Sends a request to update task group
 * @param {FormData} formData submitted form data
 */
function _renameGroup(formData) {
    const url = taskGroupForm.action
    const data = loadFormData(formData)
    const callback = async (msg) => {
        hideBSPopup('taskGroupModal')
        notifyAutoHide(msg.content, msg.tag)
        updateTaskGroupUI(formData.get('task_group_id'), formData.get('group_form-name'))
        resetGroupForm()
    }
    _fetch(url, callback, 'POST', data)
}