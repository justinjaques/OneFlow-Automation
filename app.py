from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

@app.route('/handle_sms', methods=["POST"])
def handle_sms_reply():
    company_name = "Blueprint"
    
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            phone_number = data.get('fromNumber', 'Unknown')
            message = data.get('text', 'No message')

            print(f"{company_name}, you received reply from {phone_number}: {message}")
            return jsonify({
                "status": "success",
                "message": f"Received reply from {phone_number}"
            }), 200
        else:
            return jsonify({"error": "Invalid content type. Expecting JSON."}), 400
    else:
        return jsonify({"error": "Invalid request type"})

def run_flask():
    app.run(host='0.0.0.0', port=5000)  # Bind to all interfaces

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
