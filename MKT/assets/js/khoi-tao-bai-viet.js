// loading-transition.js

/**
 * Xử lý chuyển đổi từ Trạng thái Thiết lập (Input) sang Trạng thái Loading.
 * Hiển thị spinner lớn và khóa giao diện theo yêu cầu thiết kế.
 */
function transitionToLoadingState() {
    console.log("🚀 Bắt đầu chuyển sang trạng thái Loading...");

    // 1. Định nghĩa các Selector
    const rightColumn = document.querySelector('.column.right');
    const leftColumn = document.querySelector('.column.left'); // Hoặc input cụ thể
    const elementsToHide = document.querySelectorAll(
        '.video-placeholder, .preview-text, #generateBtn, #previewLength, .guide-btn'
    );
    const existingLoading = document.getElementById('loading'); // Spinner nhỏ cũ

    // 2. Vô hiệu hóa tương tác bên trái
    if (leftColumn) {
        // leftColumn.style.opacity = '0.5'; // User requested no dimming
        leftColumn.style.pointerEvents = 'none'; // Chặn click

        // Vô hiệu hóa cụ thể các input
        const inputs = leftColumn.querySelectorAll('input, select, textarea, button');
        inputs.forEach(input => input.disabled = true);
    }

    // 3. Ẩn nội dung bên phải mặc định
    elementsToHide.forEach(el => {
        if (el) el.style.display = 'none';
    });
    if (existingLoading) existingLoading.style.display = 'none'; // Đảm bảo spinner cũ biến mất

    // 4. Chèn UI Loading Lớn Mới
    // Kiểm tra xem đã chèn chưa để tránh trùng lặp
    let bigLoading = document.getElementById('fullscreen-loading-state');
    if (!bigLoading) {
        bigLoading = document.createElement('div');
        bigLoading.id = 'fullscreen-loading-state';
        bigLoading.className = 'loading-state-container';
        bigLoading.innerHTML = `
            <div class="spinner-large-container">
                <svg class="spinner-circle" viewBox="0 0 50 50">
                    <!-- Vòng tròn nền (Xanh nhạt) -->
                    <circle class="spinner-track" cx="25" cy="25" r="20" fill="none" stroke-width="4"></circle>
                    <!-- Vòng tròn xoay (Xanh đậm) -->
                    <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="4"></circle>
                </svg>
            </div>
            <h3 class="loading-title">Dàn ý đang được khởi tạo...</h3>
            <p class="loading-desc">Hệ thống đang xử lý thông tin và sắp xếp nội dung.<br>Vui lòng chờ trong giây lát.</p>
        `;
        // Append vào cột phải
        if (rightColumn) {
            rightColumn.appendChild(bigLoading);
            rightColumn.classList.add('flex-centered'); // Class hỗ trợ căn giữa
        }
    } else {
        bigLoading.style.display = 'flex';
    }

    // 5. Cuộn tới vị trí giữa view nếu cần
    bigLoading.scrollIntoView({ behavior: 'smooth', block: 'center' });

    console.log("✅ Chuyển đổi hoàn tất. UI đã khóa.");
}

/**
 * Xử lý chuyển hướng sang trang Thinking sau khi API/Xử lý hoàn tất
 */
function redirectToThinkingPage(delay = 1000) {
    console.log(`⏱️ Đang chờ ${delay}ms trước khi chuyển trang Thinking...`);
    setTimeout(() => {
        window.location.href = 'thinking.php';
    }, delay);
}

// Export global
window.transitionToLoadingState = transitionToLoadingState;
window.redirectToThinkingPage = redirectToThinkingPage;
