// ============================================
// 1. CẤU HÌNH API - FIXED
// ============================================
const API_BASE_URL = 'http://localhost:8080/api/v1';  // ✅ FIXED: Đổi từ 172.16.1.26 sang localhost

console.log("🔧 Script loaded");
console.log("🔧 API Base URL:", API_BASE_URL);

// ============================================
// 2. LOAD CONFIGS TỪ API
// ============================================
async function loadConfigs() {
    console.log("🚀 Đang tải cấu hình hệ thống...");
    
    const selectIds = ['content_types', 'writing_tones', 'languages', 'bots'];

    // Set loading state
    selectIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = '<option value="">Đang tải dữ liệu...</option>';
    });

    try {
        const url = `${API_BASE_URL}/ui/configs`;  // ✅ FIXED: Đúng đường dẫn
        console.log("🌐 Fetching from:", url);
        
        const res = await fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        console.log("📡 Response status:", res.status);

        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }

        const data = await res.json();
        console.log("✅ Configs loaded:", data);

        // Populate select elements
        const populate = (id, items, label) => {
            const el = document.getElementById(id);
            if (!el) {
                console.warn(`⚠️ Element ${id} not found`);
                return;
            }
            
            el.innerHTML = `<option value="">${label}</option>`;
            
            if (items && Array.isArray(items)) {
                items.forEach(item => {
                    const opt = document.createElement('option');
                    opt.value = item;
                    opt.textContent = item;
                    el.appendChild(opt);
                });
                console.log(`✅ Populated ${id} with ${items.length} items`);
            }
        };

        populate('content_types', data.content_types, 'Chọn loại bài viết');
        populate('writing_tones', data.writing_tones, 'Chọn tone giọng');
        populate('languages', data.languages, 'Chọn ngôn ngữ');
        populate('bots', data.bots, 'Chọn AI Model');

        showNotification('✅ Đã tải cấu hình thành công!', 'success');
        return true;

    } catch (e) {
        console.error("❌ Lỗi loadConfigs:", e);
        showNotification("⚠️ Không kết nối được API. Dùng cấu hình mặc định.", "warning");
        createDefaultConfigs();
        return false;
    }
}

function createDefaultConfigs() {
    console.log("📦 Loading default configs...");
    
    const defaults = {
        content_types: ["Blog SEO", "Tin tức", "Hướng dẫn"],
        writing_tones: ["Chuyên nghiệp", "Thuyết phục", "Sáng tạo"],
        languages: ["Tiếng Việt", "Tiếng Anh", "Tiếng Thái"],
        bots: ["GPT-4.1", "Gemini-2.5-flash"]
    };

    const fill = (id, arr, label) => {
        const el = document.getElementById(id);
        if (!el) return;
        
        el.innerHTML = `<option value="">${label}</option>`;
        arr.forEach(x => {
            const opt = document.createElement('option');
            opt.value = x;
            opt.textContent = x;
            el.appendChild(opt);
        });
    };
    
    fill('content_types', defaults.content_types, 'Chọn loại bài viết');
    fill('writing_tones', defaults.writing_tones, 'Chọn tone giọng');
    fill('languages', defaults.languages, 'Chọn ngôn ngữ');
    fill('bots', defaults.bots, 'Chọn AI Model');
    
    console.log("✅ Default configs loaded");
}

// ============================================
// 3. UTILITY FUNCTIONS
// ============================================
function showNotification(message, type = 'info') {
    console.log(`📢 Notification (${type}):`, message);
    
    const colors = {
        success: '#10B981',
        error: '#EF4444',
        warning: '#F59E0B',
        info: '#3B82F6'
    };

    // Remove existing
    document.querySelectorAll('.custom-notification').forEach(n => n.remove());

    const notification = document.createElement('div');
    notification.className = 'custom-notification';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${colors[type] || colors.info};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        font-size: 14px;
        font-weight: 500;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 4000);
}

// ============================================
// 4. KEYWORD TAGS
// ============================================
function initializeKeywordTags() {
    console.log("🏷️ Initializing keyword tags...");
    
    const input = document.getElementById('secondaryKeyword');
    const container = document.getElementById('tagContainer');
    
    if (!input || !container) {
        console.warn("⚠️ Keyword elements not found");
        return;
    }

    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && input.value.trim()) {
            e.preventDefault();
            
            const text = input.value.trim();
            const existing = Array.from(container.querySelectorAll('.tag'))
                .map(t => t.textContent.replace('×', '').trim());
            
            if (existing.includes(text)) {
                console.log("⚠️ Tag already exists");
                return;
            }

            const tag = document.createElement('span');
            tag.className = 'tag';
            tag.innerHTML = `${text} <span class="close-icon" onclick="this.parentElement.remove()">×</span>`;
            container.appendChild(tag);
            
            console.log("✅ Tag added:", text);
            input.value = '';
        }
    });
    
    console.log("✅ Keyword tags initialized");
}

// ============================================
// 5. SIDEBAR TOGGLE
// ============================================
function initializeSidebarToggle() {
    const toggleBtn = document.querySelector('.menu-toggle');
    const appContainer = document.querySelector('.app-container');
    
    if (toggleBtn && appContainer) {
        toggleBtn.addEventListener('click', () => {
            appContainer.classList.toggle('sidebar-collapsed');
        });
        console.log("✅ Sidebar toggle initialized");
    }
}

// ============================================
// 6. TAB SWITCHING
// ============================================
function initializeTabs() {
    const tabs = document.querySelectorAll(".tab");
    
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            
            const target = tab.dataset.tab;
            
            document.querySelectorAll(".content").forEach(c => {
                c.classList.remove("active");
                if (c.id === target) {
                    c.classList.add("active");
                }
            });
            
            console.log("✅ Tab switched to:", target);
        });
    });
}

// ============================================
// 7. GENERATE BUTTON - MAIN WORKFLOW
// ============================================
function initializeGenerateButton() {
    console.log("🎯 Initializing generate button...");
    
    const generateBtn = document.getElementById('generateBtn');
    
    if (!generateBtn) {
        console.warn("⚠️ Generate button not found");
        return;
    }

    generateBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        console.log("🚀 Generate button clicked");

        // ✅ FIXED: Lấy sourceType trong scope đúng
        const activeTab = document.querySelector('.tab.active');
        const sourceType = activeTab?.dataset.tab || 'private';
        
        console.log("📝 Source type:", sourceType);

        // Get form data
        let user_query, title;
        
        if (sourceType === 'internet') {
            user_query = document.getElementById('internet_user_query')?.value.trim();
            title = document.getElementById('articleTitle_internet')?.value.trim();
        } else {
            user_query = document.getElementById('user_query')?.value.trim();
            title = document.getElementById('articleTitle')?.value.trim();
        }

        const content_type = document.getElementById('content_types')?.value;
        const writing_tone = document.getElementById('writing_tones')?.value;
        const language = document.getElementById('languages')?.value;
        const bot = document.getElementById('bots')?.value;
        const article_length = document.getElementById('article_length')?.value;

        const tags = Array.from(document.querySelectorAll('.active #tagContainer .tag'))
            .map(t => t.textContent.replace('×', '').trim());

        console.log("📋 Form data:", {
            sourceType,
            user_query,
            title,
            content_type,
            writing_tone,
            language,
            bot,
            article_length,
            tags
        });

        // Validate
        if (!user_query) {
            showNotification('⚠️ Vui lòng nhập từ khóa chính!', 'warning');
            return;
        }

        if (!content_type) {
            showNotification('⚠️ Vui lòng chọn loại bài viết!', 'warning');
            return;
        }

        if (!bot) {
            showNotification('⚠️ Vui lòng chọn AI Model!', 'warning');
            return;
        }

        // Start workflow
        try {
            showNotification('🔍 Đang tìm kiếm tin tức...', 'info');
            
            // Step 1: Search news
            console.log("📰 Step 1: Searching news...");
            const newsResults = await searchNews(user_query);
            
            if (!newsResults || !newsResults.success) {
                throw new Error('Không tìm thấy tin tức phù hợp');
            }
            
            console.log("✅ Found", newsResults.total_results, "news");
            showNotification(`✅ Tìm thấy ${newsResults.total_results} bài viết`, 'success');

            // Step 2: Crawl articles
            console.log("📝 Step 2: Crawling articles...");
            showNotification('📝 Đang lấy nội dung bài viết...', 'info');
            
            const crawlResults = await crawlArticles(newsResults);
            
            if (!crawlResults || !crawlResults.success) {
                throw new Error('Không thể lấy nội dung bài viết');
            }
            
            console.log("✅ Crawled", crawlResults.processed_count, "articles");
            showNotification(`✅ Đã lấy ${crawlResults.processed_count} bài viết`, 'success');

            // Step 3: Filter and create outline
            console.log("🤖 Step 3: Creating outline...");
            showNotification('🤖 Đang tạo dàn ý bài viết...', 'info');
            
            const outlineResults = await filterNews(crawlResults, user_query);
            
            if (!outlineResults || !outlineResults.success) {
                throw new Error('Không thể tạo dàn ý');
            }
            
            console.log("✅ Outline created");
            showNotification('✅ Dàn ý đã được tạo thành công!', 'success');

            // Save pipeline data
            const pipelineData = {
                sourceType,
                user_query,
                title,
                content_type,
                writing_tone,
                language,
                bot,
                article_length,
                tags,
                newsResults,
                crawlResults,
                outlineResults
            };

            sessionStorage.setItem('pipelineData', JSON.stringify(pipelineData));
            console.log("💾 Pipeline data saved");

            // Redirect after 2 seconds
            setTimeout(() => {
                console.log("🔄 Redirecting to outline page...");
                window.location.href = 'dan-y-bai-viet.php';
            }, 2000);

        } catch (error) {
            console.error("❌ Workflow failed:", error);
            showNotification(`❌ Lỗi: ${error.message}`, 'error');
        }
    });
    
    console.log("✅ Generate button initialized");
}

// ============================================
// 8. API CALLS
// ============================================
async function searchNews(keyword) {
    console.log("🔍 Searching news for:", keyword);
    
    const url = `${API_BASE_URL}/crawl/news`;
    console.log("🌐 POST to:", url);
    
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: keyword,
            max_results: 10
        })
    });

    console.log("📡 Response:", response.status);
    
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    console.log("✅ News data:", data);
    
    return data;
}

async function crawlArticles(newsResults) {
    console.log("📝 Crawling articles...");
    
    const url = `${API_BASE_URL}/crawl/crawl`;
    console.log("🌐 POST to:", url);
    
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            articles: newsResults.results
        })
    });

    console.log("📡 Response:", response.status);
    
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    console.log("✅ Crawl data:", data);
    
    return data;
}

async function filterNews(crawlResults, keyword) {
    console.log("🤖 Filtering news...");
    
    const url = `${API_BASE_URL}/ai/news-filterings`;
    console.log("🌐 POST to:", url);
    
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            articles: crawlResults.articles,
            main_keyword: keyword,
            config: {
                max_articles: 5,
                min_relevance_score: 0.6
            }
        })
    });

    console.log("📡 Response:", response.status);
    
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    console.log("✅ Filter data:", data);
    
    return data;
}

// ============================================
// 9. INITIALIZE PAGE
// ============================================
async function initializePage() {
    console.log("🚀 Initializing page...");
    
    // Load configs from API
    await loadConfigs();
    
    // Initialize UI features
    initializeKeywordTags();
    initializeSidebarToggle();
    initializeTabs();
    initializeGenerateButton();
    
    console.log("✅ Page initialized successfully");
}

// ============================================
// 10. START APPLICATION
// ============================================
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializePage);
} else {
    initializePage();
}

console.log("✅ Script initialization complete");