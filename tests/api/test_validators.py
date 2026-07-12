import pytest

from api.validators import is_valid_uuid, validate_non_empty_str, validate_required_fields, validate_uuid


class TestIsValidUuid:
    def test_uuid01_valid_v4_returns_true(self):
        assert is_valid_uuid("6fa459ea-ee8a-4ca4-894e-db77e160355e") is True

    def test_uuid02_v1_uuid_returns_false(self):
        # domyślnie walidujemy wersję 4
        assert is_valid_uuid("d9428888-122b-11e1-b85c-61cd3cbb3210") is False

    def test_uuid03_garbage_returns_false(self):
        assert is_valid_uuid("nie-uuid") is False
        assert is_valid_uuid("") is False


class TestValidateUuid:
    def test_validate_uuid01_returns_value(self):
        value = "6fa459ea-ee8a-4ca4-894e-db77e160355e"

        assert validate_uuid(value) == value

    def test_validate_uuid02_raises_value_error(self):
        with pytest.raises(ValueError):
            validate_uuid("nie-uuid")


class TestValidateNonEmptyStr:
    def test_non_empty01_strips_and_returns(self):
        assert validate_non_empty_str("  tekst  ") == "tekst"

    def test_non_empty02_raises_on_whitespace_only(self):
        with pytest.raises(ValueError):
            validate_non_empty_str("   ")

    def test_non_empty03_raises_on_empty(self):
        with pytest.raises(ValueError):
            validate_non_empty_str("")


class TestValidateRequiredFields:
    def test_required01_all_present_returns_ok(self):
        is_valid, message = validate_required_fields({"a": 1, "b": 2}, ["a", "b"])

        assert is_valid is True and message == ""

    def test_required02_missing_fields_listed_in_message(self):
        is_valid, message = validate_required_fields({"a": 1}, ["a", "b", "c"])

        assert is_valid is False
        assert "b" in message and "c" in message
