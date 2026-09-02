from app import add, is_prime


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(17) is True
    assert is_prime(1) is False
    assert is_prime(18) is False


# --- Exercise 3 lives here: uncomment the next test to see a red pipeline ---
# def test_this_will_fail():
#     assert add(2, 2) == 5
