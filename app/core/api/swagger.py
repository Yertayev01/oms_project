from fastapi import Depends, APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html

from app.core.config import swagger_login_page
from fastapi.responses import HTMLResponse
from fastapi import Depends, APIRouter

from app.core.config import settings

from app.core import oauth2

router = APIRouter()

ACCESS_TOKEN_EXPIRES_IN = settings.access_token_expires_in
REFRESH_TOKEN_EXPIRES_IN = settings.refresh_token_expires_in


@router.get("/swagger", response_class=HTMLResponse, include_in_schema=False)
async def swagger_login():
    return swagger_login_page

# Define an endpoint for retrieving the Swagger UI documentation.


@router.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(oauth2.require_admin)):
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")

# Define an endpoint for retrieving the ReDoc documentation.


@router.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(oauth2.require_admin)):
    return get_redoc_html(openapi_url="/api/openapi.json", title="docs")