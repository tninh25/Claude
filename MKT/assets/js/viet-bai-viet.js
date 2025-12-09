document.addEventListener('DOMContentLoaded', () => {
    // --- MOCK DATA FOR USER SECTIONS (To simulate what user added) ---
    const initialUserSections = [
        "Ưu tiên xử lý tại chỗ (Edge AI)",
        "Bảo mật thông minh",
        "Làm việc lại tối ưu",
        "Tự động hóa sâu",
        "Tối ưu chi phí vận hành"
    ];

    const userSectionsContainer = document.getElementById('user-sections-container');
    const addSectionBtn = document.getElementById('add-section-btn');
    const popup = document.getElementById('ai-popup');
    const closePopupBtn = document.querySelector('.close-popup');
    const textPreview = document.querySelector('.selected-text-preview');
    const contextMenu = document.getElementById('custom-context-menu');
    const ctxChatAi = document.getElementById('ctx-chat-ai');


    // Function to create a section element
    function createSectionElement(title, isNew = false) {
        const div = document.createElement('div');
        div.className = 'content-section';
        div.innerHTML = `
            <div class="section-header">
                <span contenteditable="${isNew}">${title}</span>
                <div style="display:flex; gap:10px; align-items:center;">
                    <i class="fas fa-trash-alt delete-icon" style="color:#EF4444; font-size:12px; cursor:pointer; opacity:0.5; transition:opacity 0.2s;" title="Xóa"></i>
                    <i class="fas fa-chevron-down toggle-icon" style="color:#9CA3AF; font-size:12px;"></i>
                </div>
            </div>
            <div class="section-body" contenteditable="true" style="padding: 20px; color: var(--text-sub); line-height: 1.6; outline:none;">
                <p>Nội dung cho mục này...</p>
            </div>
        `;

        // Delete Logic
        const delBtn = div.querySelector('.delete-icon');
        delBtn.addEventListener('mouseenter', () => delBtn.style.opacity = 1);
        delBtn.addEventListener('mouseleave', () => delBtn.style.opacity = 0.5);
        delBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (confirm('Bạn có chắc muốn xóa mục này?')) {
                div.remove();
            }
        });

        // Toggle Logic
        const header = div.querySelector('.section-header');
        header.addEventListener('click', (e) => {
            if (e.target.classList.contains('delete-icon')) return; // Ignore delete click
            if (e.target.getAttribute('contenteditable') === 'true') return; // Ignore editing title

            div.classList.toggle('expanded');

            const icon = div.querySelector('.toggle-icon');
            if (div.classList.contains('expanded')) {
                icon.classList.remove('fa-chevron-down');
                icon.classList.add('fa-chevron-up');
            } else {
                icon.classList.remove('fa-chevron-up');
                icon.classList.add('fa-chevron-down');
            }
        });

        return div;
    }

    // Render Initial Sections
    if (userSectionsContainer) {
        initialUserSections.forEach(title => {
            userSectionsContainer.appendChild(createSectionElement(title));
        });
    }

    // Add New Section Logic
    if (addSectionBtn) {
        addSectionBtn.addEventListener('click', () => {
            const newSection = createSectionElement("Nhập tiêu đề mới...", true);
            userSectionsContainer.appendChild(newSection);
            // Auto expand
            newSection.classList.add('expanded');
            newSection.querySelector('.toggle-icon').classList.replace('fa-chevron-down', 'fa-chevron-up');
            // Focus on title
            const titleSpan = newSection.querySelector('.section-header span');
            titleSpan.focus();
            // Select all text for easy replacement
            document.execCommand('selectAll', false, null);
        });
    }


    // --- LOAD PIPELINE DATA ---
    function loadPipelineData() {
        const raw = sessionStorage.getItem('pipelineData');
        if (raw) {
            try {
                const data = JSON.parse(raw);
                if (data.config && data.config.title) {
                    const titleInput = document.querySelector('.article-title-input');
                    if (titleInput) titleInput.value = data.config.title;
                }
                if (data.private_data && data.private_data.text && data.private_data.text.trim().length > 0) {
                    const firstSectionBody = document.querySelector('.content-section.expanded .section-body'); // The main one
                    if (firstSectionBody) {
                        const pText = data.private_data.text.split('\n').map(line => line.trim() ? `<p style="margin-bottom: 20px;">${line}</p>` : '').join('');
                        firstSectionBody.innerHTML = pText;
                    }
                }
            } catch (e) {
                console.error("Error parsing pipeline data", e);
            }
        }
    }
    loadPipelineData();

    // 1. Toggle Content Sections (Legacy for the first static section)
    const staticHeader = document.querySelector('.content-section.expanded .section-header');
    if (staticHeader) {
        staticHeader.addEventListener('click', () => {
            const section = staticHeader.parentElement;
            section.classList.toggle('expanded');
            // Icon handled by CSS or existing logic, but let's be safe
            const icon = staticHeader.querySelector('.fa-chevron-up, .fa-chevron-down');
            if (section.classList.contains('expanded')) {
                if (icon && icon.classList.contains('fa-chevron-down')) {
                    icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
                }
            } else {
                if (icon && icon.classList.contains('fa-chevron-up')) {
                    icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
                }
            }
        });
    }

    // 2. Tab Switching
    const tabs = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            tabContents.forEach(c => c.style.display = 'none');
            const target = tab.dataset.target;
            const targetEl = document.getElementById(`tab-${target}`);
            if (targetEl) targetEl.style.display = 'block';
        });
    });

    // 3. Right Sidebar Accordions
    const infoHeaders = document.querySelectorAll('.info-header');
    infoHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const accordion = header.parentElement;
            const content = accordion.querySelector('.info-content');
            const icon = header.querySelector('.fa-chevron-up, .fa-chevron-down');
            accordion.classList.toggle('active');
            content.classList.toggle('open');
            if (content.classList.contains('open')) {
                if (icon && icon.classList.contains('fa-chevron-down')) {
                    icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
                }
            } else {
                if (icon && icon.classList.contains('fa-chevron-up')) {
                    icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
                }
            }
        });
    });

    // 4. Floating AI Popup Functions
    function showPopup(rect, text) {
        if (!popup) return;

        // Update Original Text
        const originalBox = popup.querySelector('.original-text-box');
        if (originalBox) {
            // Limit length for display
            originalBox.textContent = text.length > 150 ? text.substring(0, 150) + '...' : text;
        }

        // Update Result Box (Mockup logic: just repeat text for now or show a "Thinking..." state)
        // In a real app, you'd call an API here. For design matching, we'll put some dummy text or the same text.
        const resultBox = popup.querySelector('.ai-result-box');
        if (resultBox) {
            // Check if we already have content? For demo, we'll just set a placeholder or a 'rewritten' version
            resultBox.textContent = "AI đang viết lại: " + (text.length > 50 ? text.substring(0, 50) + '...' : text);
        }

        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const scrollLeft = window.scrollX || document.documentElement.scrollLeft;

        // Position: slightly below the selection
        const top = rect.bottom + scrollTop + 10;
        const left = rect.left + scrollLeft;

        // Ensure it doesn't go off screen (simple check)
        // popup width is ~400px
        const headerHeight = 60; // Approx

        popup.style.top = `${top}px`;
        popup.style.left = `${left}px`;
        popup.style.display = 'block';

        // Auto-focus input
        const input = popup.querySelector('input');
        if (input) input.focus();
    }

    function hidePopup() {
        if (popup) popup.style.display = 'none';
    }

    if (closePopupBtn) {
        closePopupBtn.addEventListener('click', hidePopup);
    }

    // --- CONTEXT MENU LOGIC ---
    let lastSelectionRange = null;
    let lastSelectionText = "";

    // 1. Prevent default right-click on editable areas and show custom menu
    document.addEventListener('contextmenu', (e) => {
        let node = e.target;
        let isEditable = false;

        while (node) {
            // Check if clicking inside an editable content section directly or its child
            // Use try-catch or simple check to avoid errors on text nodes
            if (node.nodeType === 1 && node.getAttribute('contenteditable') === 'true') {
                isEditable = true;
                break;
            }
            if (node.parentNode) {
                node = node.parentNode;
            } else {
                break;
            }
        }

        const selection = window.getSelection();

        // Ensure we are selecting text
        if (isEditable && !selection.isCollapsed) {
            e.preventDefault();
            // Store the selection immediately
            lastSelectionRange = selection.getRangeAt(0).cloneRange();
            lastSelectionText = selection.toString();

            // Position menu
            const x = e.pageX;
            const y = e.pageY;

            if (contextMenu) {
                contextMenu.style.left = `${x}px`;
                contextMenu.style.top = `${y}px`;
                contextMenu.style.display = 'block';
            }
        } else {
            if (contextMenu && contextMenu.style.display === 'block') {
                contextMenu.style.display = 'none';
            }
        }
    });

    // 2. Hide context menu on click elsewhere
    document.addEventListener('click', (e) => {
        if (contextMenu && contextMenu.style.display === 'block') {
            contextMenu.style.display = 'none';
        }
    });

    // 3. Handle "Chat AI" click
    if (ctxChatAi) {
        ctxChatAi.addEventListener('click', (e) => {
            // Use stored selection instead of live selection
            if (lastSelectionRange && lastSelectionText) {
                const rect = lastSelectionRange.getBoundingClientRect();
                showPopup(rect, lastSelectionText);
            }
        });
    }

});