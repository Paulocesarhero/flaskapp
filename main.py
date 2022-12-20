from flask import Flask, request, make_response, redirect

app = Flask(__name__)  # en este caso __name__ = main.py


@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    return f'Hello World Platzi, tu IP es {user_ip}'


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)
