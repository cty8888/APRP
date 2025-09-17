import secrets
import string

def generate_secret_key(length=32):
    """生成安全的JWT密钥"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    # 生成一个安全的密钥
    secret_key = generate_secret_key(64)
    print("生成的JWT密钥:")
    print(secret_key)
    print(f'$env:SECRET_KEY="{secret_key}"')

