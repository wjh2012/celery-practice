from celery import Celery

app = Celery('app',
             broker='sqla+sqlite:///./broker.sqlite3',
             backend='db+sqlite:///./backend.sqlite3',
             include=['app.tasks'])

app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()