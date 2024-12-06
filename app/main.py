# Import necessary modules from FastAPI and project-specific modules.
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from .core import database, models, routers, config, utils, oauth2
from .core.database import engine
from fastapi.staticfiles import StaticFiles
import os

models.Base.metadata.create_all(bind=engine)

# Create a new FastAPI instance and set its properties.
app = FastAPI()

# Include the router defined in the `routers` module in the app.
app.include_router(routers.router)

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
    try:
        # Retrieve the admin user from the database
        user = db.query(models.User).filter(models.User.name == config.settings.admin_username).first()
        
        if not user:
            # If the admin user doesn't exist, create a new user
            user = models.User(
                name=config.settings.admin_username,
                password=await utils.hash_password(config.settings.admin_password),
                is_admin=True,
            )
        else:
            # If the admin user exists, update their username and password
            user.name = config.settings.admin_username
            user.password = await utils.hash_password(config.settings.admin_password)
        
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        # Close the database session in case of any error
        db.close()
        raise e
    finally:
        db.close()


# Define an endpoint for retrieving the OpenAPI specification document.
@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(oauth2.require_user)):
    return get_openapi()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010, debug=True)
