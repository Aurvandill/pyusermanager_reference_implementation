from pyusermanager import *

import bottle
from http import HTTPStatus

from bottle import (
    route,
    run,
    post,
    get,
    static_file,
    request,
    redirect,
    HTTPResponse,
    response,
)

# from gevent import monkey
# monkey.patch_all()


from return_stuff import *
import filestuff


def get_default_response():
    default_response = HTTPResponse(
        status=HTTPStatus.IM_A_TEAPOT,
        body=json.dumps({"error": "this should never happen lol"}),
    )
    default_response.headers["Access-Control-Allow-Origin"] = "*"
    default_response.headers[
        "Access-Control-Allow-Methods"
    ] = "PUT, GET, POST, DELETE, OPTIONS"
    default_response.headers[
        "Access-Control-Allow-Headers"
    ] = "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"
    default_response.body = get_json_from_args(
        Alert("oh god something went terribly wrong", ALERT_TYPE.DANGER)
    )

    return default_response


###################################
#
# Fastapi stuff starts here!
#
###################################

app = bottle.app()


@app.get("/user/<username>")
def api_verify_token(username):
    ip = request.environ.get("HTTP_X_FORWARDED_FOR") or request.environ.get(
        "REMOTE_ADDR"
    )
    return_response = get_default_response()
    return_response.status = HTTPStatus.UNAUTHORIZED

    request_params = dict(request.query.decode())
    print(request_params)

    try:
        token = request_params["token"]
    except Exception:
        token = None
        return_response.status = HTTPStatus.BAD_REQUEST
        return_response.body = get_json_from_args(
            Alert("No Token supplied!", ALERT_TYPE.DANGER), Redirect("/")
        )
        return return_response

    try:
        success, perms, username = verify_token(token, ip)
    except TypeError:
        return_response.status = HTTPStatus.BAD_REQUEST
        return_response.body = get_json_from_args(
            Alert("Token Type is not valid!", ALERT_TYPE.DANGER), Redirect("/")
        )
        return return_response


@app.post("/login")
def login():
    return_response = get_default_response()

    print("reeee")
    json_text = request.body.read().decode("utf-8")
    print(json_text)

    try:
        json_obj = json.load(request.body)
    except Exception as err:
        return_response.status = HTTPStatus.BAD_REQUEST
        print(err)
        print("could not read json input!")
        return return_response
    print("successfully converted to json")
    print(json_obj)

    # perform login!

    try:
        password = json_obj["password"]
        username = json_obj["username"]
    except Exception:
        return_response.status = HTTPStatus.BAD_REQUEST
        return_response.body = get_json_from_args(
            Alert("required vars missing", ALERT_TYPE.WARNING)
        )
        return return_response

    try:
        remember_me = json_obj["remember_me"]
        if remember_me:
            valid_days = 365
        else:
            valid_days = 1
    except Exception:
        valid_days = 1

    try:
        success, user = login_user(username, password)
    except MissingUserException:
        return_response.status = HTTPStatus.BAD_REQUEST
        return_response.body = get_json_from_args(
            Alert("User does not exist!", ALERT_TYPE.WARNING)
        )
        return return_response

    if success:
        ip = request.environ.get("HTTP_X_FORWARDED_FOR") or request.environ.get(
            "REMOTE_ADDR"
        )
        # create token
        try:
            token = create_token(user, ip, valid_days)
            return_response.status = HTTPStatus.OK
            return_response.body = get_json_from_args(
                {"Login": {"valid_day": valid_days, "token": token}},
                Alert("Successfull Login", ALERT_TYPE.INFO),
                Redirect(f"/user/{user}"),
            )
        except Exception:
            return_response.status = HTTPStatus.INTERNAL_SERVER_ERROR
            return_response.body = get_json_from_args(
                Alert("could not generate token!", ALERT_TYPE.DANGER)
            )
    else:
        return_response.status = HTTPStatus.UNAUTHORIZED
        return_response.body = get_json_from_args(
            Alert("password/User Combination is wrong!", ALERT_TYPE.WARNING)
        )

    return return_response


@app.get("/header")
def api_get_header():
    return_response = get_default_response()

    request_params = dict(request.query.decode())
    print(request_params)

    header = filestuff.get_template("header_logged_out.html")

    return_response.status = HTTPStatus.OK
    return_response.body = get_json_from_args({"pre_rendered": {"content": header}})

    try:
        token = request_params["token"]
    except Exception:
        token = None

    print(f"token: {token}")
    if token is not None:
        ip = request.environ.get("HTTP_X_FORWARDED_FOR") or request.environ.get(
            "REMOTE_ADDR"
        )
        # verify token
        success, perms, username = verify_token(token, ip)
        print(verify_token(token, ip))

        if success:

            user_dict, token_dict, perm_dict = get_extended_info(username)
            template_vars = {
                "username": username,
                "api_url": "http://127.0.0.1:1337",
                "user_avatar": user_dict["avatar"],
            }

            if LoginConfig.admin_group_name in perms:
                header = filestuff.get_template(
                    "header_logged_in_admin.html", **template_vars
                )
            else:
                header = filestuff.get_template(
                    "header_logged_in.html", **template_vars
                )

            return_response.body = get_json_from_args(
                {"pre_rendered": {"content": header}}
            )

    return return_response


@app.get("/users")
def api_get_users():

    ip = request.environ.get("HTTP_X_FORWARDED_FOR") or request.environ.get(
        "REMOTE_ADDR"
    )

    return_response = get_default_response()
    return_response.status = HTTPStatus.UNAUTHORIZED

    request_params = dict(request.query.decode())

    print(request_params)

    try:
        token = request_params["token"]
    except Exception:
        token = None

    print(token)

    if token is None or len(token) < 2:
        return_response.status = HTTPStatus.UNAUTHORIZED
        return_json = get_json_from_args(
            Alert("please log in", ALERT_TYPE.WARNING), Redirect("/login")
        )
        # return_json = get_json_from_args(Alert("Bitte einloggen!",ALERT_TYPE.WARNING),Modal("du bist nicht eingelogt",MODAL_TYPE.ERROR,headline="satanismus") ,Redirect("/"))
        return_response.body = return_json
    else:
        print(token)
        # verify token
        print(verify_token(str(token), ip))
        success, perms, username = verify_token(str(token), ip)
        if success:
            return_response.status = HTTPStatus.OK
            user_dict = get_users()
            return_response.body = get_json_from_args(user_dict)
            print(return_response.body)
        else:
            return_response.status = HTTPStatus.UNAUTHORIZED
            print(
                get_json_from_args(
                    Alert("please log in", ALERT_TYPE.WARNING), Redirect("/login")
                )
            )
            return_response.body = get_json_from_args(
                Alert("Bitte einloggen!", ALERT_TYPE.WARNING), Redirect("/login")
            )

    print(return_response)
    return return_response


@app.get("/user/<username>")
def api_get_user(username):

    ip = request.environ.get("HTTP_X_FORWARDED_FOR") or request.environ.get(
        "REMOTE_ADDR"
    )

    return_response = get_default_response()
    return_response.status = HTTPStatus.UNAUTHORIZED

    request_params = dict(request.query.decode())

    print(request_params)

    try:
        token = request_params["token"]
    except Exception:
        token = None

    print(token)

    if token is None or len(token) < 2:
        return_response.status = HTTPStatus.UNAUTHORIZED
        return_json = get_json_from_args(
            Alert("please log in", ALERT_TYPE.WARNING), Redirect("/login")
        )
        return_response.body = return_json
    else:
        print(token)
        # verify token
        print(verify_token(str(token), ip))
        success, perms, user = verify_token(str(token), ip)
        include_mail = None
        if user == username or LoginConfig.admin_group_name in perms:
            include_mail = True
        if success:
            return_response.status = HTTPStatus.OK
            try:
                user_dict, token_dict, perm_dict = get_extended_info(
                    username, include_mail
                )
            except MissingUserException:
                return_response.status = HTTPStatus.BAD_REQUEST
                return_response.body = get_json_from_args(
                    Alert("User does not Exist", ALERT_TYPE.DANGER), Redirect("/users")
                )
                return return_response

            if LoginConfig.admin_group_name in perms:
                return_response.body = get_json_from_args(
                    {"user": user_dict},
                    {"token": token_dict},
                    {"groups": perm_dict},
                    {"Admin": True},
                )
            elif username == user:
                return_response.body = get_json_from_args(
                    {"user": user_dict}, {"token": token_dict}, {"groups": perm_dict}
                )
            else:
                return_response.body = get_json_from_args(
                    {"user": user_dict}, {"groups": perm_dict}
                )

            print(return_response.body)
        else:
            return_response.status = HTTPStatus.UNAUTHORIZED
            print(
                get_json_from_args(
                    Alert("please log in", ALERT_TYPE.WARNING), Redirect("/login")
                )
            )
            return_response.body = get_json_from_args(
                Alert("Bitte einloggen!", ALERT_TYPE.WARNING), Redirect("/login")
            )

    print(return_response)
    return return_response


@app.post("/user/delete/<username>")
def api_delete_user(username):
    return_response = get_default_response()

    return return_response


@app.get("/logout")
def api_logout_user():
    ip = request.environ.get("HTTP_X_FORWARDED_FOR") or request.environ.get(
        "REMOTE_ADDR"
    )
    return_response = get_default_response()
    return_response.status = HTTPStatus.UNAUTHORIZED

    request_params = dict(request.query.decode())
    print(request_params)

    try:
        token = request_params["token"]
    except Exception:
        token = None

    print(token)

    if token is not None:
        try:
            logout = {"Logout": logout_user(token, ip)}
            return_response.body = get_json_from_args(
                logout, Alert("successfull Logout", ALERT_TYPE.INFO), Redirect("/")
            )
        except TokenMissingException:
            return_response.status = HTTPStatus.BAD_REQUEST
            return_response.body = get_json_from_args(
                logout, Alert("Token does not exist!", ALERT_TYPE.DANGER)
            )
        except ValueError:
            return_response.status = HTTPStatus.BAD_REQUEST
            return_response.body = get_json_from_args(
                logout,
                Alert("cant Log Out User from Different IP!", ALERT_TYPE.WARNING),
            )
    else:
        return_response.status = HTTPStatus.BAD_REQUEST
        return_response.body = get_json_from_args(
            Alert("no Token transmitted", ALERT_TYPE.DANGER)
        )

    return return_response


@app.get("/avatars/<filename>")
def static_files(filename):
    return static_file(str(filename), root="./avatars/")


if __name__ == "__main__":

    # init base ad config
    ad_config = AD_Config()

    # init db config
    db_config = DB_Config(
        provider="mysql",
        host="127.0.0.1",
        port=3306,
        user="test",
        pw="test123",
        db_name="users",
    )

    # init db config with db config and other parameters
    config = LoginConfig(
        db_config=db_config,
        debug=True,
        auto_activate_accounts=False,
        admin_group_name="administrator",
    )

    # generate our admin user if it does not exist yet
    try:
        create_user(uname="admin", pw="12345", email="test@local", auth=AUTH_TYPE.LOCAL)
        # if user is new we need to verify the token if auto activate is disabled
        if not LoginConfig.auto_activate_accounts:
            print("since new admin user is not activated we try to activate him")
            auth_token = get_token("admin", ActivationCode)
            feedback = list(verify_token(token=auth_token, token_type=ActivationCode))
            print(f"success: {feedback[0]}")
    except AlreadyExistsException:
        print("user already exists")
    except Exception:
        print("somethign bad happened o-o")

    # add default admin group and add admin to it
    print(f"creating admin group: {LoginConfig.admin_group_name}")
    create_perm(LoginConfig.admin_group_name)

    print(f"adding admin user to {LoginConfig.admin_group_name} group")
    assign_perm_to_user("admin", LoginConfig.admin_group_name)

    app.run(host="0.0.0.0", port=1337, debug=True, server="bjoern")
