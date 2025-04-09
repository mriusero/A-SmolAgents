import requests
import urllib.parse
from smolagents import tool

@tool
def calculator(operation: str, expression: str) -> str:
    """
    A tool that performs advanced mathematical operations using the Newton API.
    Args:
        operation: The mathematical operation to perform (e.g., 'derive', 'integrate').
        expression: The mathematical expression to operate on.
    Returns:
        The result of the mathematical operation as a string.
    """
    encoded_expression = urllib.parse.quote(expression)
    url = f"https://newton.now.sh/api/v2/{operation}/{encoded_expression}"

    response = requests.get(url)

    if response.status_code == 200:
        result = response.json().get("result")
        return result
    else:
        return f"Error: Unable to fetch result. Status code: {response.status_code}"