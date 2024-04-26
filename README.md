# after engine setup need to change to /3d-ensults
app.mount("/api/static", StaticFiles(directory="../video_results"), name="static")

app.mount("/api/avatar", StaticFiles(directory="../profile_image"), name="avatar")


# 1. check are you in .../fastapi or not => cd fastapi
# 2. python3 -m venv venv
# 2.1(ubuntu) source venv/bin/activate
# 3. pip install -r requirements.txt
# 4  uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload

#GITHUB push 
echo "# a" >> README.md 
git init 
git add README.md 
git commit -m "first commit" 
git branch -M main 
git remote add origin https://github.com/Yertayev01/a.git 
git push -u origin main

#GITHUB pull 
git remote -v 
git branch -a 
git fetch origin 
git checkout <branch_name> 
git merge origin/<branch_name>



# DATABASE MIGRATION
# 1. pip install alembic
# 2. alembic init alembic 
# 3. env.py -> from app.core.database import base
# 6. env.py -> from app.core.config import settings
# 7.put after config = context.config config.set_main_option("sqlalchemy.url", f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}')
# 8. alembic revision -m "create tablename table"
# 9. fill up functions in a version file in alembic and then run to update -> alembic upgrade "revision_name"
# 10. to cancel last update and rollback -> alembic downgrade "revision name"

#NGINX REVERSE PROXY SERVER
# 1. CREATE NGINX file to source folder
# 2. ADD NGINX installation folder to project folder
# 3. CREATE new FASTAPI.conf file 
# 4. INCLUDE YOUR FASTAPI.conf file in NGINX.conf file( listen port_number - should be same everywhere)
# 5. OPEN cmd(admin) - start nginx, nginx -t, nginx -s reload, nginx -t
# 6. OPEN browser - localhost:port_number/docs
# 7. GENERATE PRIVATE/PUBLIC KEYS AND SSLcertificate with OpenSSL:
# - go to bin folder after you download the OpenSSL
#   - openssl genrsa -out private_key_p2p.key 2048 (GENERATE PRIVATE KEY)
# - extract public key from private
#   - openssl rsa -in private_key_p2p.key -pubout -out public_key_p2p.key
#   set OPENSSL_CONF=C:\Users\USER\Downloads\openssl-0.9.8h-1-bin\share\openssl.cnf
#   openssl req -new -key private_key_p2p.key -out private_key_p2p.csr
#   openssl req -text -in private_key_p2p.csr -noout -verify
#   openssl x509 -in private_key_p2p.csr -out private_key_p2p.crt -req -signkey private_key_p2p.key -days 365
