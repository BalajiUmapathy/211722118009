import requests
from collections import deque
from flask import Flask, jsonify, request

app = Flask(__name__)
window = deque(maxlen=10)

# Your Bearer Token
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzQ5Nzk0NTgxLCJpYXQiOjE3NDk3OTQyODEsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6ImZhNDM3YjZiLWNjNGEtNDMyZC05M2U1LTJhYmJkMWVlMmFkNSIsInN1YiI6ImJhbGFqaS51LjIwMjIuY2NlQHJpdGNoZW5uYWkuZWR1LmluIn0sImVtYWlsIjoiYmFsYWppLnUuMjAyMi5jY2VAcml0Y2hlbm5haS5lZHUuaW4iLCJuYW1lIjoiYmFsYWppIHUiLCJyb2xsTm8iOiIyMTE3MjIxMTgwMDkiLCJhY2Nlc3NDb2RlIjoicFRUcXhtIiwiY2xpZW50SUQiOiJmYTQzN2I2Yi1jYzRhLTQzMmQtOTNlNS0yYWJiZDFlZTJhZDUiLCJjbGllbnRTZWNyZXQiOiJCYkF3Tmt6UVdLWXZaZVptIn0.m_JRMOvWEJpCDfvqO6Mq6Hm16NWu3UQTahNry_u0mBY"
@app.route("/numbers/<number_id>", methods=["GET"])
def get_number(number_id):
    allowed_numbers = ['p', 'f', 'e', 'r']
    if number_id not in allowed_numbers:
        return jsonify({"error": "Invalid number ID"}), 400

    map = {
        'p': 'http://20.244.56.144/evaluation-service/primes',
        'f': 'http://20.244.56.144/evaluation-service/fibo',
        'e': 'http://20.244.56.144/evaluation-service/even',
        'r': 'http://20.244.56.144/evaluation-service/rand'
    }

    api_url = map[number_id]

    try:
        # Include Authorization header
        response = requests.get(api_url, headers={
            "Authorization": f"Bearer {BEARER_TOKEN}"
        })
    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to external API"}), 503

    if response.status_code == 404:
        return jsonify({"error": "API not found"}), 404
    elif response.status_code != 200:
        return jsonify({"error": "Failed to fetch numbers"}), 502

    data = response.json()
    numbers = data.get("numbers", [])
    print(f"Fetched numbers: {numbers}")

    prev_state = list(window)
    new_numbers = [n for n in numbers if n not in window]

    for n in new_numbers:
        window.append(n)

    curr_state = list(window)
    avg = round(sum(curr_state) / len(curr_state), 2) if curr_state else 0.0

    return jsonify({
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": numbers,
        "avg": avg
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
