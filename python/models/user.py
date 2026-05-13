import bcrypt
from database import fetch_all, fetch_one, execute

def hash_password(password: str) -> str:
    """Encrypt the password before saving it to the database."""
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    """Compare inserted password with the stored hash."""
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed.encode("utf-8")
    )

def get_all_users():
    """Get a list of all users."""
    return fetch_all("SELECT * FROM Users")

def get_user_by_id(user_id):
    """Retrieve user information by ID."""
    return fetch_one(
        "SELECT * FROM Users WHERE UserID = %s",
        (user_id,)
    )

def get_user_by_email(email):
    """Retrieve user information by email."""
    return fetch_one(
        "SELECT * FROM Users WHERE Email = %s",
        (email,)
    )

def create_user(username, email, phone, password):
    """Create a new user with a hashed password, return the newly created UserID."""
    existing_user = get_user_by_email(email)
    if existing_user:
        return None
    
    hashed = hash_password(password)
    return execute(
        "INSERT INTO Users (UserName, Email, PhoneNumber, PasswordHash) " \
        "VALUES (%s, %s, %s, %s)",
        (username, email, phone, hashed)
    )

def create_initial_account(user_id, bank_name, balance):
    """Create the initial bank/wallet account for a new user."""
    return execute(
        "INSERT INTO BankAccounts (UserID, BankName, Balance) VALUES (%s, %s, %s)",
        (user_id, bank_name, balance)
    )

def login_user(email, password):
    """
    Verify email + password
    Return user object if successful, else None
    """
    user = get_user_by_email(email)
    if not user:
        return None
    if verify_password(password, user["PasswordHash"]):
        return user
    return None

def user_exists(user_id):
    """Check if the user exists."""
    result = fetch_one(
        "SELECT COUNT(*) AS cnt FROM Users WHERE UserID = %s",
        (user_id,)
    )
    return result["cnt"] > 0