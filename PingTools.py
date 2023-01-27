"""
Ping Test class used to gather information.

Weirdly... A lot of this was written with some help from ChatGPT? Very neat.

"""

import subprocess
import time
import threading
import sys
import logging

class Ping():
    """
    Summary:
        Class for a ping testing session.
        - ip_address: An IP address, represented as a string in the form,
        "8.8.8.8". 
        - ping-interval: The seconds between pings.
    """
    def __init__(self, ip_address: str = "127.0.0.1", ping_interval: int = 2):
        self.ip_address = ip_address
        self.ping_interval = ping_interval
        self.stop_event = threading.Event()
        self.thread = None
        
        # append tuple (time, success, time_ms)
        # self.log = [("time", "time_ms")]
        self.log = [("time", "success", "time_ms")]
    
    def update_log(self, success: bool = 0, time_ms: float = 0):
        # gives as epoch time.
        # new_log = (time.time(), int(time_ms))
        new_log = (time.time(), bool(success), float(time_ms))
        self.log.append(new_log)
        logging.info(new_log)

    def win_ping(self):
        """
        Stupid windows :(
        """
        while not self.stop_event.is_set():
            success = 0
            time_ms = 0

            result = subprocess.run(["ping", "-n", "1", self.ip_address], stdout=subprocess.PIPE, universal_newlines=True)
            if result.returncode == 0:
                # Extract the time in milliseconds from the output
                time_ms = float(result.stdout.split("Average = ")[1].split("ms")[0])
                success = 1
                logging.debug("IS UP!")
            else:
                logging.debug("IS DOWN!")

            self.update_log(success, time_ms)

            time.sleep(self.ping_interval)
            if not self.thread.is_alive():
                break

    def ping(self):
        while True:
            success = 0
            time_ms = 0
            
            result = subprocess.run(["ping", "-c", "1", self.ip_address], stdout=subprocess.PIPE, universal_newlines=True)
            if result.returncode == 0:
                # Extract the time in milliseconds from the output
                time_ms = float(result.stdout.split("time=")[1].split(" ms")[0])
                success = 1
                logging.debug("IS UP!")
            else:
                logging.debug("IS DOWN!")

            self.update_log(success, time_ms)

            time.sleep(self.ping_interval)
            if not self.thread.is_alive():
                break
    
    def start(self):
        if sys.platform == "win32":
            self.thread = threading.Thread(target=self.win_ping)
        else:
            self.thread = threading.Thread(target=self.ping)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()
