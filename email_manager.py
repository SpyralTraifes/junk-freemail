import uuid
import time
from redis_client import r

EMAIL_TTL = 600  # 10 minutes in seconds

def generate_email():
    local_part = uuid.uuid4().hex[:8]
    domain = "junkfreemail.com"
    address = f"{local_part}@{domain}"
    r.setex(address, EMAIL_TTL, "[]")  # store empty inbox
    return address

def store_email(to_address, email_data):
    if not r.exists(to_address):
        return False
    inbox = eval(r.get(to_address))
    inbox.append(email_data)
    r.setex(to_address, EMAIL_TTL, str(inbox))
    return True

def get_inbox(address):
    inbox = r.get(address)
    return eval(inbox) if inbox else []
