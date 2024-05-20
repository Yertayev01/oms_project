# Import necessary modules from FastAPI and project-specific modules.
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from .core import database, models, routers, config, utils, oauth2
from .core.database import engine
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)


# Create a new FastAPI instance and set its properties.
app = FastAPI()

# Include the router defined in the `routers` module in the app.
app.include_router(routers.router)

# after engine setup need to change to /3d-ensults
app.mount("/api/static", StaticFiles(directory="../results"), name="static")

app.mount("/api/avatar", StaticFiles(directory="../profile_image"), name="avatar")

app.mount("/api/json", StaticFiles(directory="../nodes"), name="json")
# Set the allowed origins for CORS requests.
origins = [
    "*"
]

# Add a CORS middleware to the app.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    db = database.SessionLocal()
    user = db.query(models.User).filter(models.User.username == config.settings.admin_username).first()
    try:
        if not user:
            user = models.User(username = config.settings.admin_username, password = await utils.hash_password(config.settings.admin_password), is_admin = True)
        else:
            user.username = config.settings.admin_username
            user.password = await utils.hash_password(config.settings.admin_password)
            user.is_admin = True
        db.add(user)
        db.commit()
        db.refresh(user)
    except:
        db.close()

# # Define an endpoint for retrieving the Swagger UI documentation.
# @app.get("/docs", include_in_schema=False)
# async def get_swagger_documentation(username: str):
#     return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

# # Define an endpoint for retrieving the ReDoc documentation.
# @app.get("/redoc", include_in_schema=False)
# async def get_redoc_documentation(username: str):
#     return get_redoc_html(openapi_url="/openapi.json", title="docs")

# Define an endpoint for retrieving the OpenAPI specification document.
@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(oauth2.require_user)):
    return get_openapi()


if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8010, debug=True)
