import pytest
from src.validation import validate_email, check_duplicate_emails, validate_budget


class TestValidateEmail:
    def test_valid_emails(self):
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@example.co.uk") is True
        assert validate_email("user+tag@domain.com") is True
        assert validate_email("123@test.fr") is True

    def test_invalid_emails(self):
        assert validate_email("") is False
        assert validate_email("notanemail") is False
        assert validate_email("@example.com") is False
        assert validate_email("user@") is False
        assert validate_email("user@.com") is False
        assert validate_email("user @example.com") is False


class TestCheckDuplicateEmails:
    def test_no_duplicates(self):
        emails = ["a@test.com", "b@test.com", "c@test.com"]
        assert check_duplicate_emails(emails) is True

    def test_with_duplicates(self):
        emails = ["a@test.com", "b@test.com", "a@test.com"]
        assert check_duplicate_emails(emails) is False

    def test_empty_list(self):
        assert check_duplicate_emails([]) is True

    def test_single_email(self):
        assert check_duplicate_emails(["test@test.com"]) is True


class TestValidateBudget:
    def test_positive_budget(self):
        assert validate_budget(10) is True
        assert validate_budget(100) is True
        assert validate_budget(1) is True

    def test_zero_budget(self):
        assert validate_budget(0) is True

    def test_negative_budget(self):
        assert validate_budget(-1) is False
        assert validate_budget(-100) is False
