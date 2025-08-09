// Task Flow

// === Глобальные переменные ===
const TASK_FLOW = {
    csrfToken: null,
    boardId: null
};

// === Инициализация ===
document.addEventListener('DOMContentLoaded', function() {
    TASK_FLOW.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
    initTaskModal();
    initBoardActions();
    initDragAndDrop();
    initUserInvite();
    
    console.log('Task Flow initialized');
});

// === Модальное окно задач ===
function initTaskModal() {
    const taskModal = document.getElementById('taskModal');
    if (!taskModal) return;
    
    const taskStatusInput = document.getElementById('taskStatus');
    const saveTaskBtn = document.getElementById('saveTaskBtn');
    const taskForm = document.getElementById('taskForm');
    
    document.querySelectorAll('[data-bs-target="#taskModal"]').forEach(button => {
        button.addEventListener('click', function() {
            const status = this.getAttribute('data-status');
            if (taskStatusInput) {
                taskStatusInput.value = status;
            }

            if (taskForm) {
                taskForm.reset();
            }
        });
    });

    if (saveTaskBtn) {
        saveTaskBtn.addEventListener('click', function() {
            handleTaskSave();
        });
    }
}

// === Обработка сохранения задачи ===
function handleTaskSave() {
    const form = document.getElementById('taskForm');
    if (!form) return;
    
    const formData = new FormData(form);
    
    const title = formData.get('title');
    if (!title || title.trim() === '') {
        showAlert('Введите название задачи', 'warning');
        return;
    }

    const boardId = window.location.pathname.split('/')[1];
    if (!boardId) {
        showAlert('Ошибка: не найден ID доски', 'danger');
        return;
    }
    
    const taskData = {
        title: formData.get('title'),
        description: formData.get('description') || '',
        status: formData.get('status'),
        assignee: formData.get('assignee') || null
    };

    makeAjaxRequest(`/tasks/board/${boardId}/create/`, 'POST', taskData)
        .then(response => {
            if (response.success) {
                const taskModal = document.getElementById('taskModal');
                if (taskModal) {
                    const modal = bootstrap.Modal.getInstance(taskModal);
                    if (modal) {
                        modal.hide();
                    }
                }
                
                showAlert('Задача создана!', 'success');

                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                showAlert(`Ошибка: ${response.error}`, 'danger');
            }
        })
        .catch(error => {
            showAlert('Ошибка при создании задачи', 'danger');
        });
}

// === Действия с досками ===
function initBoardActions() {

    document.querySelectorAll('[data-confirm-delete]').forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm-delete') || 'Удалить этот элемент?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    document.querySelectorAll('.task-card, .board-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('shadow-hover');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-hover');
        });
    });
}

// === Утилиты ===
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    alertContainer.insertBefore(alertDiv, alertContainer.firstChild);

    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// === AJAX утилиты ===
function makeAjaxRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'X-CSRFToken': TASK_FLOW.csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    };
    
    if (data && method !== 'GET') {
        if (data instanceof FormData) {
            options.body = data;
        } else {
            options.headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(data);
        }
    }
    
    return fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('AJAX request failed:', error);
            showAlert('Произошла ошибка при выполнении запроса', 'danger');
            throw error;
        });
}

// === Drag & Drop ===
function initDragAndDrop() {
    const draggables = document.querySelectorAll('.draggable');
    const dropZones = document.querySelectorAll('.drop-zone');
    
    if (!draggables.length || !dropZones.length) {
        console.log('Drag & Drop elements not found');
        return;
    }

    draggables.forEach(draggable => {
        draggable.addEventListener('dragstart', handleDragStart);
        draggable.addEventListener('dragend', handleDragEnd);
    });

    dropZones.forEach(zone => {
        zone.addEventListener('dragover', handleDragOver);
        zone.addEventListener('dragenter', handleDragEnter);
        zone.addEventListener('dragleave', handleDragLeave);
        zone.addEventListener('drop', handleDrop);
    });
    
    console.log('Drag & Drop initialized');
}

let draggedElement = null;

function handleDragStart(e) {
    draggedElement = this;
    this.classList.add('dragging');

    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.outerHTML);
    e.dataTransfer.setData('text/plain', this.dataset.taskId);
    
    console.log('Drag started for task:', this.dataset.taskId);
}

function handleDragEnd(e) {
    this.classList.remove('dragging');

    document.querySelectorAll('.drop-zone').forEach(zone => {
        zone.classList.remove('drag-over');
    });
    
    draggedElement = null;
    console.log('Drag ended');
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    
    e.dataTransfer.dropEffect = 'move';
    return false;
}

function handleDragEnter(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }

    const currentStatus = draggedElement?.dataset.status;
    const targetStatus = this.dataset.status;
    
    if (currentStatus !== targetStatus) {
        this.classList.add('drag-over');
    }
    
    return false;
}

function handleDragLeave(e) {
    const rect = this.getBoundingClientRect();
    const x = e.clientX;
    const y = e.clientY;
    
    if (x < rect.left || x >= rect.right || y < rect.top || y >= rect.bottom) {
        this.classList.remove('drag-over');
    }
}

function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    const taskId = e.dataTransfer.getData('text/plain');
    const newStatus = this.dataset.status;
    const currentStatus = draggedElement?.dataset.status;

    this.classList.remove('drag-over');

    if (currentStatus === newStatus) {
        console.log('Task dropped in the same column');
        return false;
    }
    
    console.log(`Moving task ${taskId} from ${currentStatus} to ${newStatus}`);

    updateTaskStatus(taskId, newStatus);
    
    return false;
}

function updateTaskStatus(taskId, newStatus) {
    const url = `/tasks/${taskId}/update-status/`;
    
    makeAjaxRequest(url, 'POST', { status: newStatus })
        .then(response => {
            if (response.success) {
                showAlert(response.message, 'success');

                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                showAlert(`Ошибка: ${response.error}`, 'danger');
            }
        })
        .catch(error => {
            showAlert('Ошибка при перемещении задачи', 'danger');
            console.error('Error updating task status:', error);
        });
}

// === Приглашение пользователей ===
function initUserInvite() {
    const userSelectButtons = document.querySelectorAll('.user-select-btn');
    if (!userSelectButtons.length) return;

    userSelectButtons.forEach(button => {
        button.addEventListener('click', function() {
            const username = this.getAttribute('data-username');
            const usernameInput = document.getElementById('id_username');
            
            if (usernameInput) {
                usernameInput.value = username;

                userSelectButtons.forEach(btn => {
                    btn.classList.remove('btn-primary');
                    btn.classList.add('btn-outline-secondary');
                });
                
                this.classList.remove('btn-outline-secondary');
                this.classList.add('btn-primary');
            }
        });
    });

    const usernameInput = document.getElementById('id_username');
    if (usernameInput) {
        usernameInput.addEventListener('input', function() {
            userSelectButtons.forEach(btn => {
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-outline-secondary');
            });
        });
    }
    
    console.log('User invite functionality initialized');
}

window.TASK_FLOW = TASK_FLOW;
window.showAlert = showAlert;
window.makeAjaxRequest = makeAjaxRequest;
