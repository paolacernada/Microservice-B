import zmq
import json
from datetime import datetime

# Initialize ZeroMQ context and REP socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

log_file = "dice_rolls_log.json"


# Function to log a dice roll
def log_dice_roll(user_name, dice_result):
    with open(log_file, 'a') as f:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_name": user_name,
            "result": dice_result
        }
        f.write(json.dumps(log_entry) + "\n")


# Function to retrieve dice rolls for a specific user
def get_logs_for_user(user_name):
    logs = []
    try:
        with open(log_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    log_entry = json.loads(line)
                    if log_entry['user_name'] == user_name:
                        logs.append(log_entry)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return logs  # Return an empty list if no log file exists

    return logs


# Function to retrieve the last roll for a specific user
def get_last_roll_for_user(user_name):
    logs = get_logs_for_user(user_name)
    return logs[-1]['result'] if logs else []


print("Microservice B is running...")


while True:
    try:
        print("Awaiting data...")
        message = socket.recv_json()

        command = message.get('command', '')

        if command == 'log_roll':
            log_dice_roll(message['user_name'], message['result'])
            print("Logging roll...")
            socket.send_string("Roll logged successfully.")
            print("Roll logged successfully.")
        elif command == 'get_logs':
            logs = get_logs_for_user(message['user_name'])
            print("Retrieving logs...")
            socket.send_json(logs)
            print("Logs sent to client.")
        else:
            socket.send_string("Invalid command.")
            print("Response sent: Invalid command.")

    except zmq.ZMQError as e:
        print(f"Microservice B error: {e}")
        socket.send_string("Error occurred in Microservice B.")
        print("Response sent: Error occurred in Microservice B.")
