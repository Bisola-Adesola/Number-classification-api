from flask import Flask, request, jsonify
import requests
import math
import logging
import os

app = Flask(__name__)  # Corrected __name__

# Configure logging
logging.basicConfig(level=logging.INFO)

# Welcome Route for Stage 0
@app.route('/')
def welcome():
    return "Welcome to DevOps Stage 0"

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is a perfect number (optimized)."""
    if n < 1:
        return False
    divisors = {1}
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return sum(divisors) == n

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    if n < 0:
        return False  # Armstrong numbers are usually positive
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

def get_fun_fact(n):
    """Fetch a fun fact from the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json", timeout=5)
        if response.status_code == 200:
            return response.json().get("text", "No fun fact available")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch fun fact for {n}: {e}")
        return "No fun fact available"
    return "No fun fact available"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_str = request.args.get('number')

    if not number_str:
        return jsonify({"error": "Missing 'number' parameter"}), 400

    try:
        number = int(number_str)
    except (ValueError, TypeError):
        return jsonify({"error": f"Invalid input '{number_str}'. Please provide an integer."}), 400

    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 else "even")

    result = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(number))),  # Handle negative numbers
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(result), 200  # Corrected indentation

if __name__ == '__main__':  # Corrected __name__
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)
 
