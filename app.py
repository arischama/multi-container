import time
import redis
import random
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    teams = ["Nacional", "Medellin", "Junior", "Jaguares"]
    return "Pulsa Actualizar si crees que {} es el mejor equipo de fútbol del mundo. Solo has actualizado {} veces. REFRESCA MAS!!!\n".format(teams[random.randint(0,3)], count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
