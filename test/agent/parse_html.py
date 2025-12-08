from bs4 import BeautifulSoup

def strip_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text("\n")

if __name__ == '__main__':
    html_content = """
    <html>
        <head>
            <title>Trang web mẫu</title>
        </head>
        <body>
            <h1>Xin chào!</h1>
            <p>Đây là một <strong>đoạn văn</strong> ví dụ.</p>
            <ul>
                <li>Mục 1</li>
                <li>Mục 2</li>
                <li>Mục 3</li>
            </ul>
            <div>
                <p>Đoạn văn khác trong thẻ div.</p>
            </div>
        </body>
    </html>
    """
    
    result = strip_html(html_content)
    print(result)