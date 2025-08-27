from celery import Celery

app = Celery('worker',
             broker='sqla+sqlite:///./broker.sqlite3',
             backend='db+sqlite:///./backend.sqlite3',
             include=['worker.tasks'])

app.conf.update(
    result_expires=10,
    timezone='Asia/Seoul',
    enable_utc=False,
)

app.conf.database_engine_options = {
    'echo': False,
}

app.conf.database_table_names = {
    'task': 'task_result',
    'group': 'group_meta',
}
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10.0,
        sender.tasks["celery.backend_cleanup"].s(),
        name="cleanup-expired-results-every-minute",
    )
