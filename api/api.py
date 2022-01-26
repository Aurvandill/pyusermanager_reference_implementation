
from logging import exception
from pyusermanager import *

from fastapi import FastAPI, Cookie, Request
import uvicorn
from typing import Optional

from DataModels import *
from return_stuff import *

app = FastAPI()

#init base ad config
ad_config = AD_Config()

#init db config
db_config = DB_Config(provider = "mysql", host = "127.0.0.1",port = 3306, user = "test", pw = "test123", db_name = "users")

#init db config with db config and other parameters
config = LoginConfig(  
                    db_config=db_config,
                    debug = True,
                    auto_activate_accounts = False,
                    admin_group_name="administrator"
                    )

#generate our admin user if it does not exist yet
try:
    create_user(uname="admin",pw="12345",email="test@local",auth=AUTH_TYPE.LOCAL)
    #if user is new we need to verify the token if auto activate is disabled
    if not LoginConfig.auto_activate_accounts:
        print("since new admin user is not activated we try to activate him")
        auth_token = get_token("admin",ActivationCode)
        feedback = list(verify_token(token = auth_token, token_type=ActivationCode))
        print(f"success: {feedback[0]}")
except AlreadyExistsException:
    print("user already exists")
except Exception:
    print("somethign bad happened o-o")


#add default admin group and add admin to it
print(f"creating admin group: {LoginConfig.admin_group_name}")
create_perm(LoginConfig.admin_group_name)

print(f"adding admin user to {LoginConfig.admin_group_name} group")
assign_perm_to_user("admin",LoginConfig.admin_group_name)


###################################
#
# Fastapi stuff starts here!
#
###################################

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users")
async def api_get_users(request: Request):

    try:
        json = await request.json()
    except Exception:
        json = {}

    try:
        body = await request.body()
    except Exception:
        body = ""
    
    token = Token(**request.cookies)

    print(json)
    print(body)
    print(token.token)

    return_json = token

    if token.token is None:
        alert = Alert("no token specified",ALERT_TYPE.DANGER)
        redir = Redirect("/")

        return_json = get_json(alert,redir)
    
    else:

        return_json = get_users()

    return return_json


@app.get("/user/{username}")
async def get_user_info(username: str):
    return {"message": "not implemented yet"}



@app.post("/register")


@app.put("/user/{username}")
async def edit_user(username: str):
    return {"message": "not implemented yet"}




# start uvicorn with fastapi
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=1337, log_level="info")