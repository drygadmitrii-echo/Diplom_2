from generators import *

class HTTPStatus:
    CREATED = 201
    INTERNAL_ERROR = 500
    BAD_REQUEST = 400
    FORBIDDEN = 403
    OK = 200
    REDIRECT = 302
    UNAUTHORIZED = 401
    NOT_FOUND = 404

class ResponseMessages:
    SUCCESS = "success"
    FAILURE = "success"
    REDIRECT_LOCATION = "/login"

class ErrorMessages:
    USER_EXISTS = {"success": False, "message": "User already exists"}
    MISSING_FIELDS = {"success": False, "message": "Email, password and name are required fields"}
    INVALID_CREDENTIALS = {"success": False, "message": "email or password are incorrect"}
    NO_INGREDIENTS = {"success": False, "message": "Ingredient ids must be provided"}

class UserData:
    valid_user = {
        "email": generate_email(),
        "password": generate_secure_password(),
        "name": generate_username()
    }

    invalid_logins = [
        {  # корректные данные логина
            "email": valid_user["email"],
            "password": valid_user["password"]
        },
        {  # данные входа с неправильным логином
            "email": generate_email(),
            "password": valid_user["password"]
        },
        {  # данные входа с неправильным паролем
            "email": valid_user["email"],
            "password": generate_secure_password()
        }
    ]

    incomplete_users = [
        {  # данные регистрации без пароля
            "email": generate_email(),
            "password": "",
            "name": generate_username()
        },
        {  # данные регистрации без email
            "email": "",
            "password": generate_secure_password(),
            "name": generate_username()
        },
        {  # данные регистрации без имени
            "email": generate_email(),
            "password": generate_secure_password(),
            "name": ""
        }
    ]

class OrderData:
    valid_order = {"ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]}
    empty_order = {"ingredients": []}
    invalid_ingredients = {"ingredients": ["61c0c5a71d1f82001bdaaa6d", "invalid_hash_12345"]}