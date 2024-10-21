var subtaskCounter = 1;

function addSubtask() {
    var subtaskDiv = document.createElement('div');
    subtaskDiv.classList.add('subtask_block');
    var subtaskInput = document.createElement('input');
    subtaskInput.type = 'text';
    subtaskInput.name = 'subtask_title_' + subtaskCounter;
    subtaskInput.placeholder = 'Введіть підпункт';
    var subDeleteIcon = document.createElement('i');
    subDeleteIcon.classList.add('delete_left', 'fa-solid', 'fa-delete-left');
    subDeleteIcon.onclick = function () {
        removeSubtask(this);
    };
    subtaskDiv.appendChild(subtaskInput);
    subtaskDiv.appendChild(subDeleteIcon);
    document.getElementById('subtasks').appendChild(subtaskDiv);
    subtaskCounter++;
}

function removeSubtask(icon) {
    icon.parentNode.remove();
}

let isButtonClicked = false;

function openEditMenu(todoId) {
    isButtonClicked = !isButtonClicked;
    let edit_menu = document.getElementById(`edit_notation_block_${todoId}`);

    if (isButtonClicked) {
        edit_menu.style.visibility = 'visible';
        edit_menu.style.opacity = '1';
    } else {
        edit_menu.style.visibility = 'hidden';
        edit_menu.style.opacity = '0';
    }
}

function closeEditMenu(todoId) {
    let edit_menu = document.getElementById(`edit_notation_block_${todoId}`)

    edit_menu.style.visibility = 'hidden';
    edit_menu.style.opacity = '0';
}

var subtaskEditCounter = 1;

function addEditSubtask(todoId) {
    var subtaskEditDiv = document.createElement('div');
    subtaskEditDiv.classList.add('subtask_edit_block');
    var subtaskEditInput = document.createElement('input');
    subtaskEditInput.type = 'text';
    subtaskEditInput.name = 'subtask_title_' + todoId + subtaskEditCounter;
    subtaskEditInput.placeholder = 'Введіть підпункт';
    var subEditIcon = document.createElement('i');
    subEditIcon.classList.add('edit_left', 'fa-solid', 'fa-delete-left');
    subEditIcon.onclick = function () {
        removeEditSubtask(this);
    };
    subtaskEditDiv.appendChild(subtaskEditInput);
    subtaskEditDiv.appendChild(subEditIcon);

    document.getElementById(`subtasks_el_${todoId}`).appendChild(subtaskEditDiv);
    subtaskEditCounter++;
}

function removeEditSubtask(icon) {
    const subtaskInput = icon.parentNode.querySelector('input');
    subtaskInput.value = ''; // Очистити значення текстового поля підпункту
}

document.getElementById('add_notation').addEventListener('click', function () {
    let add_menu = document.getElementById('add_notations_block')

    add_menu.style.visibility = 'visible';
    add_menu.style.opacity = '1';
})

document.getElementById('close_add').addEventListener('click', function () {
    let add_menu = document.getElementById('add_notations_block')

    add_menu.style.visibility = 'hidden';
    add_menu.style.opacity = '0';
})


const notationBlocks = document.querySelectorAll('.notation_block');

// Проходження через кожен блок нотаток та встановлення min-height для edit_notation_block
notationBlocks.forEach((block) => {
  const editNotationBlock = block.querySelector('.edit_notation_block');
  editNotationBlock.style.minHeight = `${block.offsetHeight}px`;
});