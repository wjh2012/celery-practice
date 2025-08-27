import time
import uuid

from worker.tasks import do_work


def send_task():
    path = "/abc/def"
    gid = uuid.uuid4()

    do_work(path=path,gid=gid)
    print("task send")

if __name__ == "__main__":
    while True:
        send_task()
        time.sleep(0.5)
