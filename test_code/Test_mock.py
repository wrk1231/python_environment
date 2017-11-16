import unittest
import mock
from mock import patch

class function():
    def add_and_multiply(self, x, y):
        addition = x + y
        multiple = self.multiply(x, y)
        subtraction = self.minus(x, y)
        return (addition, multiple, subtraction)

    def multiply(self, x, y):
        return x * y + 1

    def minus(self, x, y):
        return x - y + 1

class Test_mock(unittest.TestCase):
    @patch.object(function, "multiply")
    @patch.object(function, "minus")
    def test_add_and_multiply(self, mock_minus, mock_multiply):
        x = 3
        y = 5
        mock_multiply.return_value = 15
        mock_minus.return_value = -2
        addition, multiple, subtraction = function().add_and_multiply(x, y)
        self.assertEqual(8, addition)
        self.assertEqual(15, multiple)
        self.assertEqual(-2, subtraction)


if __name__ == "__main__":
    unittest.main()