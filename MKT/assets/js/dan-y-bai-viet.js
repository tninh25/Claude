// Khởi tạo dữ liệu outline - có thể lấy từ server hoặc localStorage
let outlineData = [];
let editMode = null;
let sortableInstance = null;

// Hàm khởi tạo dữ liệu mặc định hoặc lấy từ nguồn khác
function initOutlineData() {
    // Có thể lấy từ localStorage
    const saved = localStorage.getItem('outlineData');
    if (saved) {
        outlineData = JSON.parse(saved);
        // Ensure keywords support (migration)
        outlineData.forEach(item => {
            if (!item.keywords) {
                item.keywords = item.keyword ? [item.keyword] : [];
            }
        });
    } else {
        // Dữ liệu mặc định
        outlineData = [
            { id: 1, title: 'Máy tính AI lên ngôi', open: false, length: 50, keywords: ['AI doanh nghiệp'], link: true },
            { id: 2, title: 'Ưu tiên xử lý tại chỗ (Edge AI)', open: false, length: 50, keywords: [], link: true },
            { id: 3, title: 'Bảo mật thông minh', open: false, length: 50, keywords: [], link: true },
            { id: 4, title: 'Làm việc lai tối ưu', open: false, length: 50, keywords: [], link: true },
            { id: 5, title: 'Tự động hóa sâu', open: false, length: 50, keywords: [], link: true },
            { id: 6, title: 'Tối ưu chi phí vận hành', open: false, length: 50, keywords: [], link: true }
        ];
    }
}

// Hàm lưu dữ liệu
function saveOutlineData() {
    localStorage.setItem('outlineData', JSON.stringify(outlineData));
}

function renderOutline() {
    const list = document.getElementById('outlineList');
    if (!list) return;

    list.innerHTML = outlineData.map((item, index) => `
        <div class="outline-item" data-id="${item.id}" data-index="${index}">
            <div class="outline-item-header" onclick="toggleItem(${item.id})">
                <div class="outline-item-left">
                    <svg class="drag-handle" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"/>
                    </svg>
                    <svg class="chevron ${item.open ? 'open' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                    </svg>
                    <div class="item-title">
                        ${editMode === item.id ?
            `<input type="text" value="${item.title}" 
                                onblur="saveTitle(${item.id}, this.value)" 
                                onkeydown="if(event.key==='Enter') this.blur()"
                                onclick="event.stopPropagation()" 
                                autofocus>`
            : item.title
        }
                    </div>
                    <span class="h-badges">H2</span>
                </div>
                <div class="outline-item-right">
                    <button class="action-icon" onclick="event.stopPropagation(); editTitle(${item.id})">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                        </svg>
                    </button>
                    <button class="action-icon delete" onclick="event.stopPropagation(); deleteItem(${item.id})">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="outline-item-body ${item.open ? 'show' : ''}">
                <div class="body-row">
                    <label class="body-label">Tỷ lệ độ dài:</label>
                    <div class="range-control">
                        <input type="range" min="0" max="100" value="${item.length}" 
                            oninput="updateLength(${item.id}, this.value, this)"
                            style="background: linear-gradient(to right, #3b82f6 0%, #3b82f6 ${item.length}%, #e2e8f0 ${item.length}%, #e2e8f0 100%);">
                        <span class="range-value" id="length-${item.id}">${item.length}%</span>
                    </div>
                </div>
                <div class="body-row" style="align-items: flex-start">
                    <label class="body-label" style="margin-top: 10px;">Keyword tùy chỉnh:</label>
                    <div class="keyword-section">
                        <input type="text" class="body-input" 
                            placeholder="Nhập từ khóa và nhấn Enter để thêm"
                            onkeydown="handleKeywordEnter(${item.id}, event)">
                        <div class="keyword-tags">
                            ${(item.keywords || []).map((kw, idx) => `
                                <span class="keyword-tag">
                                    ${kw}
                                    <span class="remove-tag" onclick="removeKeyword(${item.id}, ${idx})">×</span>
                                </span>
                            `).join('')}
                        </div>
                    </div>
                </div>
                <div class="body-row">
                    <label class="body-label">Liên kết nội bộ:</label>
                    <div class="toggle-row">
                        <label class="switch">
                            <input type="checkbox" ${item.link ? 'checked' : ''} 
                                onchange="updateLink(${item.id}, this.checked)">
                            <span class="switch-slider"></span>
                        </label>
                    </div>
                </div>
            </div>
        </div>
    `).join('');

    // Initialize Sortable if not already done
    if (!sortableInstance) {
        sortableInstance = new Sortable(list, {
            animation: 150,
            handle: '.drag-handle',
            ghostClass: 'sortable-ghost',
            dragClass: 'sortable-drag',
            onEnd: function (evt) {
                // Update array
                const item = outlineData.splice(evt.oldIndex, 1)[0];
                outlineData.splice(evt.newIndex, 0, item);
                saveOutlineData();
            }
        });
    }
}

function handleKeywordEnter(id, event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const value = event.target.value.trim();
        if (value) {
            addKeyword(id, value);
            event.target.value = ''; // Clear input
        }
    }
}

function addKeyword(id, text) {
    const item = outlineData.find(i => i.id === id);
    if (item) {
        if (!item.keywords) item.keywords = [];
        item.keywords.push(text);
        renderOutline();
        saveOutlineData();
    }
}

function removeKeyword(id, index) {
    const item = outlineData.find(i => i.id === id);
    if (item && item.keywords) {
        item.keywords.splice(index, 1);
        renderOutline();
        saveOutlineData();
    }
}

function toggleItem(id) {
    if (editMode) return;
    const item = outlineData.find(i => i.id === id);
    if (item) {
        item.open = !item.open;
        renderOutline();
        saveOutlineData();
    }
}

function editTitle(id) {
    editMode = id;
    renderOutline();
}

function saveTitle(id, value) {
    const item = outlineData.find(i => i.id === id);
    if (item && value.trim()) {
        item.title = value.trim();
    }
    editMode = null;
    renderOutline();
    saveOutlineData();
}

function deleteItem(id) {
    const idx = outlineData.findIndex(i => i.id === id);
    if (idx > -1) {
        outlineData.splice(idx, 1);
        renderOutline();
        saveOutlineData();
    }
}

function addOutlineItem() {
    const newId = outlineData.length > 0 ? Math.max(...outlineData.map(i => i.id)) + 1 : 1;
    outlineData.push({
        id: newId,
        title: 'Tiêu đề mới',
        open: false,
        length: 50,
        keywords: [],
        link: true
    });
    renderOutline();
    saveOutlineData();
}

function updateLength(id, value, slider) {
    const item = outlineData.find(i => i.id === id);
    if (item) {
        item.length = value;
        const valueEl = document.getElementById(`length-${id}`);
        if (valueEl) {
            valueEl.textContent = value + '%';
        }
        // Update slider background gradient
        if (slider) {
            slider.style.background = `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${value}%, #e2e8f0 ${value}%, #e2e8f0 100%)`;
        }
        saveOutlineData();
    }
}

function updateLink(id, checked) {
    const item = outlineData.find(i => i.id === id);
    if (item) {
        item.link = checked;
        saveOutlineData();
    }
}

// Khởi tạo khi load trang
document.addEventListener('DOMContentLoaded', function () {
    initOutlineData();
    renderOutline();
});
