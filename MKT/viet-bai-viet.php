<?php require "thanh-dieu-huong.php" ?>
<link rel="stylesheet" href="./assets/css/thanh-dieu-huong.css">
<link rel="stylesheet" href="./assets/css/viet-bai-viet.css">
<!-- Icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Note: The included file may close body tags prematurely, but browsers often handle this by extending the body. 
     We verify the structure relies on app-body being open or flex. -->

<main class="main-content" style="flex:1;">
    <!-- Header -->
    <div class="page-header">
        <h1 class="page-title">Cấu hình bài viết</h1>
        <div class="step-indicator">Bước 3/3</div>
    </div>

    <!-- Tip Box -->
    <div class="tip-box">
        <span class="tip-icon"><i class="fas fa-lightbulb"></i></span>
        <span>Mẹo: Từ khóa chính càng cụ thể, AI sẽ tạo nội dung càng phù hợp với mục tiêu SEO của bạn.</span>
    </div>

    <!-- Main Grid -->
    <div class="editor-grid">
        <!-- Left Panel: Editor -->
        <div class="editor-panel">
            <input type="text" class="article-title-input" value="Xu hướng máy tính AI dành cho doanh nghiệp vừa và nhỏ">

            <!-- Toolbar -->
            <div class="toolbar">
                <div class="toolbar-group">
                    <button class="tool-btn"><i class="fas fa-undo"></i></button>
                    <button class="tool-btn"><i class="fas fa-redo"></i></button>
                </div>
                <div class="toolbar-group">
                    <button class="tool-btn"><i class="fas fa-print"></i></button>
                    <div class="tool-select" style="display:flex; align-items:center; gap:5px; border:1px solid #E5E7EB; border-radius:4px; padding:4px 8px;">
                        <span>Arial</span> <i class="fas fa-caret-down" style="font-size:10px"></i>
                    </div>
                </div>
                <div class="toolbar-group">
                    <div class="tool-btn" style="border:1px solid #E5E7EB; border-radius:4px 0 0 4px;">-</div>
                    <span style="padding:0 8px; font-size:13px; font-weight:500;">00</span>
                    <div class="tool-btn" style="border:1px solid #E5E7EB; border-radius:0 4px 4px 0;">+</div>
                </div>
                <div class="toolbar-group">
                    <button class="tool-btn"><b>B</b></button>
                    <button class="tool-btn"><i>I</i></button>
                    <button class="tool-btn"><u>U</u></button>
                    <button class="tool-btn"><i class="fas fa-strikethrough"></i></button>
                </div>
                <div class="toolbar-group">
                    <button class="tool-btn" style="color:#2563EB"><i class="fas fa-square"></i></button>
                    <button class="tool-btn"><i class="fas fa-font"></i></button>
                </div>
                <div class="toolbar-group">
                    <button class="tool-btn"><i class="fas fa-link"></i></button>
                    <button class="tool-btn"><i class="fas fa-image"></i></button>
                    <button class="tool-btn"><i class="fas fa-list-ul"></i></button>
                    <button class="tool-btn"><i class="fas fa-list-ol"></i></button>
                    <button class="tool-btn"><i class="fas fa-align-left"></i></button>
                    <button class="tool-btn"><i class="fas fa-align-center"></i></button>
                    <button class="tool-btn"><i class="fas fa-align-right"></i></button>
                </div>
            </div>

            <!-- Content Sections (Accordions) -->
            <div class="section-list">
                <!-- Section 1 (Expanded by default for demo) -->
                <div class="content-section expanded">
                    <div class="section-header">
                        <span>Máy tính AI lên ngôi</span>
                        <i class="fas fa-chevron-up" style="color:#9CA3AF; font-size:12px;"></i>
                    </div>
                    <div class="section-body" contenteditable="true" style="display:block; padding: 20px; color: var(--text-sub); line-height: 1.6; outline:none;">
                        <p id="demo-text-1" style="margin-bottom: 20px;">Máy tính AI đang trở thành xu hướng nổi bật khi doanh nghiệp ưu tiên hiệu năng cao và khả năng xử lý thông minh. Nhờ tích hợp mô hình AI trực tiếp trên thiết bị, máy tính AI giúp tăng tốc công việc, tối ưu dữ liệu và hỗ trợ ra quyết định nhanh hơn.</p>

                        <p style="margin-bottom: 20px;">Sự lên ngôi của máy tính AI đến từ nhu cầu tự động hóa và nâng cao trải nghiệm người dùng. Các tác vụ như phân tích dữ liệu, sáng tạo nội dung hay vận hành phần mềm đều được cải thiện rõ rệt, mang lại hiệu suất vượt trội cho đội ngũ doanh nghiệp.</p>

                        <p>Trong thời đại cạnh tranh số, máy tính AI trở thành công cụ cần thiết để doanh nghiệp nâng chuẩn vận hành. Với khả năng học hỏi liên tục và đáp ứng khối lượng công việc lớn, máy tính AI mở ra lợi thế mới cho những chiến lược tăng trưởng bền vững.</p>
                    </div>
                </div>

                <!-- Dynamic User Sections -->
                <div id="user-sections-container">
                    <!-- Javascript will populate this with the 'user added' sections -->
                </div>

                <!-- Add Section Button -->
                <button id="add-section-btn" class="add-section-btn">
                    <i class="fas fa-plus"></i> Thêm đoạn mới
                </button>
            </div>

            <!-- Bottom Text Area Placeholder -->
            <div style="margin-top:20px; color:#9CA3AF; font-size:14px;">
                Mô tả ngắn...
            </div>
        </div>

        <!-- Right Panel: Tools -->
        <div class="right-sidebar">
            <div class="tools-panel">
                <div class="tabs">
                    <button class="tab" data-tab="internet"><img src="./assets/images/icon-nguon-internet.png" alt="">Nguồn Internet</button>
                    <button class="tab active" data-tab="private"><img src="./assets/images/icon-du-lieu-rieng.png" alt=""> Dữ liệu riêng</button>
                </div>

                <!-- Tab: Media -->
                <div id="tab-media" class="tab-content" style="display: none;">
                    <div class="search-box">
                        <i class="fas fa-search search-icon"></i>
                        <input type="text" class="search-input" placeholder="Tìm hình theo từ khóa">
                    </div>

                    <div class="media-grid">
                        <?php
                        // Using placeholder images
                        $images = [
                            "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=200&h=200&fit=crop",
                            "https://images.unsplash.com/photo-1593642532744-9365ef14de66?w=200&h=200&fit=crop",
                            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=200&h=200&fit=crop",
                            "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=200&h=200&fit=crop"
                        ];
                        foreach ($images as $img) {
                        ?>
                            <div class="media-item">
                                <img src="<?php echo $img; ?>" alt="Media">
                            </div>
                        <?php } ?>
                    </div>
                </div>

                <!-- Tab: Smart Edit -->
                <div id="tab-smart-edit" class="tab-content">
                    <div class="ai-chat-area">
                        <div class="ai-message">
                            <div class="ai-avatar"><img src="./assets/images/stars.png" alt="AI"></div>
                            <div class="message-bubble">
                                Tôi có thể giúp gì cho bài viết này? Bạn có thể yêu cầu tôi viết lại, mở rộng hoặc kiểm tra chính tả!
                            </div>
                        </div>
                    </div>

                    <div class="suggestion-chips">
                        <button class="chip">Thêm FAQ</button>
                        <button class="chip">Tìm từ khóa SE...</button>
                    </div>

                    <div class="chat-input-wrapper">
                        <input type="text" placeholder="Nhập yêu cầu chỉnh sửa...">
                        <button class="send-btn"><i class="fas fa-paper-plane"></i></button>
                    </div>
                </div>
            </div>

            <!-- Accordions -->
            <div class="info-accordion active">
                <div class="info-header" onclick="this.parentElement.querySelector('.info-content').classList.toggle('open')">
                    <span style="display:flex; align-items:center; gap:8px;">
                        <i class="fas fa-chevron-up"></i>
                        Nguồn tham khảo
                    </span>
                    <span class="count">3 nguồn</span>
                </div>
                <div class="info-content open">
                    <div class="ref-item">
                        <div class="ref-dot"></div> Link số 1
                    </div>
                    <div class="ref-item">
                        <div class="ref-dot"></div> Link số 2
                    </div>
                    <div class="ref-item">
                        <div class="ref-dot"></div> Link số 3
                    </div>
                </div>
            </div>

            <div class="info-accordion">
                <div class="info-header" onclick="this.parentElement.querySelector('.info-content').classList.toggle('open')">
                    <span style="display:flex; align-items:center; gap:8px;">
                        <i class="fas fa-chevron-down"></i>
                        Đánh giá SEO
                    </span>
                    <span class="score">85 điểm</span>
                </div>
                <div class="info-content">
                    <div class="ref-item">Chi tiết đánh giá...</div>
                </div>
            </div>

        </div>
    </div>

    <!-- Floating AI Popup (Hidden by default) -->
    <div id="ai-popup" class="ai-popup" style="display: none;">
        <div class="popup-header">
            <span class="popup-title">AIS EDIT</span>
            <button class="close-popup"><i class="fas fa-times"></i></button>
        </div>
        <div class="popup-body">
            <p class="selected-text-preview" style="margin-bottom: 5px;">Nội dung đang chọn...</p>
            <div class="popup-actions" style="margin-bottom: 12px; font-size: 13px; color: var(--primary-blue); font-weight: 500;">
                <span style="cursor:pointer">Sao chép</span> <span style="color:#E5E7EB; margin:0 5px;">|</span> <span style="cursor:pointer">Thay vào bài viết</span>
            </div>
            <div class="chat-input-wrapper small">
                <input type="text" placeholder="Nhập yêu cầu chỉnh sửa...">
                <button class="send-btn"><i class="fas fa-paper-plane"></i></button>
            </div>
            <main class="main-content" style="flex:1;">
                <!-- Header -->
                <div class="page-header">
                    <h1 class="page-title">Cấu hình bài viết</h1>
                    <div class="step-indicator">Bước 3/3</div>
                </div>

                <!-- Tip Box -->
                <div class="tip-box">
                    <span class="tip-icon"><i class="fas fa-lightbulb"></i></span>
                    <span>Mẹo: Từ khóa chính càng cụ thể, AI sẽ tạo nội dung càng phù hợp với mục tiêu SEO của bạn.</span>
                </div>

                <!-- Main Grid -->
                <div class="editor-grid">
                    <!-- Left Panel: Editor -->
                    <div class="editor-panel">
                        <input type="text" class="article-title-input" value="Xu hướng máy tính AI dành cho doanh nghiệp vừa và nhỏ">

                        <!-- Toolbar -->
                        <div class="toolbar">
                            <div class="toolbar-group">
                                <button class="tool-btn"><i class="fas fa-undo"></i></button>
                                <button class="tool-btn"><i class="fas fa-redo"></i></button>
                            </div>
                            <div class="toolbar-group">
                                <button class="tool-btn"><i class="fas fa-print"></i></button>
                                <div class="tool-select" style="display:flex; align-items:center; gap:5px; border:1px solid #E5E7EB; border-radius:4px; padding:4px 8px;">
                                    <span>Arial</span> <i class="fas fa-caret-down" style="font-size:10px"></i>
                                </div>
                            </div>
                            <div class="toolbar-group">
                                <div class="tool-btn" style="border:1px solid #E5E7EB; border-radius:4px 0 0 4px;">-</div>
                                <span style="padding:0 8px; font-size:13px; font-weight:500;">00</span>
                                <div class="tool-btn" style="border:1px solid #E5E7EB; border-radius:0 4px 4px 0;">+</div>
                            </div>
                            <div class="toolbar-group">
                                <button class="tool-btn"><b>B</b></button>
                                <button class="tool-btn"><i>I</i></button>
                                <button class="tool-btn"><u>U</u></button>
                                <button class="tool-btn"><i class="fas fa-strikethrough"></i></button>
                            </div>
                            <div class="toolbar-group">
                                <button class="tool-btn" style="color:#2563EB"><i class="fas fa-square"></i></button>
                                <button class="tool-btn"><i class="fas fa-font"></i></button>
                            </div>
                            <div class="toolbar-group">
                                <button class="tool-btn"><i class="fas fa-link"></i></button>
                                <button class="tool-btn"><i class="fas fa-image"></i></button>
                                <button class="tool-btn"><i class="fas fa-list-ul"></i></button>
                                <button class="tool-btn"><i class="fas fa-list-ol"></i></button>
                                <button class="tool-btn"><i class="fas fa-align-left"></i></button>
                                <button class="tool-btn"><i class="fas fa-align-center"></i></button>
                                <button class="tool-btn"><i class="fas fa-align-right"></i></button>
                            </div>
                        </div>

                        <!-- Content Sections (Accordions) -->
                        <div class="section-list">
                            <!-- Section 1 (Expanded by default for demo) -->
                            <div class="content-section expanded">
                                <div class="section-header">
                                    <span>Máy tính AI lên ngôi</span>
                                    <i class="fas fa-chevron-up" style="color:#9CA3AF; font-size:12px;"></i>
                                </div>
                                <div class="section-body" contenteditable="true" style="display:block; padding: 20px; color: var(--text-sub); line-height: 1.6; outline:none;">
                                    <p id="demo-text-1" style="margin-bottom: 20px;">Máy tính AI đang trở thành xu hướng nổi bật khi doanh nghiệp ưu tiên hiệu năng cao và khả năng xử lý thông minh. Nhờ tích hợp mô hình AI trực tiếp trên thiết bị, máy tính AI giúp tăng tốc công việc, tối ưu dữ liệu và hỗ trợ ra quyết định nhanh hơn.</p>

                                    <p style="margin-bottom: 20px;">Sự lên ngôi của máy tính AI đến từ nhu cầu tự động hóa và nâng cao trải nghiệm người dùng. Các tác vụ như phân tích dữ liệu, sáng tạo nội dung hay vận hành phần mềm đều được cải thiện rõ rệt, mang lại hiệu suất vượt trội cho đội ngũ doanh nghiệp.</p>

                                    <p>Trong thời đại cạnh tranh số, máy tính AI trở thành công cụ cần thiết để doanh nghiệp nâng chuẩn vận hành. Với khả năng học hỏi liên tục và đáp ứng khối lượng công việc lớn, máy tính AI mở ra lợi thế mới cho những chiến lược tăng trưởng bền vững.</p>
                                </div>
                            </div>

                            <!-- Dynamic User Sections -->
                            <div id="user-sections-container">
                                <!-- Javascript will populate this with the 'user added' sections -->
                            </div>

                            <!-- Add Section Button -->
                            <button id="add-section-btn" class="add-section-btn">
                                <i class="fas fa-plus"></i> Thêm đoạn mới
                            </button>
                        </div>

                        <!-- Bottom Text Area Placeholder -->
                        <div style="margin-top:20px; color:#9CA3AF; font-size:14px;">
                            Mô tả ngắn...
                        </div>
                    </div>

                    <!-- Right Panel: Tools -->
                    <div class="right-sidebar">
                        <div class="tools-panel">
                            <div class="tabs">
                                <button class="tab-btn" data-target="media"><i class="far fa-image"></i> Media</button>
                                <button class="tab-btn active" data-target="smart-edit"><i class="fas fa-magic"></i> Sửa thông minh</button>
                            </div>

                            <!-- Tab: Media -->
                            <div id="tab-media" class="tab-content" style="display: none;">
                                <div class="search-box">
                                    <i class="fas fa-search search-icon"></i>
                                    <input type="text" class="search-input" placeholder="Tìm hình theo từ khóa">
                                </div>

                                <div class="media-grid">
                                    <?php
                                    // Using placeholder images
                                    $images = [
                                        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=200&h=200&fit=crop",
                                        "https://images.unsplash.com/photo-1593642532744-9365ef14de66?w=200&h=200&fit=crop",
                                        "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=200&h=200&fit=crop",
                                        "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=200&h=200&fit=crop"
                                    ];
                                    foreach ($images as $img) {
                                    ?>
                                        <div class="media-item">
                                            <img src="<?php echo $img; ?>" alt="Media">
                                        </div>
                                    <?php } ?>
                                </div>
                            </div>

                            <!-- Tab: Smart Edit -->
                            <div id="tab-smart-edit" class="tab-content">
                                <div class="ai-chat-area">
                                    <div class="ai-message">
                                        <div class="ai-avatar"><img src="./assets/images/stars.png" alt="AI"></div>
                                        <div class="message-bubble">
                                            Tôi có thể giúp gì cho bài viết này? Bạn có thể yêu cầu tôi viết lại, mở rộng hoặc kiểm tra chính tả!
                                        </div>
                                    </div>
                                </div>

                                <div class="suggestion-chips">
                                    <button class="chip">Thêm FAQ</button>
                                    <button class="chip">Tìm từ khóa SE...</button>
                                </div>

                                <div class="chat-input-wrapper">
                                    <input type="text" placeholder="Nhập yêu cầu chỉnh sửa...">
                                    <button class="send-btn"><i class="fas fa-paper-plane"></i></button>
                                </div>
                            </div>
                        </div>

                        <!-- Accordions -->
                        <div class="info-accordion active">
                            <div class="info-header" onclick="this.parentElement.querySelector('.info-content').classList.toggle('open')">
                                <span style="display:flex; align-items:center; gap:8px;">
                                    <i class="fas fa-chevron-up"></i>
                                    Nguồn tham khảo
                                </span>
                                <span class="count">3 nguồn</span>
                            </div>
                            <div class="info-content open">
                                <div class="ref-item">
                                    <div class="ref-dot"></div> Link số 1
                                </div>
                                <div class="ref-item">
                                    <div class="ref-dot"></div> Link số 2
                                </div>
                                <div class="ref-item">
                                    <div class="ref-dot"></div> Link số 3
                                </div>
                            </div>
                        </div>

                        <div class="info-accordion">
                            <div class="info-header" onclick="this.parentElement.querySelector('.info-content').classList.toggle('open')">
                                <span style="display:flex; align-items:center; gap:8px;">
                                    <i class="fas fa-chevron-down"></i>
                                    Đánh giá SEO
                                </span>
                                <span class="score">85 điểm</span>
                            </div>
                            <div class="info-content">
                                <div class="ref-item">Chi tiết đánh giá...</div>
                            </div>
                        </div>

                    </div>
                </div>

                <!-- Floating AI Popup (Hidden by default) -->
                <div id="ai-popup" class="ai-popup" style="display: none;">
                    <div class="popup-header">
                        <div class="popup-title">
                            <span class="brand">AIS</span>
                            <span class="brand-sub">EDIT</span>
                        </div>
                        <button class="close-popup"><i class="fas fa-times"></i></button>
                    </div>
                    <div class="popup-body">
                        <!-- Original Text (Faded) -->
                        <div class="original-text-box">
                            Máy tính AI đang trở thành xu hướng nổi bật khi doanh nghiệp ưu tiên hiệu năng cao...
                        </div>

                        <!-- AI Result Text -->
                        <div class="ai-result-box">
                            Máy tính AI đang vươn lên thành xu hướng chủ đạo khi doanh nghiệp ngày càng chú trọng hiệu năng...
                        </div>

                        <!-- Actions -->
                        <div class="popup-actions">
                            <span class="action-btn">Sao chép</span>
                            <span class="divider">|</span>
                            <span class="action-btn">Thay vào bài viết</span>
                        </div>

                        <!-- Input Area -->
                        <div class="chat-input-wrapper big">
                            <input type="text" placeholder="Nhập yêu cầu chỉnh sửa...">
                            <button class="send-btn"><i class="fas fa-paper-plane"></i></button>
                        </div>
                    </div>
                </div>

        </div> <!-- End .app-body (opened in thanh-dieu-huong.php) -->
    </div> <!-- End .app-container (opened in thanh-dieu-huong.php) -->

    <!-- Custom Context Menu -->
    <div id="custom-context-menu" class="context-menu" style="display: none;">
        <div class="menu-item" id="ctx-chat-ai">
            <i class="fas fa-magic" style="color: #6366f1;"></i> Chat AI
        </div>
        <div class="divider" style="height:1px; background:#f3f4f6; margin:4px 0;"></div>
        <div class="menu-item" onclick="document.execCommand('copy')">
            <i class="fas fa-copy" style="color: #6b7280;"></i> Sao chép
        </div>
    </div>

</main>
<script src="./assets/js/viet-bai-viet.js"></script>
<script src="./assets/js/thanh-dieu-huong.js"></script>
</body>

</html>