# Table of Contents
- [Table of Contents](#table-of-contents)
- [1. pyusermanager Example implementation](#1-pyusermanager-example-implementation)
  - [1.1. About](#11-about)
  - [1.2. Info](#12-info)
- [2. Configuration](#2-configuration)
  - [2.1. api.py (api)](#21-apipy-api)
  - [2.2. base.py (web_interface)](#22-basepy-web_interface)
- [3. How to install](#3-how-to-install)
  - [3.1. Pre Requires](#31-pre-requires)
    - [3.1.1. pip modules](#311-pip-modules)
    - [3.1.2. Misc.](#312-misc)
    - [3.1.3. Clone the repository](#313-clone-the-repository)
    - [3.1.4. build jquery](#314-build-jquery)
- [4. How to run](#4-how-to-run)
  - [4.1. API](#41-api)
  - [4.2. Web Interface](#42-web-interface)


# 1. pyusermanager Example implementation
## 1.1. About
this is an example implementation of pyusermanager in an api backend for a webiste where you can do the following
* Log In
* Log Out
* Register
* Delete own Account
* Delete other Accounts as admin
* do changes to your account
* change other accounts as admin

## 1.2. Info
the api is written so it creates an user called "admin" authenticated by "12345" with the specified admin group

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

## 2.2. base.py (web_interface)
in line 8 you finde the following
```
config={"api_url":"http://172.28.117.204:1337"}
```
its the api url for the api backend

# 3. How to install
## 3.1. Pre Requires
### 3.1.1. pip modules
* [pyusermanager](https://pypi.org/project/pyusermanager/) >=1.0.5
* [bottle](https://pypi.org/project/bottle/)
* [bjoern](https://pypi.org/project/bjoern/)
  * you could also use any other wsgi server like gevent or just the reference
* npm (to install jquery which is required for the frontend)

### 3.1.2. Misc.
for Debian/Ubuntu you need libev-dev to install bjoern

### 3.1.3. Clone the repository
* git clone --recurse-submodules https://github.com/Aurvandill137/pyusermanager_reference_implementation
### 3.1.4. build jquery
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