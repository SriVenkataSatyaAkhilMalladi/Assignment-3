from fastapi import Depends, FastAPI,Response,Request
from fastapi.responses import JSONResponse
from api import jwt,metadata_geos,metadata_nexrad,file_url_generator,nexrad_coords,file_url_generator,file_transfer,file_transfer_nexrad,goes_db,nexrad_db,registration,ratelimiting
from datetime import datetime
import logging
from jose import jwt as jwt_pck
import os
from dotenv import load_dotenv
load_dotenv()

secret_key = os.environ.get("SECRET_KEY")
app = FastAPI()

app.include_router(jwt.router_jwt)
app.include_router(metadata_geos.router_metadata_geos)
app.include_router(metadata_nexrad.router_metadata_nexrad)
app.include_router(file_url_generator.router_file_url_generator)
app.include_router(file_transfer.router_file_transfer)
app.include_router(file_transfer_nexrad.router_file_transfer_nexrad)
app.include_router(nexrad_coords.router_nexrad_coords)
app.include_router(registration.router_register_user)
app.include_router(registration.router_update_password)
app.include_router(goes_db.router_goes_db)
app.include_router(nexrad_db.router_nexrad_db)


@app.get("/test")
async def root():
    return {"message": "Hello Bigger Applications!"}


logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('logs/app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
@app.middleware("http")
async def log_requests(request: Request, call_next):

    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header[len('Bearer '):]
    else:
        token = None

    # Extract the username from the JWT token
    username = 'default'
    if token:
        try:
            payload = jwt_pck.decode(token, secret_key, algorithms=['HS256'])
            username = payload.get('sub')
        except:
            pass
    
    response = await call_next(request)
    log_dict = {
        "username": username,
        'endpoint': request.url.path,
        'statuscode': response.status_code,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M:%S')
    }
    logger.info(log_dict)

    



    return response


