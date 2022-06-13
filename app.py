import secrets
from datetime import datetime, timezone

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/create", methods=["GET"])
def create():
	room_code = generate_code()
	rooms[room_code] = {"chat": []}

	if request.mimetype == "application/json":
		return jsonify({ "room_code": room_code })

	return f"{room_code}"

@app.route("/chat/<room_code>", methods=["GET", "POST"])
def chat(room_code):
	if request.method == "GET":
		if rooms.get(room_code):
			if request.mimetype == "application/json":
				return jsonify(rooms.get(room_code)["chat"])
			else:
				return "\n".join([f"{chat_item.get('timestamp')} {chat_item.get('content')}" for chat_item in rooms.get(room_code)["chat"]])
	elif request.method == "POST":
		if not request.get_json():
			return ("", 400)
		timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
		content = request.get_json().get("content")

		if rooms.get(room_code):
			rooms[room_code]["chat"].append({"timestamp": timestamp, "content": content})
			return ("", 201)

	return ("", 404)

def generate_code():
	return secrets.token_urlsafe(8)

rooms = {}
