import hmac
import hashlib


class RNG:
    """
    Simple pseudo-random number generator based on SHA-256.
    
    Can generate variable-length unsigned integers (from 1 to 16 bytes).

    This RNG is not safe for cryptographic use.

    Some basic statistical tests are undertaken in statistical_tests.py
    """

    _byte_order: str = "little"

    def _to_int(self, number: bytes) -> int:
        return int.from_bytes(number, RNG._byte_order)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __init__(self, salt: int = 0, gen_number_length: int = 4):
        if gen_number_length > 16:
            raise ValueError("Number length must be <= 16")
        self.number_len = gen_number_length
        salt_bytes = salt.to_bytes(self.number_len, RNG._byte_order)
        msg = bytes(gen_number_length)
        self._hmac = hmac.new(salt_bytes, msg, digestmod=hashlib.sha256)

    def get(self) -> int:
        """Get random number"""
        mac = self._hmac.digest()
        to_int = lambda x: int.from_bytes(x, RNG._byte_order)
        totally_random_number = to_int(mac[self.number_len : 2 * self.number_len])
        next_seed = mac[0 : self.number_len]
        self._hmac.update(next_seed)

        return totally_random_number
