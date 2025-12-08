import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from typing import List
import json
import csv
import os


class SitemapService:
    """
    Service lấy toàn bộ URL từ website thông qua sitemap
    - Tự phát hiện sitemap từ robots.txt
    - Hỗ trợ sitemap index (đệ quy)
    - Xuất JSON / CSV
    """

    def __init__(self, site_url: str, timeout: int = 15):
        self.site_url = site_url.rstrip("/")
        self.timeout = timeout
        self.sitemap_url: str | None = None
        self.urls: List[str] = []

    # =========================
    # 1. PHÁT HIỆN SITEMAP
    # =========================
    def detect_sitemap(self) -> str | None:
        robots_url = urljoin(self.site_url, "/robots.txt")

        try:
            r = requests.get(robots_url, timeout=self.timeout)
            if r.status_code != 200:
                return None

            for line in r.text.splitlines():
                if line.lower().startswith("sitemap:"):
                    self.sitemap_url = line.split(":", 1)[1].strip()
                    return self.sitemap_url

        except Exception as e:
            print("❌ Lỗi khi đọc robots.txt:", e)

        return None

    # =========================
    # 2. PARSE SITEMAP ĐỆ QUY
    # =========================
    def _parse_sitemap_recursive(self, sitemap_url: str) -> List[str]:
        r = requests.get(sitemap_url, timeout=self.timeout)
        r.raise_for_status()

        root = ET.fromstring(r.text)
        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls: List[str] = []

        # ✅ Sitemap index (cha)
        if root.tag.endswith("sitemapindex"):
            for loc in root.findall(".//ns:loc", ns):
                child_sitemap = loc.text.strip()
                print("📂 Đọc sitemap con:", child_sitemap)
                urls.extend(self._parse_sitemap_recursive(child_sitemap))

        # ✅ Sitemap chứa URL thật
        elif root.tag.endswith("urlset"):
            for loc in root.findall(".//ns:loc", ns):
                urls.append(loc.text.strip())

        return urls

    # =========================
    # 3. LOAD TOÀN BỘ URL
    # =========================
    def load_all_urls(self) -> List[str]:
        if not self.sitemap_url:
            self.detect_sitemap()

        if not self.sitemap_url:
            raise ValueError("❌ Không tìm thấy sitemap trong robots.txt")

        print("✅ Tìm thấy sitemap:", self.sitemap_url)

        self.urls = self._parse_sitemap_recursive(self.sitemap_url)
        self.urls = self._filter_valid_urls(self.urls)

        return self.urls

    # =========================
    # 4. LỌC URL SẠCH
    # =========================
    def _filter_valid_urls(self, urls: List[str]) -> List[str]:
        blacklist_ext = (".jpg", ".png", ".js", ".css", ".pdf", ".zip", ".xml")
        return [u for u in urls if not u.lower().endswith(blacklist_ext)]

    # =========================
    # 5. EXPORT JSON
    # =========================
    def export_json(self, file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.urls, f, ensure_ascii=False, indent=2)

        print(f"✅ Đã lưu JSON: {file_path}")

    # =========================
    # 6. EXPORT CSV
    # =========================
    def export_csv(self, file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["url"])
            for u in self.urls:
                writer.writerow([u])

        print(f"✅ Đã lưu CSV: {file_path}")

service = SitemapService("https://www.tnc.com.vn")

urls = service.load_all_urls()

print("Tổng URL:", len(urls))
for u in urls[:10]:
    print(u)

service.export_json("output/tnc_urls.json")
service.export_csv("output/tnc_urls.csv")