# Notice
this repository is deprecated since it was written to use pyusermanager v1.0.5 which is deprecated

<h1 align="center">pyusermanager</h1>
<p align="center">
<a href="https://pypi.org/project/pyusermanager/"><img height="20" alt="PyPI version" src="https://img.shields.io/pypi/v/pyusermanager"></a>
<a href="https://pypi.org/project/pyusermanager/"><img height="20" alt="Supported python versions" src="https://img.shields.io/pypi/pyversions/pyusermanager"></a>
<br>
<a href="https://pypi.org/project/black"><img height="20" alt="Black badge" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://codeclimate.com/github/Aurvandill137/pyusermanager_reference_implementation/maintainability"><img src="https://api.codeclimate.com/v1/badges/6b41eb574f426c371a70/maintainability" /></a>
<br>
<a href="https://codeclimate.com/github/Aurvandill137/pyusermanager_reference_implementation/test_coverage"><img src="https://api.codeclimate.com/v1/badges/6b41eb574f426c371a70/test_coverage" /></a>
<a href="https://pyusermanager.readthedocs.io/en/latest/"><img height="20" alt="Documentation status" src="https://img.shields.io/badge/documentation-up-00FF00.svg"></a>
</p>


# 1. Info
this is an example implementation of pyusermanager in an api backend for a webiste where you can do the following
* Log In
* Log Out
* Register
* Delete own Account
* Delete other Accounts as admin
* do changes to your account
* change other accounts as admin

## 1.1. Table of Contents
- [1. Info](#1-info)
  - [1.1. Table of Contents](#11-table-of-contents)
- [2. Configuration](#2-configuration)
  - [2.1. api.py (api)](#21-apipy-api)
  - [2.2. base.py (web_interface)](#22-basepy-web_interface)
- [3. How to install](#3-how-to-install)
  - [3.1. pip modules](#31-pip-modules)
  - [3.2. Misc.](#32-misc)
  - [3.3. Clone the repository](#33-clone-the-repository)
  - [3.4. build jquery](#34-build-jquery)
- [4. How to run](#4-how-to-run)
  - [4.1. API](#41-api)
  - [4.2. Web Interface](#42-web-interface)

# 2. Configuration
## 2.1. api.py (api)
you can find the following code in api.py in
```
if __name__ == "__main__":
```
```
    #init db config
    db_config = DB_Config(provider = "mysql", host = "127.0.0.1",port = 3306, user = "test", pw = "test123", db_name = "users")

    #init db config with db config and other parameters
    config = LoginConfig(  
                    db_config=db_config,
                    debug = True,
                    auto_activate_accounts = False,
                    admin_group_name="administrator"
                    )
```
all config parameters should be self explaining

you can also change the default user the api creates here
```
create_user(uname="admin", pw="12345", email="test@local", auth=AUTH_TYPE.LOCAL)
```

## 2.2. base.py (web_interface)
in line 8 you finde the following
```
config={"api_url":"http://172.28.117.204:1337"}
```
its the api url for the api backend

# 3. How to install
## 3.1. pip modules
* [pyusermanager](https://pypi.org/project/pyusermanager/) >=1.0.5
* [bottle](https://pypi.org/project/bottle/)
* [bjoern](https://pypi.org/project/bjoern/)
  * you could also use any other wsgi server like gevent or just the reference
* npm (to install jquery which is required for the frontend)

## 3.2. Misc.
for Debian/Ubuntu you need libev-dev to install bjoern

## 3.3. Clone the repository
* git clone --recurse-submodules https://github.com/Aurvandill137/pyusermanager_reference_implementation
## 3.4. build jquery
* cd web_interface/jquery
* npm run build

and you are done

# 4. How to run
## 4.1. API
* head into the api subfolder
* run api.py with python3
## 4.2. Web Interface
* head into the web_interface Folder
* run base.py with python3
