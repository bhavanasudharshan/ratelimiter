import threading

import time

from rate_limiter import RequestsPerUserRateLimiter
from rediscli import get_cache
from tasks import refillTokens

class RefillTokenScheduler:
    BATCH_SIZE = 5

    def __init__(self, interval):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            print("refill schedule starting")
            keys = get_cache().keys(RequestsPerUserRateLimiter.USER_BUCKET_KEY + "*")
            l = len(keys)
            print("found total "+str(l)+" keys")
            userIds = []
            count = 0
            for i in range(0, l):
                if count == self.BATCH_SIZE:
                    refillTokens.delay(userIds)
                    userIds = []
                    count = 0
                count = count + 1
                userIds.append(keys[i])

            if count < self.BATCH_SIZE:
                refillTokens.delay(userIds)  # refill the remaining tokens
            print("refilling sleeping")
            time.sleep(self.interval)
