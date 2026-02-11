"""
Manual end-to-end test for UserService flow.

This script:
1. Registers a user (via auth)
2. Gets user profile
3. Changes phone
4. Changes username
5. Changes password (correct flow)
6. Tests wrong current password
7. Tests duplicate username protection

No mocks.
Works with real JSON storage.
"""

# from services.auth_service import register_user
# from services.user_service import (
#     change_phone,
#     change_username,
#     change_password,
#     get_user_profile,
# )
# from utils.exceptions import (
#     UsernameAlreadyExistsError,
#     WrongPasswordError,
#     PasswordMismatchError,
# )

# def run_user_service_flow_test():
#     print("\n=== USER SERVICE FLOW TEST START ===\n")

#     username = "user_service_test"
#     password = "StrongPass123"
#     birth_date = "2000-01-01"
#     phone = "09123456789"

#     # --- Register user (setup) ---
#     print("1) Register user...")
#     user = register_user(username, password, birth_date, phone)
#     user_id = user.id
#     print(f"✓ User registered | id={user_id}")

#     # --- Get profile ---
#     print("\n2) Get user profile...")
#     user = get_user_profile(user_id)
#     print(f"✓ Profile loaded | username={user.username} | role={user.role.value}")

#     # --- Change phone ---
#     print("\n3) Change phone...")
#     new_phone = "09987654321"
#     user = change_phone(user_id, new_phone)
#     if user.phone == new_phone:
#         print("✓ Phone updated")
#     else:
#         print("✗ Phone update failed")

#     # --- Change username ---
#     print("\n4) Change username...")
#     new_username = "user_service_test_new"
#     user = change_username(user_id, new_username)
#     if user.username == new_username:
#         print("✓ Username updated")
#     else:
#         print("✗ Username update failed")

#     # --- Duplicate username test ---
#     print("\n5) Duplicate username check...")
#     try:
#         change_username(user_id, new_username)
#         print("✓ Same username allowed (no change needed)")
#     except UsernameAlreadyExistsError:
#         print("✗ Duplicate username incorrectly blocked")

#     # --- Change password (success) ---
#     print("\n6) Change password (correct flow)...")
#     new_password = "NewStrongPass123"
#     user = change_password(
#         user_id,
#         current_password=password,
#         new_password=new_password,
#         confirm_password=new_password
#     )
#     print("✓ Password changed successfully")

#     # --- Wrong current password ---
#     print("\n7) Change password with wrong current password...")
#     try:
#         change_password(
#             user_id,
#             current_password="WrongPass",
#             new_password="AnotherPass123",
#             confirm_password="AnotherPass123"
#         )
#         print("✗ ERROR: Password changed with wrong current password!")
#     except WrongPasswordError:
#         print("✓ Wrong current password rejected")

#     # --- Password mismatch ---
#     print("\n8) Change password mismatch...")
#     try:
#         change_password(
#             user_id,
#             current_password=new_password,
#             new_password="Pass12345",
#             confirm_password="Different123"
#         )
#         print("✗ ERROR: Password mismatch accepted!")
#     except PasswordMismatchError:
#         print("✓ Password mismatch rejected")

#     print("\n=== USER SERVICE FLOW TEST END ===")


# if __name__ == "__main__":
#     run_user_service_flow_test()

