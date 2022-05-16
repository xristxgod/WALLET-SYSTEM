from celery import Celery
from config import Config

celery_app = Celery(
    "worker",
    backend=Config.REDIS_URL,
    broker=Config.RABBITMQ_URL,
)
celery_app.conf.task_routes = {
    "worker.celery_worker.parser_message": "balancer-queue"
}
celery_app.conf.update(task_track_started=True)