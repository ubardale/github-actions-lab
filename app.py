def add(a, b):
    """A tiny function to give our pipeline something real to build and test."""
    return a + b


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    print("2 + 3 =", add(2, 3))
    print("Is 17 prime?", is_prime(17))
