from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.config_loader import config
from api.v1.crawl import router as crawl_router
from api.v1.prompt import router as prompt_router
from api.v1.ai import router as ai_router
from api.v1.ui import router as ui_router
from api.v1.seo import router as seo_router

# Load config
app_config = config.get('app')
server_config = config.get('server')

app = FastAPI(
    title=app_config['name'],
    version=app_config['version'],
    debug=app_config['debug']
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crawl_router, prefix="/api/v1/crawl", tags=["News Searching and Crawl Content"])
app.include_router(prompt_router, prefix="/api/v1/prompt", tags=["Config Prompt for LuminAI"])
app.include_router(ai_router, prefix="/api/v1/ai", tags=["AI Services"])
app.include_router(ui_router, prefix="/api/v1/ui", tags=["UI Config"])
app.include_router(seo_router, prefix="/api/v1/seo", tags=["SEO Checker"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=server_config['host'],
        port=server_config['port'],
        reload=app_config['debug']
    )
