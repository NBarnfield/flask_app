from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
#
# first_word = input("What is your first name?")
#     second_word = input("What is your second name?")
#     full_name = print("So your full name is {} {}. Good for you!".format(first_word, second_word))