from celery import Celery
from celery.schedules import crontab

app = Celery('app',
             broker='sqla+sqlite:///./broker.sqlite3',
             backend='db+sqlite:///./backend.sqlite3',
             include=['app.tasks'])

app.conf.update(
    result_expires=10,
    timezone='Asia/Seoul',
    enable_utc=False,
)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        # 1분마다 만료된 결과 정리
        # crontab(),
        # 10초마다 만료된 결과 정리
        10.0,
        sender.tasks["celery.backend_cleanup"].s(),
        name="cleanup-expired-results-every-minute",
    )
