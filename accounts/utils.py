import hashlib


def create_gravatar_url(email: str, size: int = 100) -> str:
    email_hash = hashlib.md5(email.strip().lower().encode("utf-8")).hexdigest()
    url = f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"
    return url
