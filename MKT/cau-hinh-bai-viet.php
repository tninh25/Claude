<?php require "thanh-dieu-huong.php" ?>
<link rel="stylesheet" href="./assets/css/thanh-dieu-huong.css">
<link rel="stylesheet" href="./assets/css/cau-hinh-bai-viet.css">

<div class="app-container">
    <!-- Body Container (Sidebar + Content) -->
    <div class="app-body">
        <!-- Sidebar -->

        <!-- Main Content Area -->
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
                                    <label>Từ khóa chính *<span class="required">*</span></label>
                                    <div class="input-wrapper">
                                        <input type="text" id="internet_user_query" placeholder="VD: máy tính AI cho doanh nghiệp...">
                                    </div>
                                </div>

                                <div class="form-group">
                                    <label>Từ khóa phụ</label>
                                    <input type="text" id="customData_secondaryKeyword" placeholder="Nhập từ khóa và nhấn Enter để thêm">
                                    <div class="tag-container" id="customData_tagContainer">
                                        <!-- Tags sẽ được thêm động -->
                                    </div>
                                </div>


                                <div class="form-group">
                                    <label>Tiêu đề bài viết (Tuy chọn)</label>
                                    <input type="text" id="articleTitle_internet" placeholder="Nhập tiêu đề">
                                </div>
                            </div>

                            <!-- Private Tab -->
                            <div class="content active" id="private">
                                <!-- Context Textarea -->
                                <div class="form-group">
                                    <div class="textarea-wrapper">
                                        <textarea id="private_context" placeholder="Nhập nội dung của bạn..."></textarea>
                                        <div class="char-counter">0/300 từ</div>
                                    </div>
                                </div>

                                <!-- Website Input -->
                                <div class="form-group">
                                    <label>Website của bạn</label>
                                    <div class="input-with-button">
                                        <input type="text" id="user_website" placeholder="HTTPS:">
                                        <button type="button" class="btn-add" id="addWebsiteBtn">Thêm</button>
                                    </div>
                                </div>

                                <!-- Main Keyword -->
                                <div class="form-group">
                                    <label>Từ khóa chính <span class="required">*</span></label>
                                    <input type="text" id="user_query" placeholder="VD: máy tính AI cho doanh nghiệp">
                                </div>

                                <!-- Secondary Keywords -->
                                <div class="form-group">
                                    <label>Từ khóa phụ</label>
                                    <input type="text" id="secondaryKeyword" placeholder="Nhập từ khóa và nhấn Enter để thêm">
                                    <div class="tag-container" id="tagContainer">
                                        <!-- Tags sẽ được thêm động -->
                                    </div>
                                </div>

                                <!-- Article Title -->
                                <div class="form-group">
                                    <label>Tiêu đề bài viết</label>
                                    <input type="text" id="articleTitle" placeholder="Nhập tiêu đề">
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

                        <button class="generate-btn" id="generateBtn">
                            Tạo dàn ý bài viết <span style="margin-left: 5px;">-></span>
                        </button>

                    </section>
                </div>

                <!-- Right Column -->
                <div class="column right">
                    <div class="video-placeholder">
                        <button class="guide-btn">Hướng dẫn</button>
                        <iframe class="video-thumb" src="https://www.youtube.com/embed/Uzqpwc5hpCE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
                    </div>

                    <div class="preview-text">
                        <h3>Dàn ý của bạn sẽ hiển thị tại đây</h3>
                        <p>Công cụ AI được thiết kế để tạo nhiều dạng nội dung khác nhau với chất lượng ổn định và đáng tin cậy.</p><br>
                        <p>Xem ví dụ bên dưới để hiểu cách quy trình hoạt động và tạo ra nội dung hấp dẫn. Tất cả bài viết trên nền tảng đều được tạo từ công cụ này.</p>

                    </div>

                    <!-- Hidden preview structure to keep JS happy if it tries to update it, or we update JS -->
                    <div id="previewLength" style="display:none;"></div>

                    <div class="loading" id="loading" style="display: none; text-align: center; margin: 20px 0;">
                        <div class="spinner"></div>
                        <p>Đang tạo bài viết...</p>
                    </div>
                </div>
            </div>
        </main>
    </div>
</div>

<div class="tooltip" id="tooltip"></div>
<script src="./assets/js/cau-hinh-bai-viet.js"></script>
<!-- <script src="khoi-tao-bai-viet.js"></script> -->
<!-- <script src="dan-y-bai-viet.js"></script> -->


</body>

</html>