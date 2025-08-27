import os
import random
import shutil
import time
from datetime import datetime

from celery import chain
from worker.celery import app

IMAGE_SAVE_DIR = "./"


def move_file(src: str, dst: str):
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    if os.path.exists(dst):
        print(f"[OK] 이미 목적지에 존재 (멱등 처리): {dst}")
        return dst

    if not os.path.exists(src):
        raise FileNotFoundError(f"원본 파일이 존재하지 않음: {src}")

    shutil.move(src, dst)
    print(f"[OK] 파일 이동 완료: {src} -> {dst}")
    return dst


# 1. 파일 이동 전용 태스크
@app.task
def move_file_task(gid, path):
    print(f"[TASK-move_file] {gid}, {path}")
    original_filename = os.path.basename(path)
    _, extension = os.path.splitext(original_filename)
    unique_filename = f"{gid}{extension}"
    today_str = datetime.now().strftime("%Y%m%d")
    new_path = os.path.join(IMAGE_SAVE_DIR, today_str)
    final_dest_path = os.path.join(new_path, unique_filename)

    return move_file(src=path, dst=final_dest_path)


# 2. HTTP 요청 전송 태스크
@app.task(ignore_result=True)
def mock_http_task(final_dest_path):
    print(f"[TASK-mock_http] {final_dest_path}")
    delay = random.uniform(0.2, 2.0)
    time.sleep(delay)
    if random.random() < 0.2:
        raise Exception("전송 실패 (네트워크 오류 시뮬레이션)")
    return {"hello": f"{final_dest_path}"}


# 3. 체인 실행 진입점 (do_work는 체인 시작만 담당)
def do_work(gid, path):
    # workflow = move_file_task.s(gid, path) | mock_http_task.s()
    # workflow()

    workflow = chain(
        move_file_task.s(gid, path),   # 1단계: 파일 이동
        mock_http_task.s()             # 2단계: HTTP 요청
    )
    workflow()  # 비동기로 실행
