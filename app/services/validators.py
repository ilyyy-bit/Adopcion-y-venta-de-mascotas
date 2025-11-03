
import re
def validar_email(email: str) -> bool:
    if not email: return True
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))
def validar_identificacion(ident: str) -> bool:
    return bool(ident and ident.strip())
