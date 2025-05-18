def login_success(user):
    return {
        "status": "success",
        "message": "Login successful",
        "user": {
            "id": user.get_id(),
            "identity": user.get_identity(),
            "name": user.get_name(),
            "role": user.get_role().lower().strip(),
            "worker_type": user.get_worker_type()
        }
    }