# Import necessary modules from FastAPI and project-specific modules.
# Import necessary modules from FastAPI and project-specific modules.
from fastapi import APIRouter

from .api import  auth, swagger, order, product, promotion

# Create an API router with the prefix "/api"
router = APIRouter(prefix="/api")


router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["Auth"],
)

router.include_router(
    order.router,
    prefix="/order",
    tags=["Order"]
)

router.include_router(
    product.router,
    prefix="/product",
    tags=["Product"]
)

router.include_router(
    promotion.router,
    prefix="/promotion",
    tags=["Promotion"]
)

router.include_router(
    swagger.router,
    prefix="/swagger",
    tags=["Swagger"]
)
