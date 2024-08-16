
# Microservice B - Dice Roll Logger

## Overview
This microservice logs and retrieves dice roll results for individual users. It stores the results in a JSON file and can retrieve all past rolls for a user.

## Functionality
- Logs dice rolls for users.
- Retrieves all logged dice rolls for a user.

## Communication
- **Protocol:** ZeroMQ (REP-REQ)
- **Port:** `tcp://*:5556`
- **Endpoints:**
  - Logs dice rolls.
  - Retrieves past rolls for a specific user.

## Requirements
- ZeroMQ library.

## How to Run
1. Ensure ZeroMQ is installed.
2. Run the script using Python:
   ```bash
   python microservice_b.py
