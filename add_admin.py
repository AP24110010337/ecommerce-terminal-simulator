from services.auth_service import AuthService
from utils.data_manager import DataManager

if __name__ == "__main__":
    auth = AuthService()
    print("Creating admin user...")
    admin_uname = "admin"
    admin_pass = "admin123"
    
    # Try register first
    if auth.register(admin_uname, admin_pass, role="admin"):
        print(f"Admin '{admin_uname}' created with password '{admin_pass}'!")
    else:
        # User exists, just update role
        for u in auth.users.values():
            if u.username == admin_uname:
                u.role = "admin"
                auth.update_user_data(u)
        print(f"User '{admin_uname}' updated to Admin role!")
