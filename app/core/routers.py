# Import necessary modules from FastAPI and project-specific modules.
# Import necessary modules from FastAPI and project-specific modules.
from fastapi import APIRouter

from .api import  asset, upload, anchor, generation, comment, like, save, node, auth, swagger, follow, payment, user, video 

# Create an API router with the prefix "/api"
router = APIRouter(prefix="/api")


router.include_router(
    user.router, 
    prefix="/user", 
    tags=["User"],
)

router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["Auth"],
)

router.include_router(
    upload.router,
    prefix="/upload",
    tags=["Upload"]
)

router.include_router(
    asset.router,
    prefix="/object",
    tags=["Object"]
)

router.include_router(
    anchor.router,
    prefix="/anchor",
    tags=["Anchor"]
)

router.include_router(
    node.router,
    prefix="/node",
    tags=["Node"]
)

router.include_router(
    video.router,
    prefix="/video",
    tags=["Video"]
)

router.include_router(
    generation.router,
    prefix="/generation",
    tags=["Generation"]
)

router.include_router(
    comment.router,
    prefix="/comment",
    tags=["Comment"]
)

router.include_router(
    like.router,
    prefix="/like",
    tags=["Like"]
)

router.include_router(
    save.router,
    prefix="/save",
    tags=["Save"]
)

router.include_router(
    swagger.router,
    prefix="/swagger",
    tags=["Swagger"]
)

router.include_router(
    follow.router,
    prefix="/follow",
    tags=["Follow"]
)

router.include_router(
    payment.router,
    prefix="/payment",
    tags=["Payment"]
)

