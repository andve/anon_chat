#!/usr/bin/env python

import getopt
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
	print("usage: simple_client [-c | -r <code>] [-s <message> | -g | -h]")

url = os.environ.get("URL") or "http://localhost:8000"

try:
	opts, args = getopt.getopt(sys.argv[1:], "cr:m:gh")
except getopt.GetoptError as err:
	print(f"error: {err.msg}")
	sys.exit(2)

if len(opts) == 0:
	print("error: no options given")
	sys.exit()

g_flag = False
room_code = ""
message = ""

for o, a in opts:
	if o == "-c":
		try:
			response = create_room()
		except requests.exceptions.ConnectionError:
			print("error: connection failure")
			sys.exit()
		if response.status_code != 200:
			print("error: room not created")
		else:
			print(response.text)
		sys.exit()
	elif o == "-r":
		room_code = a
	elif o == "-m":
		message = a
	elif o == "-g":
		g_flag = True
	elif o == "-h":
		print_usage()
		sys.exit()
	else:
		assert False, "unhandled option"

if not room_code:
	print("error: no room code given")
	sys.exit()

if g_flag:
	try:
		response = retrieve_messages(room_code)
	except requests.exceptions.ConnectionError:
		print("error: connection failure")
		sys.exit()
	if response.status_code == 404:
		print("error: invalid code")
	else:
		print(response.text)
else:
	try:
		response = send_message(room_code, message)
	except requests.exceptions.ConnectionError:
		print("error: connection failure")
		sys.exit()
	if response.status_code == 201:
		print("message sent")
	else:
		print("error: message not sent")
