# Import the pytest library
import pytest
from add import add_numbers
# Function to test the add_numbers function
def test_add_numbers():
    # Define test inputs and expected output
    num1 = 5
    num2 = 7
    expected_result = 12
    
    # Call the function and get the result
    result = add_numbers(num1, num2)
    
    # Assert that the result matches the expected output
    assert result == expected_result, f"Addition failed: {num1} + {num2} did not equal {expected_result}"
