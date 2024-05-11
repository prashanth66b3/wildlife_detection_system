import os
import uuid
import flask
import urllib
from PIL import Image
from keras.models import load_model
from flask import Flask, render_template, request
import numpy as np


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR, 'ResNetakhil.h5'))

classes = ['antelope', 'badger', 'bat', 'bear', 'bee', 'beetle', 'bison', 'boar', 'butterfly', 'cat', 'caterpillar', 'chimpanzee', 'cockroach', 'cow', 'coyote', 'crab', 'crow', 'deer', 'dog', 'dolphin', 'donkey', 'dragonfly', 'duck', 'eagle', 'elephant', 'flamingo', 'fly', 'fox', 'goat', 'goldfish', 'goose', 'gorilla', 'grasshopper', 'hamster', 'hare', 'hedgehog', 'hippopotamus', 'hornbill', 'horse', 'hummingbird', 'hyena', 'jellyfish', 'kangaroo', 'koala', 'ladybugs', 'leopard', 'lion', 'lizard', 'lobster', 'mosquito', 'moth', 'mouse', 'octopus', 'okapi', 'orangutan', 'otter', 'owl', 'ox', 'oyster', 'panda', 'parrot', 'pelecaniformes', 'penguin', 'pig', 'pigeon', 'porcupine', 'possum', 'raccoon', 'rat', 'reindeer', 'rhinoceros', 'sandpiper', 'seahorse', 'seal', 'shark', 'sheep', 'snake', 'sparrow', 'squid', 'squirrel', 'starfish', 'swan', 'tiger', 'turkey', 'turtle', 'whale', 'wolf', 'wombat', 'woodpecker', 'zebra']

ALLOWED_EXT = set(['jpg', 'jpeg', 'png', 'jfif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT


def predict(filename, model):
    img = Image.open(filename)
    img = img.resize((256, 256))  # Resize the image to (256, 256)
    img_array = np.array(img)
    img_array = img_array.reshape(1, 256, 256, 3)  # Reshape the array
    img_array = img_array.astype('float32')
    img_array = img_array / 255.0

    result = model.predict(img_array)
    predicted_class_index = np.argmax(result[0])
    predicted_class="Unknown"
    if(check(result[0][predicted_class_index])):
        predicted_class = classes[predicted_class_index]
    return predicted_class


@app.route('/')
def home():
    return render_template("animalindex.html")

def check(prob):
    threshold = 0.7
    # Check if the maximum probability is above the threshold
    if prob >= threshold:
        return True
    else:
        return False
@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict_image():
    target_img = os.path.join(os.getcwd(), 'static/imgs')
    if request.method == 'POST':
        if request.form:
            link = request.form.get('link')
            try:
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename + ".jpg"
                img_path = os.path.join(target_img, filename)
                with open(img_path, "wb") as output:
                    output.write(resource.read())
                img = filename

                predicted_class = predict(img_path, model)

                Harmlessanimals = ['antelope', 'bat', 'beetle', 'butterfly', 'cat', 'catterpillar', 'cockroach', 'cow',
                                   'crow', 'deer', 'dog', 'dolphin', 'donkey', 'dragonfly', 'duck', 'flamingo', 'fly',
                                   'goat', 'goldfish', 'goose', 'hamster', 'hedgehog', 'hummingbird', 'ladybugs',
                                   'moth', 'okapi', 'orangutan', 'owl', 'oyster', 'parrot', 'pelicaniformes', 'penguin',
                                   'pig', 'pigeon', 'possum', 'reindeer', 'sheep', 'sparrow', 'squirrel', 'woodpecker']
                Harmful_animals = ['badger', 'crab', 'eagle', 'fox', 'hippopotamus', 'hornbill', 'hyena', 'jellyfish',
                                   'leopard', 'lion', 'lobster', 'octopus', 'otter', 'porcupine', 'rhinoceros', 'shark',
                                   'snake', 'squid', 'tiger', 'whale', 'wolf', 'zebra']
                Semiharm = ['bear', 'bee', 'bison', 'boar', 'chimpanzee', 'coyote', 'elephant', 'gorilla', 'hare',
                            'horse', 'kangaroo', 'koala', 'lizard', 'mosquito', 'mouse', 'panda', 'raccon', 'rat',
                            'sandpiper', 'seahorse', 'seal', 'starfish', 'swan', 'turkey', 'turtle', 'wombat', 'ox']
                op = predicted_class
                type = ''
                if op in Harmlessanimals:
                    type = 'Harmless'
                elif op in Harmful_animals:
                    type = 'HarmFul'
                elif op in Semiharm:
                    type = "SEMI HARM"
                else:
                    type = "UNknown"

                return render_template('animalresult.html', img=img, predicted_class=predicted_class,type=type)

            except Exception as e:
                print(str(e))
                error = 'This image from this site is not accessible or inappropriate input'
                return render_template('animalindex.html', error=error)

        elif request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                unique_filename = str(uuid.uuid4())
                filename = unique_filename + ".jpg"
                img_path = os.path.join(target_img, filename)
                file.save(img_path)
                img = filename

                predicted_class = predict(img_path, model)
                Harmlessanimals = ['antelope', 'bat', 'beetle', 'butterfly', 'cat', 'catterpillar', 'cockroach', 'cow',
                                   'crow', 'deer', 'dog', 'dolphin', 'donkey', 'dragonfly', 'duck', 'flamingo', 'fly',
                                   'goat', 'goldfish', 'goose', 'hamster', 'hedgehog', 'hummingbird', 'ladybugs',
                                   'moth', 'okapi', 'orangutan', 'owl', 'oyster', 'parrot', 'pelicaniformes', 'penguin',
                                   'pig', 'pigeon', 'possum', 'reindeer', 'sheep', 'sparrow', 'squirrel', 'woodpecker']
                Harmful_animals = ['badger', 'crab', 'eagle', 'fox', 'hippopotamus', 'hornbill', 'hyena', 'jellyfish',
                                   'leopard', 'lion', 'lobster', 'octopus', 'otter', 'porcupine', 'rhinoceros', 'shark',
                                   'snake', 'squid', 'tiger', 'whale', 'wolf', 'zebra']
                Semiharm = ['bear', 'bee', 'bison', 'boar', 'chimpanzee', 'coyote', 'elephant', 'gorilla', 'hare',
                            'horse', 'kangaroo', 'koala', 'lizard', 'mosquito', 'mouse', 'panda', 'raccon', 'rat',
                            'sandpiper', 'seahorse', 'seal', 'starfish', 'swan', 'turkey', 'turtle', 'wombat', 'ox']
                op = predicted_class
                type= ''
                if op in Harmlessanimals:
                    type='Harmless'
                elif op in Harmful_animals:
                    type='HarmFul'
                elif op in Semiharm:
                    type="SEMI HARM"
                else:
                    type="UNknown"


                return render_template('animalresult.html', img=img, predicted_class=predicted_class,type=type)



            else:
                error = "Please upload images of jpg, jpeg, and png extension only"
                return render_template('animalindex.html', error=error)

    return render_template('animalindex.html')



if __name__ == "__main__":
    app.run(debug=True)
