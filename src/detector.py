import socket
import json
import os
import logging
import numpy as np  # This is the 'Math Engine'

# 1. Setup Logging
log_path = os.path.join("logs", "alerts.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_path), logging.StreamHandler()]
)

def main():
    logging.info("Aegis Tactical Brain Online. Monitoring Signal Stream...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 5005))

    # This 'history' list is the Brain's memory
    history = []
    THRESHOLD = 3.0  # Sensitivity: How many standard deviations is 'dangerous'

    while True:
        data, addr = sock.recvfrom(1024)
        message = json.loads(data.decode())
        val = message.get("value")
        
        # Add the new value to memory
        history.append(val)
        
        # Keep memory to the last 50 signals so it stays fast
        if len(history) > 50:
            history.pop(0)

        # START THE ANOMALY DETECTION (Only after we have enough data to be accurate)
        if len(history) > 15:
            mean = np.mean(history)
            std = np.std(history)
            
            # The Z-Score Formula: (Current Value - Average) / Standard Deviation
            z_score = abs(val - mean) / std if std > 0 else 0
            
            if z_score > THRESHOLD:
                # This is the 'Tactical Alert'
                logging.warning(f"!!! ANOMALY DETECTED !!! Value: {val:.2f} | Z-Score: {z_score:.2f}")
            else:
                logging.info(f"Signal Nominal: {val:.2f}")
        else:
            # While the brain is still learning the baseline
            logging.info(f"Calibrating... Signal Received: {val:.2f}")

if __name__ == "__main__":
    main()