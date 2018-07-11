import os
import time
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="Exact path to the file you want to watch")
parser.add_argument("--command", help="Command to run when a change is detected")

args = parser.parse_args()

class Watcher:
	def __init__(self, filename, command):
		self._cached_stamp = 0
		self.filename = filename
		self.command = command

	def watch(self):
		while True:
			try:
				time.sleep(1)
				stamp = os.stat(self.filename).st_mtime
				if stamp != self._cached_stamp:
					print("Changed detected. Executing", self.command)
					self._cached_stamp = stamp
					completed = subprocess.run(self.command, shell=True, capture_output=True)
					print("Output:", completed.stdout)
			except KeyboardInterrupt:
				print("Keyboard interrupt. Exiting")
				break

print("Watching", args.file)
w = Watcher(args.file, args.command)
w.watch()