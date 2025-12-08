# services/crawl/images_search_service.py

import os
from clients.news_client import GoogleSearchClient
from models.crawl.images_schemas import ImageItem, ImageSearchRequest, ImageSearchResponse

class ImagesSearchService:
    """Lấy hình ảnh từ Google"""
    def __init__(self):
        self.images_search_client = GoogleSearchClient()

    async def search_images(self, request: ImageSearchRequest) -> ImageSearchResponse:
        """Tìm kiếm hình ảnh và trả về structured data"""
        try:
            
            # Gọi client để lấy hình ảnh (sync method)
            raw_images = self.images_search_client.search_images(request.query, request.num_results)
            
            if not raw_images:
                return ImageSearchResponse(
                    success=True,
                    query=request.query,
                    total_results=0,
                    images=[],
                    message="Không tìm thấy hình ảnh nào"
                )

            images = []
            for img in raw_images:
                try:
                    image_item = ImageItem(
                        url=img.get('url', ''),
                        thumbnail=img.get('thumbnail', ''),
                        title=img.get('title', ''),
                        source=img.get('source', ''),
                        size=img.get('size', ''),
                    )
                    images.append(image_item)
                except Exception as e:
                    continue
            
            return ImageSearchResponse(
                success=True,
                query=request.query,
                total_results=len(images),
                images=images,
                message=f"Tìm thấy {len(images)} hình ảnh"
            )

        except Exception as e:
            return ImageSearchResponse(
                success=False,
                query=request.query,
                total_results=0,
                images=[],
                message=f"Lỗi tìm kiếm hình ảnh: {str(e)}"
            )
    
    #.... test ....
    def generate_html(self, query: str, num_results: int = 10) -> str:
        """Tạo HTML để hiển thị ảnh"""
        images = self.images_search_client.search_images(query, num_results)
        
        if not images:
            return """
            <html>
                <body>
                    <h2>Không tìm thấy ảnh nào cho từ khóa '{}'</h2>
                </body>
            </html>
            """.format(query)

        # Tạo HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Kết quả tìm kiếm: {query}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .image-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                    gap: 20px;
                }}
                .image-card {{
                    background: white;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    transition: transform 0.3s;
                }}
                .image-card:hover {{
                    transform: translateY(-5px);
                }}
                .image-card img {{
                    width: 100%;
                    height: 200px;
                    object-fit: cover;
                }}
                .image-info {{
                    padding: 15px;
                }}
                .image-title {{
                    font-weight: bold;
                    margin-bottom: 5px;
                    color: #333;
                }}
                .image-source {{
                    color: #666;
                    font-size: 12px;
                    margin-bottom: 5px;
                }}
                .image-size {{
                    color: #888;
                    font-size: 11px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Kết quả tìm kiếm: "{query}"</h1>
                <p>Tìm thấy {len(images)} ảnh</p>
            </div>
            
            <div class="image-grid">
        """

        # Thêm từng ảnh vào grid
        for img in images:
            html_content += f"""
                <div class="image-card">
                    <img src="{img['url']}" alt="{img['title']}" 
                         onerror="this.src='{img['thumbnail']}'">
                    <div class="image-info">
                        <div class="image-title">{img['title'][:50]}{'...' if len(img['title']) > 50 else ''}</div>
                        <div class="image-source">Nguồn: {img['source']}</div>
                        <div class="image-size">Kích thước: {img['size']}</div>
                    </div>
                </div>
            """

        html_content += """
            </div>
        </body>
        </html>
        """

        return html_content

    def save_html(self, query: str, num_results: int = 10, filename: str = None):
        """Lưu HTML vào file và mở trong browser"""
        if filename is None:
            filename = f"image_search_{query.replace(' ', '_')}.html"
        
        html_content = self.generate_html(query, num_results)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Mở file trong browser
        os.system(f'start {filename}')  # Windows
        # os.system(f'open {filename}')  # Mac
        # os.system(f'xdg-open {filename}')  # Linux
        
        print(f"Đã lưu kết quả vào: {filename}")

    def display_simple_gallery(self, query: str, num_results: int = 10):
        """Hiển thị gallery đơn giản trong terminal với URLs có thể click"""
        images = self.images_search_client.search_images(query, num_results)
        
        if not images:
            print("Không tìm thấy ảnh nào!")
            return

        print(f"\n Tìm thấy {len(images)} ảnh cho '{query}':")
        print("=" * 60)
        
        for i, img in enumerate(images, 1):
            print(f"\n{i}. {img['title']}")
            print(f"    URL: {img['url']}")
            print(f"    Thumbnail: {img['thumbnail']}")
            print(f"    Nguồn: {img['source']}")
            print(f"    Kích thước: {img['size']}")

if __name__ == '__main__':
    image_search_service = ImagesSearchService()

    # 1. Tạo và lưu HTML (tự động mở trong browser)
    image_search_service.display_simple_gallery("chatgpt 5.0", 8)