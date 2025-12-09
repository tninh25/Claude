<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="header.css">
</head>

<body>
    <div class="app-container">
        <!-- Top Header (Reused) -->
        <header class="top-header">
            <div class="header-left">
                <button class="menu-toggle">
                    <img src="./assets/images/menu.png" alt="">
                </button>
                <div class="logo">
                    <img src="./assets/images/AIS.png" alt="">
                </div>
            </div>

            <div class="header-center">
                <nav class="top-nav">
                    <a href="#" class="active">AI SEO</a>
                    <a href="#">AI Social Media</a>
                    <a href="#">Bảng giá</a>
                    <a href="#">Hướng dẫn</a>
                    <a href="#">Liên hệ</a>
                </nav>
            </div>

            <!-- <div class="header-right">
                <a href="#" class="header-action"><span class="icon"><img src="./assets/images/icon-tu-mau.png" alt=""></span> Chọn từ mẫu</a>
                <a href="#" class="header-action"><span class="icon"><img src="./assets/images/icon-luu-nhap.png" alt=""></span> Lưu nháp</a>
                <div class="user-avatar">
                    <img src="./assets/images/icon-people.png" alt="Avatar">
                </div>
            </div> -->
            <?php if (empty($hideHeaderActions)) { ?>
                <a href="#" class="header-action">
                    <span class="icon"><img src="./assets/images/icon-tu-mau.png" alt=""></span>
                    Chọn từ mẫu
                </a>

                <a href="#" class="header-action">
                    <span class="icon"><img src="./assets/images/icon-luu-nhap.png" alt=""></span>
                    Lưu nháp
                </a>
            <?php } ?>

            <div class="user-avatar">
                <img src="./assets/images/icon-people.png" alt="Avatar">
            </div>



        </header>

        <!-- Body Container -->
        <div class="app-body">
            <!-- Sidebar (Reused) -->
            <aside class="sidebar">
                <nav class="sidebar-nav">
                    <div class="nav-group">
                        <a href="#" class="nav-item active">
                            <span class="icon">
                                <img src="./assets/images/icon-google.png" alt="">
                            </span> AI SEO
                        </a>
                        <a href="#" class="nav-item">
                            <span class="icon">
                                <img src="./assets/images/icon-viet-seo.png" alt="">
                            </span> Viết bài SEO
                        </a>
                        <a href="#" class="nav-item">
                            <span class="icon">
                                <img src="./assets/images/icon-chuoi-seo.png" alt="">
                            </span> Viết chuỗi bài SEO
                        </a>
                        <a href="#" class="nav-item">
                            <span class="icon">
                                <img src="./assets/images/icon-danh-sach.png" alt="">
                            </span> Danh sách bài viết
                        </a>
                        <a href="#" class="nav-item">
                            <span class="icon">
                                <img src="./assets/images/icon-search.png" alt="">
                            </span> Phân tích từ khóa
                        </a>
                        <a href="#" class="nav-item">
                            <span class="icon">
                                <img src="./assets/images/icon-mau-cau-hinh.png" alt="">
                            </span> Mẫu cấu hình
                        </a>
                    </div>

                    <div class="nav-group">
                        <div class="nav-label">AI Facebook</div>
                        <a href="#" class="nav-item">
                            <span class="icon">
                                <img src="./assets/images/icon-viet-seo.png" alt="">
                            </span> Viết bài Facebook
                        </a>
                        <a href="#" class="nav-item">
                            <span class="icon">
                                <img src="./assets/images/icon-danh-sach.png" alt="">
                            </span>
                            Danh sách bài viết
                        </a>
                        <a href="#" class="nav-item">
                            <span class="icon">
                                <img src="./assets/images/icon-mau-cau-hinh.png" alt="">
                            </span> Mẫu cấu hình
                        </a>
                    </div>

                    <div class="nav-group mt-auto">
                        <a href="#" class="nav-item"><span class="icon">
                                <img src="./assets/images/icon-tich-hop.png" alt="">
                            </span> Tích hợp</a>
                        <a href="#" class="nav-item"><span class="icon">
                                <img src="./assets/images/icon-tai-lieu.png" alt="">
                            </span> Tài liệu</a>
                        <a href="#" class="nav-item"><span class="icon">
                                <img src="./assets/images/icon-cai-dat.png" alt="">
                            </span> Thiết đặt</a>

                    </div>
                </nav>
            </aside>