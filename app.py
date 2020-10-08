from flask import Flask, json
from flask import Response

from rate_limiter import RequestsPerUserRateLimiter

app = Flask(__name__)
userRatelimiter = RequestsPerUserRateLimiter()


@app.route('/')
def index():
    resp = Response()
    resp.set_data('Rate limiter')
    return resp


@app.route('/get/<userId>',methods=["GET"])
def get(userId):
    resp = Response()
    # if enough tokens for the user in the bucket?
    # if yes decrement the token and allow the token
    if userRatelimiter.enoughTokens(userId):
        userRatelimiter.consumeToken(userId)
        resp.status_code = 200
        return resp
    else:
        resp.status_code=429
        resp.response=json.dumps({'message':'rate limited for user '+userId})
        return resp
    # if not deny
    return


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
