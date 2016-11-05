import random
import base64
import json

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

weights = {'true':1,'false':1,'unknown':2}

images = {'true':['yes.png'],'false':['no.png'],'unknown':['dunno.png']}

def decode_answer(name):
    for k,v in images.items():
        for i,img in enumerate(v):
            if img == name:
                return k, img

def train_ai(id,answer):
    # TODO: Train the data for image ID id, with answer 'answer'
    pass


def process_answer(data):
    """
    Process the given answer to check it is correct
    """
    if "ans" in data:
        key, identity = decode_answer(data["ans"])
        answer = ("yes" in data)
        if answer:
            print("they clicked yes")
        if key == "true":
            return answer
        if key == "false":
            return not answer
        if key == "unknown":
            train_ai(identity, answer)
            return True

@app.route('/correct')
def correct():
    return "Correct!"

@app.route('/', methods=['GET', 'POST'])
def captcha_form():
    if request.method == 'POST':
        print("Received post")
        if process_answer(request.form):
            print("Correct")
            return redirect(url_for('correct'))
        else:
            print("False!")
            # Carry on with the normal rendering
    image,t,f,u = decide_image()
    with open("images/"+image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return render_template("form.html", image=str(encoded_string)[2:-1], answer=image)

def decide_image():
    total = sum(weights.values())
    r = random.randint(1,total)
    is_true = r <= weights['true']
    is_false = weights['true'] < r <= weights['true'] + weights['false']
    is_unknown = total - weights['unknown'] < r <= total
    if is_true:
        # a known correct image
        chosen_images = images['true']
    elif is_false:
        # a known incorrect image
        chosen_images = images['false']
    elif is_unknown:
        # an unknown image
        chosen_images = images['unknown']
    else:
        raise Exception("logic error")
    image = chosen_images[random.randint(0,len(chosen_images)-1)]
    return image, is_true, is_false, is_unknown


if __name__ == "__main__":
    app.run()
