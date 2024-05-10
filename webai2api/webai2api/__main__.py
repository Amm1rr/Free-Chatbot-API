from .main import app, config_ui_path
from .routes.claude_routes import router as claude_router
from .routes.gemini_routes import router as gemini_router
from .routes.v1_routes import router as v1_router
from .routes.http_routes import web_ui_middleware
from .utils import utility

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
import os

utility.configure_logging()
logging.info("main.py")

app = FastAPI()

COOKIE_GEMINI = utility.getCookie_Gemini()
COOKIE_CLAUDE = utility.getCookie_Claude(configfilepath=os.getcwd(), configfilename="Config.conf")

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(claude_router)
app.include_router(gemini_router)
app.include_router(v1_router)

# Serve UI files
app.mount('/', StaticFiles(directory="webai2api/UI/build"), 'static')


# Middleware for Web UI
@app.middleware("http")
async def webmiddleware(request: Request, call_next):
    logging.info("main.py.web_middleware")
    response = await call_next(request)
    res = await web_ui_middleware(request=request, response=response, url=request.url.path.lower())
    return res


def run():
    logging.info("run.__main__.py")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run()
    logging.info("__main__.py./__name__()")
