import sys
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.log import setup_logging, handle_exception

from dotenv import load_dotenv

load_dotenv()
VERSION = "0.1.1"
sys.dont_write_bytecode = True

class ShipBuild:
    def __init__(self):
        self.logger = setup_logging()
        sys.excepthook = handle_exception

        self.app = FastAPI(
            title="조선해양 공모전 AI 서버",
            version=VERSION,
            description="조선해양 공모전 AI 서버입니다.\n제작: 경상국립대학교 컴퓨터공학부 20학번 정승원",
        )

        self._configure_cors()
        self._register_routes()


    def _configure_cors(self):
        origins = ["*"]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _register_routes(self):

        @self.app.get("/version", tags=["root"])
        async def get_version():
            return {"version": VERSION}

        self.app.include_router(router.router)
    
    def get_app(self) -> FastAPI:
        return self.app

server_instance = ShipBuild()
app = server_instance.get_app()