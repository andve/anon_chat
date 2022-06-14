#!/usr/bin/env python

import os
import json
import sys

import requests

def create_room():
    return requests.get(f"{url}/create")

def send_message(room_code, message):
	payload = json.dumps({"content": message})
	return requests.post(f"{url}/chat/{room_code}",
		headers={"Content-Type": "application/json"}, data=payload)

def retrieve_messages(room_code):
	return requests.get(f"{url}/chat/{room_code}")

def print_usage():
	print("usage: simple_client [-c | -s <code> <message> | -r <code>]")

url = os.environ.get("URL") or "http://localhost"

if len(sys.argv) == 1:
	print("error: no options given")
	print_usage()
	sys.exit(1)

if sys.argv[1] == "-c":
	response = create_room()
	if response.status_code != 200:
		print("error: room not created")
	else:
		print(response.text)
elif sys.argv[1] == "-s":
	if len(sys.argv) < 4:
		print("error: not enough arguments")
		sys.exit(1)
	response = send_message(sys.argv[2], sys.argv[3])
	if response.status_code == 201:
		print("message sent")
	else:
		print("error: message not sent")
elif sys.argv[1] == "-r":
	if len(sys.argv) < 3:
		print("error: not enough arguments")
		sys.exit(1)
	response = retrieve_messages(sys.argv[2])
	if response.status_code == 404:
		print("error: invalid code")
	else:
		print(response.text)
