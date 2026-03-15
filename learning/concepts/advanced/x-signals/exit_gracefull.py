import signal
import sys
import time


def handle_exit(signum, frame):
    print(f"Exiting gracefully. {signum}, {frame}")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

time.sleep(100)
# $ python Python/advanced/x-signals/exit_gracefull.py
# ^CExiting gracefully. 2, <frame at 0x7f591fe6a640, file 'Python/advanced/x-signals/exit_gracefull.py', line 14, code <module>>
