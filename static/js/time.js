let isEditing = false;
const API_ENDPOINT = '/times';
const cellFields = ['id', 'startAt'];
const createCellFields = ['', createInput()];

function createBody(inputs) {
    return {
        startAt: inputs[0].value,
    };
}

document.addEventListener('DOMContentLoaded', function() {
    loadTimes();
    
    // 시간 추가 버튼 클릭 이벤트
    document.getElementById('add-button').addEventListener('click', function() {
        addInputRow();
    });
});

// 시간 목록 로드
async function loadTimes() {
    try {
        const response = await fetch('/times/');
        const times = await response.json();
        
        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = '';
        
        times.forEach(time => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${time.id}</td>
                <td>${time.startAt}</td>
                <td>
                    <button class="btn btn-danger btn-sm" onclick="deleteTime(${time.id})">삭제</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('시간 목록을 불러오는데 실패했습니다:', error);
    }
}

// 입력 행 추가
function addInputRow() {
    const tableBody = document.getElementById('table-body');
    const row = document.createElement('tr');
    
    row.innerHTML = `
        <td></td>
        <td>
            <input type="time" class="form-control" required>
        </td>
        <td>
            <button class="btn btn-success btn-sm mr-2" onclick="saveTime(this)">저장</button>
            <button class="btn btn-secondary btn-sm" onclick="cancelAdd(this)">취소</button>
        </td>
    `;
    
    tableBody.appendChild(row);
}

// 새로운 시간 저장
async function saveTime(button) {
    const row = button.closest('tr');
    const timeInput = row.querySelector('input[type="time"]');
    
    if (!timeInput.value) {
        alert('시간을 입력해주세요.');
        return;
    }
    
    try {
        const response = await fetch('/times/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                startAt: timeInput.value
            })
        });
        
        if (response.ok) {
            loadTimes();  // 목록 새로고침
        } else {
            const errorData = await response.json();
            alert('시간 추가에 실패했습니다: ' + (errorData.detail || ''));
        }
    } catch (error) {
        console.error('시간 추가 중 오류 발생:', error);
        alert('시간 추가 중 오류가 발생했습니다.');
    }
}

// 시간 삭제
async function deleteTime(id) {
    if (!confirm('정말로 이 시간을 삭제하시겠습니까?')) {
        return;
    }
    
    try {
        const response = await fetch(`/times/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadTimes();  // 목록 새로고침
        } else {
            alert('시간 삭제에 실패했습니다.');
        }
    } catch (error) {
        console.error('시간 삭제 중 오류 발생:', error);
        alert('시간 삭제 중 오류가 발생했습니다.');
    }
}

// 추가 취소
function cancelAdd(button) {
    const row = button.closest('tr');
    row.remove();
}

function createInput() {
    const input = document.createElement('input');
    input.type = 'time'
    input.className = 'form-control';
    return input;
}

function createActionButton(label, className, eventListener) {
    const button = document.createElement('button');
    button.textContent = label;
    button.classList.add('btn', className, 'mr-2');
    button.addEventListener('click', eventListener);
    return button;
}

function saveRow(event) {
    const row = event.target.parentNode.parentNode;
    const inputs = row.querySelectorAll('input');
    const body = createBody(inputs);

    requestCreate(body)
        .then(() => {
            location.reload();
        })
        .catch(error => console.error('Error:', error));

    isEditing = false;  // isEditing 값을 false로 설정
}

function deleteRow(event) {
    const row = event.target.closest('tr');
    const id = row.cells[0].textContent;

    requestDelete(id)
        .then(() => row.remove())
        .catch(error => console.error('Error:', error));
}


// request

function requestCreate(data) {
    const requestOptions = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    };

    return fetch(API_ENDPOINT, requestOptions)
        .then(response => {
            if (response.status === 200) return response.json();
            throw new Error('Create failed');
        });
}

function requestRead() {
    return fetch(API_ENDPOINT)
        .then(response => {
            if (response.status === 200) return response.json();
            throw new Error('Read failed');
        });
}

function requestDelete(id) {
    const requestOptions = {
        method: 'DELETE',
    };

    return fetch(`${API_ENDPOINT}/${id}`, requestOptions)
        .then(response => {
            if (response.status !== 200) throw new Error('Delete failed');
        });
}
