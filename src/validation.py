import re
from typing import List


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def check_duplicate_emails(emails: List[str]) -> bool:
    return len(emails) == len(set(emails))


def validate_budget(budget: int) -> bool:
    return budget >= 0
