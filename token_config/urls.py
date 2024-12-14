from fastapi import APIRouter

router = APIRouter()

from token_config.views.main import router as MainRouter


router.include_router(MainRouter, prefix="", tags=["Token"])
