import random
import base64
import json

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

question_count = 3 # Warning, may break at double digits!!

weights = {'true':1,'false':1,'unknown':2}

images = [(['a pole','wires','a building'],'pole.png'),(['a building','a pole'],'building.png'),(['a tree','a building'],'tree.png'),(['wires','a pole'],'wires.png')]

unknown_images = ['vague.png']

done = []

multichoice_choices = ["a pole","a building","a tree","wires"]

def decode_answer(name):
    for k,v in images:
        if v == name:
            return k, v
    return None, None

def train_ai(id,answer):
    # TODO: Train the data for image ID id, with answer 'answer'
    pass

def _get_select(option,value):
    return """
<option value={value}>{option}</option>""".format(option=option, value=value)


def gen_final(uid):
    return """
<div class="question" id="q{}">
    <h1> Thank you for registering</h1>
    <p>You will be redirected shortly</h1>
</div>
""".format(uid)

def gen_dropdown(uid,image_b64,ans):
    question = "What is prominent in this image?"
    selects = "".join([_get_select(v,i) for i,v in enumerate(multichoice_choices)])
    return """
<div class="question" id="q{id}">
    <input type="hidden" name="{id}ans" value="{answer}"/>
    <div class="row questionrow">
        <h3>{question}</h3>
    </div>
    <div class="row">
        <img class="questionimage" src="data:image/png;base64,{image}"/>
    </div>
    <div class="row answerrow">
        <select id="choices" name="{id}choices" class="form-control">
            {selects}
        </select>
        <button id="{id}button" type="button" class="btn btn-success">Submit</button>
    </div>
</div>""".format(answer=ans, question=question, id=uid, image=image_b64, selects=selects)

def gen_yesno(uid,image_b64,ans,ask):
    question = "Can you see {} in this picture?".format(ask)
    return """
<div class="question" id="q{id}">
    <input type="hidden" name="{id}ans" value="{answer}"/>
    <input type="hidden" name="{id}ask" value="{ask}"/>
    <div class="row questionrow">
        <h3>{question}</h3>
    </div>
    <div class="row">
        <img class="questionimage" src="data:image/png;base64,{image}"/>
    </div>
    <input type="hidden" id="{id}button" name="{id}button" value=""/>
    <div class="row answerrow">
        <button id="{id}yes" type="button" class="btn btn-success">Yes</button>
        <button id="{id}no"  type="button" class="btn btn-danger">No</button>
    </div>
</div>""".format(question=question, ask=ask, id=uid, image=image_b64, answer=ans)

def process_answer(data):
    """
    Process the given answer to check it is correct
    """
    good_so_far = True # Innocent until proven guilty
    training_set = []
    for i in range(question_count):
        local_data = dict([(k[1:],v) for (k,v) in data.items() if k.startswith(str(i))])
        print("for I=",i," data:",local_data)
        if 'ans' in local_data:
            keys, identity = decode_answer(local_data["ans"])
            print("key",keys,"id",identity)
            if "ask" in local_data: # if it's a y/n question
                asked_key = local_data["ask"]
                answer = (local_data["button"] == '1') # Their answer
                if keys is None: # Unknown data, might learn something
                    if answer:
                        print("LEARNING!")
                        training_set.append((identity,answer))
                elif asked_key in keys: # it should be true
                    if not answer:
                        good_so_far = False
                        break
                elif asked_key not in keys: # it should be false
                    if answer:
                        good_so_far = False
                        break
                else:
                    raise Exception("Logic Error")
            else: # Otherwise, it's a choice
                answer = multichoice_choices[int(local_data["choices"])]
                print("Their Answer:",answer)
                if keys is None: # Don't know the answer
                    print("LEARNING")
                    training_set.append((identity, answer))
                elif answer in keys:
                    pass
                    # Correct!
                elif answer not in keys:
                    good_so_far = False
                    break

    if good_so_far:
        for uid,answer in training_set:
            train_ai(uid,answer)
        return True
    else:
        return False


@app.route('/correct')
def correct():
    return "Correct!"

@app.route('/', methods=['GET', 'POST'])
def captcha_form():
    tried = False
    if request.method == 'POST':
        print("Received post")
        if process_answer(request.form):
            print("Correct!")
            return redirect("https://google.com")
        else:
            print("False!")
            tried = True
            # Carry on with the normal rendering

    #Generate the questions
    questions = []
    while len(questions) < question_count:
        uid = len(questions)
        image, ask, t, f, u = decide_image()
        with open("images/"+image, "rb") as image_file:
            encoded_string = str(base64.b64encode(image_file.read()))[2:-1]
            if random.randint(0,1):
                if (image,ask) not in done:
                    questions.append(gen_yesno(uid, encoded_string, image, ask))
            else:
                if (image) not in done:
                    questions.append(gen_dropdown(uid, encoded_string, image))
    questions.append(gen_final(uid+1))
    return render_template("form.html",tried=tried, answer=image, questions="".join(questions))

def decide_image():
    total = sum(weights.values())
    r = random.randint(1,total)
    is_true = r <= weights['true']
    is_false = weights['true'] < r <= weights['true'] + weights['false']
    is_unknown = total - weights['unknown'] < r <= total
    if is_true:
        # a known correct image
        ask, image = random.choice(images)
        ask = random.choice(ask)
    elif is_false:
        # a known incorrect image
        notask, image = random.choice(images)
        ask = random.choice([k for k,v in images if k is not notask])
        ask = random.choice(ask)
    elif is_unknown:
        # an unknown image
        image = random.choice(unknown_images)
        ask = random.choice(multichoice_choices)
    else:
        raise Exception("logic error")
    return image, ask, is_true, is_false, is_unknown


if __name__ == "__main__":
    app.run()
