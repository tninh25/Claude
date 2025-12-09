// ============================================
// 1. HẰNG SỐ & BIẾN TOÀN CỤC
// ============================================
const STORAGE_KEY = 'selected_files_v1';

let selectedFiles = [];

// ============================================
// 2. HÀM HỖ TRỢ AN TOÀN
// ============================================

// Gọi hàm an toàn (không crash khi hàm chưa tồn tại)
function safeCall(fn, ...args) {
    if (typeof fn === 'function') {
        try {
            return fn(...args);
        } catch (e) {
            console.error('Lỗi khi gọi hàm:', fn?.name, e);
        }
    }
}

// Lấy phần tử DOM an toàn
function $(selector) {
    try {
        return document.querySelector(selector);
    } catch {
        return null;
    }
}

// Parse JSON an toàn
function safeJSONParse(str, fallback = []) {
    try {
        return JSON.parse(str);
    } catch {
        return fallback;
    }
}

// ============================================
// 3. KHỞI TẠO TRANG CHÍNH
// ============================================
async function initializePage() {
    console.log('⏳ Đang khởi tạo hệ thống...');

    // 1. Load cấu hình API (có chống lỗi)
    if (typeof loadConfigs === 'function') {
        try {
            await loadConfigs();
        } catch (e) {
            console.warn('⚠️ Lỗi khi loadConfigs:', e);
        }
    }

    // 2. Load dữ liệu đã lưu từ localStorage
    try {
        const savedFiles = localStorage.getItem(STORAGE_KEY);
        if (savedFiles) {
            selectedFiles = safeJSONParse(savedFiles, []);
        }
    } catch (e) {
        console.warn('⚠️ Lỗi localStorage:', e);
        selectedFiles = [];
    }

    // 3. Khởi tạo các module giao diện
    safeCall(updateSubtabStates);
    safeCall(initializeKeywordTags);
    safeCall(initializeAiSuggest);
    safeCall(setupDraftSystem);
    safeCall(loadDraft);

    // 4. Tự động bấm tab đầu tiên có thể dùng
    setTimeout(() => {
        const firstSub = $('.sub[data-sub="file"]');

        if (firstSub && !firstSub.classList.contains('locked')) {
            firstSub.click();
        } else {
            const availableTab = $('.sub:not(.locked)');
            if (availableTab) {
                availableTab.click();
            }
        }
    }, 100);

    // 5. Cập nhật preview độ dài bài viết theo thời gian thực
    const lenInput = $('#article_length');

    if (lenInput) {
        const preview = $('#previewLength');

        lenInput.addEventListener('input', () => {
            if (preview) {
                preview.textContent = lenInput.value + ' từ';
            }
        });
    }

    // 6. Hiển thị thông báo khi sẵn sàng
    if (typeof showNotification === 'function') {
        showNotification('Hệ thống đã sẵn sàng!', 'info');
    }

    console.log('✅ Hệ thống đã sẵn sàng');
}

// ============================================
// 4. XỬ LÝ ĐÓNG / MỞ SIDEBAR
// ============================================
function initializeSidebarToggle() {
    const toggleBtn = $('.menu-toggle');
    const appContainer = $('.app-container');

    if (!toggleBtn || !appContainer) {
        console.warn('⚠️ Không tìm thấy phần tử sidebar');
        return;
    }

    toggleBtn.addEventListener('click', () => {
        appContainer.classList.toggle('sidebar-collapsed');
    });
}

// ============================================
// 5. CHẠY KHI DOM LOAD XONG
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    initializePage();
    initializeSidebarToggle();
});
