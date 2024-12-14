from passlib.context import CryptContext

# Password hashing configuration using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def hash_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.
    :param password: The plain text password
    :return: The hashed password
    """
    return pwd_context.hash(password)

# Function to verify a password
def verify_password(input_password: str, hashed_password: str) -> bool:
    """
    Verifies if the input password matches the hashed password.
    :param input_password: The plain text password provided by the user
    :param hashed_password: The hashed password stored in the database
    :return: True if the password is correct, otherwise False
    """
    return pwd_context.verify(input_password, hashed_password)
