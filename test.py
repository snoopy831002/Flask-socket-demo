from flask import Flask, render_template
from flask_sockets import Sockets
import gevent
from gevent.lock import Semaphore

app = Flask(__name__)
app.debug = True

sockets = Sockets(app)

wsl = []

def process(ws,data):
        for w in wsl:
            w.send(data)

@sockets.route('/echo')
def echo_socket(ws):

    while True:
        message = ws.receive()
        print("message : "+message)

        if (message == "socket open"):
            data = ws.receive()
            wsl.append(ws)
            gevent.spawn(process, ws, data)

        else:
            process(ws, message)




@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()