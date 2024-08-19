from celery import Celery
from celery.schedules import crontab

from src.controllers.LoansController import LoansController

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def notify_users():
    loans_controller = LoansController()
    loans_controller.notify_due_soon()
    loans_controller.notify_due_today()
    loans_controller.notify_overdue()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour="7", minute="30", day_of_week='mon-fri'),
        notify_users.s(),
    )
