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

// new HTML task group element
function createTaskGroupElm(taskGroup) {

}