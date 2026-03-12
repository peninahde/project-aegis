import socket
import json
import os
import logging

# 1. Setup Logging (to see results in your 'logs' folder)
log_path = os.path.join("logs", "alerts.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_path), logging.StreamHandler()]
)

def main():
    logging.info("Aegis Detector Engine Online. Listening on Port 5005...")

    # 2. Create the UDP Socket (The 'Ear')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 5005)) # Listen to any incoming data on this port

    while True:
        # 3. Catch the 'Sensed' data
        data, addr = sock.recvfrom(1024)
        message = json.loads(data.decode())
        
        value = message.get("value")
        logging.info(f"Signal Received from Sensor: {value:.2f}")

if __name__ == "__main__":
    main()