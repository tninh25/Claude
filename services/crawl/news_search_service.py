# services/crawl/news_search_service.py

from clients.news_client import GoogleSearchClient
from models.crawl.news_schemas import SearchRequest, SearchResponse, SearchResult

class NewsService:
    """Lấy tin tức từ Google Search Custome theo từ khóa"""
    def __init__(self):
        self.news_client = GoogleSearchClient()
    
    async def news_searching(self, request: SearchRequest) -> SearchResponse:
        search_results = self.news_client.search(
            query=request.query, 
            num_results=request.max_results
        )
        
        formatted_results = []
        for result in search_results.get("results", []):
            formatted_results.append(SearchResult(
                url=result.get("link", ""), 
                title=result.get("title", ""),
                snippet=result.get("snippet", "")
            ))
        
        return SearchResponse(
            success=search_results.get("success", True),
            query=search_results.get("query", request.query),  
            total_results=search_results.get("total_results", 0),
            results=formatted_results,
            message=search_results.get("message", "")
        )