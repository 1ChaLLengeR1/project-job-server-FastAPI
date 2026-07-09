from core.helper.password import hash_password, verify_password


class TestPasswordHelper:
    def test_password01_hash_and_verify_roundtrip(self):
        hashed = hash_password("TajneHaslo123!")

        assert hashed != "TajneHaslo123!"
        assert verify_password("TajneHaslo123!", hashed) is True

    def test_password02_wrong_password_fails(self):
        hashed = hash_password("poprawne")

        assert verify_password("niepoprawne", hashed) is False

    def test_password03_same_password_gives_unique_hashes(self):
        # bcrypt soli każdy hash — dwa hashe tego samego hasła muszą się różnić
        assert hash_password("haslo") != hash_password("haslo")
