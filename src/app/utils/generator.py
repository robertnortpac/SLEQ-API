import secrets
import string

def generate_claim_code():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(18))

def generate_random_password():
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(16))

def generate_random_signature():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(65))