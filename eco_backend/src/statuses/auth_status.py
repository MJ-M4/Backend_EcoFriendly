from src.models.user_model import UserResponse

def login_success(user_obj):
    user_response = UserResponse.model_validate(user_obj)
    return {
        "status": "success",
        "message": "Login successful",
        "user": user_response.model_dump()
    }
