import random
import time

from worker.celery import app

@app.task
def do_work(gid, path):
    print(f"[TASK] {gid, path}")
    mock_http()

def mock_http():
    delay = random.uniform(0.2, 1.0)
    time.sleep(delay)
    if random.random() < 0.2:
        raise Exception("전송 실패 (네트워크 오류 시뮬레이션)")
    return {"hello": "world"}