from celery import Celery

from rate_limiter import RequestsPerUserRateLimiter
from rediscli import get_cache


def make_celery():
    celery = Celery(
        'tasks',
        backend='amqp://guest@rabbitmq//',
        broker='amqp://guest@rabbitmq//'
    )
    # celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            # with app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery()

@celery.task(name='app.refill')
def refillTokens(userIds):
    print("refilling tokens for XXXXX")
    print(len(userIds))
    # print("populating cache for userid")
    # print(userId)
    for userId in userIds:
        maxLimit = RequestsPerUserRateLimiter.get_max_limit()
        get_cache().set(RequestsPerUserRateLimiter.USER_BUCKET_KEY + str(userId), maxLimit)