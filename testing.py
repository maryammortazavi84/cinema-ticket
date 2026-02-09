"""
Manual end-to-end test for Authentication flow.

This script:
1. Registers a user
2. Tries duplicate registration
3. Logs in with correct credentials
4. Logs in with wrong password

No mocks.
Works with real JSON storage.
"""

# from services.auth_service import register_user, login_user
# from utils.exceptions import (
#     UsernameAlreadyExistsError,
#     UserNotFoundError,
#     InvalidCredentialsError,
# )


# def run_auth_flow_test():
#     print("\n=== AUTH FLOW TEST START ===\n")

#     username = "test_user"
#     password = "StrongPass123"
#     birth_date = "2000-01-01"
#     phone = "09123456789"

#     # --- Register ---
#     print("1) Register user...")
#     try:
#         user = register_user(username, password, birth_date, phone)
#         print(f"✓ Registered successfully | id={user.id}")
#     except UsernameAlreadyExistsError:
#         print("! User already exists (OK if you ran before)")

#     # --- Duplicate Register ---
#     print("\n2) Register duplicate user...")
#     try:
#         register_user(username, password, birth_date, phone)
#         print("✗ ERROR: Duplicate registration allowed!")
#     except UsernameAlreadyExistsError:
#         print("✓ Duplicate registration blocked")

#     # --- Login success ---
#     print("\n3) Login with correct password...")
#     try:
#         user = login_user(username, password)
#         print(f"✓ Login successful | id={user.id}")
#     except Exception as e:
#         print(f"✗ Login failed unexpectedly: {e}")

#     # --- Login wrong password ---
#     print("\n4) Login with wrong password...")
#     try:
#         login_user(username, "WrongPassword")
#         print("✗ ERROR: Logged in with wrong password!")
#     except InvalidCredentialsError:
#         print("✓ Wrong password rejected")

#     # --- Login non-existent user ---
#     print("\n5) Login non-existent user...")
#     try:
#         login_user("ghost_user", "123")
#         print("✗ ERROR: Non-existent user logged in!")
#     except UserNotFoundError:
#         print("✓ Non-existent user blocked")

#     print("\n=== AUTH FLOW TEST END ===")


# if __name__ == "__main__":
#     run_auth_flow_test()
