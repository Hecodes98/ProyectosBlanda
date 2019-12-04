import requests
import base64
from static.vendor.core.CycleGAN import CycleGAN
from flask import Flask, jsonify, request, render_template
from static.vendor.classes.Image import Image

gan=CycleGAN()

last_image = Image("")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/image', methods=['POST'])
def image():
    file=request.form.get('imgBase64')
    #guardando imagen
    imgdata = base64.b64decode(file.split(',')[1])

    if imgdata != last_image.content:
        last_image.content = imgdata

        filename = './static/assets/img.jpg'
        with open(filename, 'wb') as f:
            f.write(imgdata)


        #gan.generate_image('./static/assets/demo/2_B.jpg')
        gan.generate_image(filename)

        #devolviendo imagen
        img_string=""
        with open('./static/assets/generated.png', 'rb') as f:
            img_string = base64.b64encode(f.read())

        return "data:/image/png;base64,"+str(img_string)[2:-1]
    else:
        print("entre")
        return "false"



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    #app.run(host='192.168.26.117', port=port)
    app.run(host='0.0.0.0', port=port)
