<?php require "thanh-dieu-huong.php" ?>
<link rel="stylesheet" href="./assets/css/thanh-dieu-huong.css">
<link rel="stylesheet" href="./assets/css/cau-hinh-bai-viet.css">
<link rel="stylesheet" href="./assets/css/dan-y-bai-viet.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.0/Sortable.min.js"></script>

<main class="content-area">
    <div class="page-header">
        <h1 class="page-title">Cấu hình bài viết</h1>
        <div class="step-indicator">Bước 1/3</div>
    </div>

    <div class="tip-box">
        <span class="tip-icon">💡</span>
        <span class="tip-text">Mẹo: Từ khóa chính càng cụ thể, AI sẽ tạo nội dung càng phù hợp với mục tiêu SEO của bạn.</span>
    </div>

    <div class="grid-layout">
        <div class="column left disabled-overlay">

            <!-- Left Column -->
            <div class="column left">
                <section class="card basic-info">
                    <h2 class="card-title">Thông tin cơ bản</h2>
                    <div class="card-header">
                        <div class="tabs">
                            <button class="tab" data-tab="internet"><img src="./assets/images/icon-nguon-internet.png" alt="">Nguồn Internet</button>
                            <button class="tab active" data-tab="private"><img src="./assets/images/icon-du-lieu-rieng.png" alt=""> Dữ liệu riêng</button>
                        </div>
                    </div>

                    <div class="tab-content-container">
                        <!-- Internet Tab -->
                        <div class="content" id="internet">
                            <div class="form-group">
                                <label>Từ khóa chính <span class="required">*</span></label>
                                <div class="input-wrapper">
                                    <input type="text" id="internet_user_query" placeholder="VD: máy tính AI cho doanh nghiệp...">
                                </div>
                            </div>

                            <div class="form-group">
                                <label>Từ khoá phụ</label>
                                <input type="text" id="internet_user_query" planceholde="VD: Nhập từ khoá và nhấn Enter để thêm">
                                <div class="tag-container" id="tagContainer">
                                    <!-- Tags sẽ được thêm động -->
                                </div>

                            </div>

                            <div class="form-group">
                                <label>Tiêu đề bài viết</label>
                                <input type="text" id="articleTitle_internet" placeholder="Nhập tiêu đề">
                            </div>
                        </div>

                        <!-- Private Tab -->
                        <div class="content active" id="private">
                            <div class="form-group">
                                <label>Từ khóa chính <span class="required">*</span></label>
                                <div class="input-wrapper">
                                    <input type="text" id="user_query" placeholder="VD: máy tính AI cho doanh nghiệp..." required>
                                </div>
                            </div>

                            <div class="subtabs-wrapper">
                                <div class="subtabs">
                                    <button class="sub active" data-sub="file">Tải file</button>
                                    <button class="sub" data-sub="text">Nhập văn bản</button>
                                    <button class="sub" data-sub="link">Link sản phẩm</button>
                                </div>
                            </div>

                            <input type="file" id="file-selector" multiple hidden
                                accept="application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">

                            <div id="subtab-content-area" class="subtab-content"></div>
                            <div class="uploaded-file-list-outside"></div>

                            <div class="form-group">
                                <label>Từ khóa phụ</label>
                                <input type="text" id="secondaryKeyword" placeholder="Nhập từ khóa và nhấn Enter để thêm">
                                <div class="tag-container" id="tagContainer"></div>
                            </div>

                            <div class="form-group">
                                <label>Tiêu đề bài viết</label>
                                <div class="input-with-button">
                                    <input type="text" id="articleTitle" placeholder="Nhập tiêu đề">
                                    <button type="button" class="ai-suggest-btn" id="aiSuggestBtn" style="display:none;">🤖</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <section class="card content-config">
                    <h2 class="card-title">Cấu hình nội dung</h2>

                    <div class="form-group">
                        <label>Độ dài bài viết</label>
                        <select id="article_length" class="custom-select">
                            <option value="1200">Ngắn (800-1200 từ)</option>
                            <option value="2000">Trung bình (1200-2000 từ)</option>
                            <option value="3000">Dài (2000-3000 từ)</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Loại bài viết</label>
                        <select id="content_types" class="custom-select"></select>
                    </div>

                    <div class="form-group">
                        <label>Tone giọng</label>
                        <select id="writing_tones" class="custom-select"></select>
                    </div>

                    <div class="form-row">
                        <div class="form-group half">
                            <label>Model</label>
                            <select id="bots" class="custom-select"></select>
                        </div>
                        <div class="form-group half">
                            <label>Ngôn ngữ</label>
                            <select id="languages" class="custom-select"></select>
                        </div>
                    </div>
                </section>
            </div>
        </div>

        <!-- Right Column - Outline -->
        <div class="column right">
            <div class="outline-container">
                <div class="outline-top">
                    <span class="outline-label">Dàn ý bài viết</span>
                    <button class="guide-button">Hướng dẫn</button>
                </div>

                <div class="main-heading">
                    <h3>Xu hướng máy tính AI dành <br>cho doanh nghiệp</h3>
                    <span class="h-badge">H1</span>
                </div>

                <div id="outlineList"></div>
                <button class="add-item-btn" onclick="addOutlineItem()">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    Thêm tiêu đề
                </button>

                <div class="bottom-actions">
                    <button onclick="window.location.href='thinking.php'" class="action-btn back">← Quay lại</button>
                    <button class="action-btn primary">Tạo bài viết →</button>
                </div>
            </div>
        </div>
    </div>
</main>
</div>

<script src="./assets/js/thanh-dieu-huong.js"></script>
<script src="./assets/js/dan-y-bai-viet.js"></script>
<script src="./assets/js/cau-hinh-bai-viet.js"></script>