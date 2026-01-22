from flask import jsonify

def success_response(message, data=None, status_code=200):
    payload = {"message": message}
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status_code

def error_response(message, status_code=400):
    return jsonify({"error": message}), status_code
