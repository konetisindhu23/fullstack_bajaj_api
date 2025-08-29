from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def alternate_caps(s):
    res = []
    upper = True
    for c in s:
        if upper:
            res.append(c.upper())
        else:
            res.append(c.lower())
        upper = not upper
    return "".join(res)

@app.route("/bfhl", methods=["POST"])
def process_data():
    try:
        input_json = request.json
        full_name = input_json.get("full_name", "").strip().lower()
        dob = input_json.get("dob", "").strip()  
        email = input_json.get("email", "").strip()
        roll_number = input_json.get("roll_number", "").strip()
        if not full_name or not dob or not email or not roll_number:
            return jsonify({"is_success": False, "error": "Missing required user info (full_name, dob, email, roll_number)"}), 400

        user_id = f"{full_name}_{dob}"

        data = input_json.get("data", [])
        if not isinstance(data, list):
            return jsonify({"is_success": False, "error": "Input 'data' must be an array/list"}), 400

        numbers = []
        alphabets = []
        special_chars = []

        for item in data:
            item_str = str(item)
            if item_str.isdigit():
                numbers.append(item_str)
            elif re.fullmatch(r'[a-zA-Z]+', item_str):
                alphabets.append(item_str.upper())
            else:
                special_chars.append(item_str)

        even_numbers = [n for n in numbers if int(n) % 2 == 0]
        odd_numbers = [n for n in numbers if int(n) % 2 != 0]
        total_sum = str(sum(map(int, numbers))) if numbers else "0"

        all_alpha_chars = "".join(filter(str.isalpha, "".join(map(str, data))))
        concat_string = alternate_caps(all_alpha_chars[::-1])

        response = {
            "is_success": True,
            "user_id": user_id,
            "email": email,
            "roll_number": roll_number,
            "even_numbers": even_numbers,
            "odd_numbers": odd_numbers,
            "alphabets": alphabets,
            "special_characters": special_chars,
            "sum": total_sum,
            "concat_string": concat_string
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"is_success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
