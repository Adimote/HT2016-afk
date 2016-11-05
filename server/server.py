from flask import Flask, render_template
app = Flask(__name__)

known_images = ['yes.png', 'no.png', 'dunno.png']

@app.route('/')
def captcha_form():
    return render_template("form.html")


if __name__ == "__main__":
    app.run()
