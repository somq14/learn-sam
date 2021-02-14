import unittest


class TestGetItem(unittest.TestCase):
    def test_success(self) -> None:
        self.assertEqual(1, 1)

    def test_failure(self) -> None:
        self.assertEqual(1, 2)
