import time
import random
import json
import socket

def generate_signal():
    """Generates a steady Gaussian signal with occasional tactical spikes."""
    base_value = 70
    # Add a tiny bit of random 'noise'
    noise = random.uniform(-2, 2)
    
    # 5% chance of a 'Tactical Anomaly' (The Spike)
    if random.random() < 0.05:
        return base_value + random.uniform(20, 40)
    
    return base_value + noise

def main():
    print("Aegis Sensor Online. Broadcasting to 'aegis_net'...")
    
    # We will send data over a simple UDP socket (fastest for signals)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('detector', 5005) # 'detector' is the name in our Docker Compose

    while True:
        signal_value = generate_signal()
        message = json.dumps({"value": signal_value, "timestamp": time.time()})
        
        # Send the "Sensed" data
        sock.sendto(message.encode(), server_address)
        
        print(f"Signal Transmitted: {signal_value:.2f}")
        time.sleep(0.5) # Send 2 signals per second

if __name__ == "__main__":
    main()