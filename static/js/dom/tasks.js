// vars
const sectionTasks = document.getElementById('sectionTasks');
const offcanvas = document.getElementById('offcanvasTask');
const newTaskForm = document.forms.newTaskForm;
const taskCtUpdateForm = document.forms.taskCtUpdateForm;
const taskDdUpdateForm = document.forms.taskDdUpdateForm;
const taskGroupForm = document.forms.newTaskGroupForm;
const modalTask = document.getElementById('id_task_u_form-task');
const modalDueDate = document.getElementById('id_task_u_form-due_date');
const modalCheck = document.getElementById('id_completed');
const modalCreatedBy = document.getElementById('created_by');
const modalDateCreated = document.getElementById('date_created');
const modalCompletedBy = document.getElementById('completed_by');
const modalDateCompleted = document.getElementById('date_completed');
const modalDeleteTask = document.getElementById('deleteTask');
const assignedToElm = document.getElementById('assignedTo');


/**
 * Fills the task group form with eisting task group data
 * @param {Number} id id of the task group
 * @param {HTMLElement} target clicked option
 */
function renameGroup(id, target) {
    groupName = target.closest('.list-group-item').querySelector('[data-value="group-name"]').textContent
    taskGroupForm.elements['group_form-name'].value = groupName
    taskGroupForm.elements['task_group_id'].value = id
    taskGroupForm.elements['submit'].innerHTML = 'Update'
    showBSPopup('taskGroupModal')
}

/**
 * Resets values of the task group form
 */
function resetGroupForm() {
    taskGroupForm.elements['group_form-name'].value = ''
    taskGroupForm.elements['task_group_id'].value = ''
    taskGroupForm.elements['submit'].innerHTML = 'Create'
}

/**
 * Updates task group DOM value
 * @param {Number} id task group id
 * @param {String} name task group name
 */
function updateTaskGroupUI(id, name) {
    groupElm = document.getElementById(`taskGroup${id}`)
    groupElm.querySelector('[data-value="group-name"]').innerHTML = name
}

taskGroupForm.addEventListener('submit', (e) => {
    e.preventDefault()
    _this = taskGroupForm
    if (_this.elements['task_group_id'].value) {
        _renameGroup(new FormData(_this))
    } else {
        _this.submit()
    }
})


// fill offcanvas given task data
function fillOffcanvas(task) {
    modalTask.value = task.task;
    modalDueDate.value = task.due_date;

    if (task.completed) {
        modalCheck.checked = true;
        modalCompletedBy.innerHTML = `${task.completed_by_fname} ${task.completed_by_lname}`;
        modalDateCompleted.innerHTML = formatDate(task.date_completed);
        modalCompletedBy.parentElement.hidden = false;
    } else {
        modalCheck.checked = false;
        modalCompletedBy.innerHTML = '';
        modalDateCompleted.innerHTML = '';
        modalCompletedBy.parentElement.hidden = true;
    }
    
    modalCheck.setAttribute('onchange', `changeTaskStatus(${task.id}, true)`)
    modalCreatedBy.innerHTML = `${task.created_by_fname} ${task.created_by_lname}`;
    modalDateCreated.innerHTML = formatDate(task.date_created);
    taskCtUpdateForm.setAttribute('data-task-id', task.id);
    taskDdUpdateForm.setAttribute('data-task-id', task.id);
    modalDeleteTask.setAttribute('onclick', `deleteTask(${task.id})`);

    let callIconHTML = ''
    if (task.assigned_to_phone) {
        callIconHTML = `
        <a href="tel:${task.assigned_to_phone}" class="btn btn-outline-primary border-0 py-1 px-2">
            <i class="fa-solid fa-phone"></i>
        </a>`
    }

    let assignToHTML = `
    <a role="button" class="d-block" data-bs-toggle="modal" data-bs-target="#assignTaskModal">
        <i class="fa-solid fa-user-plus"></i>
        <span class="ms-2" id="assign_to">Assign to</span>
    </a>`

    if (task.assigned_to_fname) {
        let fullName = `${task.assigned_to_fname} ${task.assigned_to_lname}`;
        assignToHTML = `
        <span class="d-block text-muted">Assigned to:</span>
        <div class="d-flex justify-content-between gap-md">
            <div class="d-block" id="date_created">
                <p class="mb-0">${fullName}<span class="ms-1 hint">${task.assigned_to_business}</span></p>
                <a href="/events/${EVENT_ID}/chatroom/chat-with/${task.assigned_to_id}/" class="btn btn-outline-success border-0 py-1 px-2">
                    <i class="fa-solid fa-message"></i>
                </a>
                ${callIconHTML}
            </div>
            <button type="button" class="btn-close" title="Remove" onclick="assignTaskToRemove(${task.id})"></button>
        </div>`
    }
    assignedToElm.innerHTML = assignToHTML
}

// new HTML task element
function createTaskElm(task) {
    let taskDueDate = '';
    let taskGroup = '';
    let taskGroupContent = '';
    const activeGroup = document.getElementById('activeTaskGroup').value;

    if (task.due_date) {
        taskDueDate = `
        <span class="text-primary">
            <i class="fa-regular fa-calendar"></i>
            <span data-value="due-date">${task.due_date}</span>
        </span>`;
    }

    if (activeGroup == 'all') {
        taskGroup = 'Tasks';
        taskGroupContent = `
        <span class="text-muted">
            <i class="fa-solid fa-table-cells-large"></i>
            <span data-value="group-name">${taskGroup}</span>
        </span>`;

        if (task.task_group) {
            taskGroup = task.task_group;
        }
    }

    const taskContent = `
    <div class="card-body d-flex gap-lg">
        <span class="pt-1">
            <input type="checkbox" class="form-check-input rounded-circle" onchange="changeTaskStatus(this.closest('[data-task-id]').dataset.taskId)">
        </span>
        <div class="flex-grow-1" onclick="taskDetails(this.closest('[data-task-id]').dataset.taskId)">
            <p class="mb-0" data-value="task">${task.task}</p>
            <div class="d-flex gap-md">
                ${taskDueDate}
                ${taskGroupContent}
            </div>
        </div>
    </div>`;

    let newTaskElm = document.createElement('div');
    newTaskElm.setAttribute('class', 'card shadow-sm mb-2');
    newTaskElm.setAttribute('data-task-id', task.id);
    newTaskElm.innerHTML = taskContent;
    sectionTasks.appendChild(newTaskElm);
}