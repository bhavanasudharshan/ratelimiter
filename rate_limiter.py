from rediscli import get_cache


class RequestsPerUserRateLimiter:  # token based rate limiter
    USER_BUCKET_KEY = "bucket:user:requests:"
    RATE_LIMIT_KEY = "ratelimit:user:requests"

    def __init__(self):
        self.maxlimit = get_cache().get(RequestsPerUserRateLimiter.RATE_LIMIT_KEY)
        if self.maxlimit is None:
            self.maxlimit = 5
        self.bucketLimit = self.maxlimit  # initially all tokens are free
        self.userBuckets = {}

    def enoughTokens(self, userId):
        v = get_cache().get(RequestsPerUserRateLimiter.USER_BUCKET_KEY + userId)
        if v is None:
            # user bucket is not available
            get_cache().set(RequestsPerUserRateLimiter.USER_BUCKET_KEY + userId, self.maxlimit)
            return True
        elif int(v) <= 0:
            return False
        else:
            return True

    def consumeToken(self, userId):
        get_cache().decr(RequestsPerUserRateLimiter.USER_BUCKET_KEY + userId)
