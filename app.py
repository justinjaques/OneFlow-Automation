from flask import Flask, request, jsonify
import threading
import requests
import os

app = Flask(__name__)


COMPANY_NAME = "Blueprint"

@app.route('/handle_sms', methods=["POST"])
def handle_sms_reply():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            phone_number = data.get('fromNumber', 'Unknown')
            message = data.get('text', 'No message')

            print(f"{COMPANY_NAME}, you received reply from {phone_number}: {message}")
            
            if message.lower() in ['y', 'yes']:
                response_message = f"You have subscribed to {COMPANY_NAME}'s notifications"
            elif message.lower() in ['n', 'no']:
                response_message = f"You have unsubscribed from {COMPANY_NAME}'s notifications"
            else:
                response_message = f"Invalid reply. Please respond with 'Y' or 'N'."

            try:
                resp = requests.post('https://textbelt.com/text', {
                    'phone': phone_number,
                    'message': response_message,
                    'replyWebhookUrl': 'http://107.201.157.230:5000/handle_sms',
                    'key': "553df227ee6b5643502d4fd312f13bc7cd833472vxmQm2Xy3anpwHqi07x33Pric",
                })
                if resp.status_code == 200:
                    return jsonify({
                        "status": "success",
                        "message": f"Received reply from {phone_number}"
                    }), 200
                else:
                    return jsonify({"error": "Failed to send SMS response."}), 500
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"error": "Invalid content type. Expecting JSON."}), 400
    else:
        return jsonify({"error": "Invalid request type"})

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
