import time

from worker.tasks import do_work


def send_task():
    do_work.delay()

if __name__ == "__main__":
    while True:
        send_task()
        time.sleep(0.5)
