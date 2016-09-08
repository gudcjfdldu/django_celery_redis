from celery.decorators import task
from celery.utils.log import get_task_logger

import views

@task(name="visit_task")
def visit_user_task(userid):
    get_task_logger('do visit task')
    return views.visit(userid)
