
import PingTools
import subprocess
import logging
import time

ADDRESS = "8.8.8.8"
PORT = 80

class PortTest(PingTools.Ping):
    def __init__(self, ip_address: str = "127.0.0.1", ping_interval: int = 2, port: int = 80):
        super().__init__(ip_address, ping_interval)
        self.port = port
    
    def win_ping(self):
        """
        Stupid windows :(
        """
        while not self.stop_event.is_set():
            success = 0
            time_ms = 0
            
            result = subprocess.run(["telnet", self.ip_address, str(self.port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

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