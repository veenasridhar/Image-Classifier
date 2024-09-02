from flask import Flask,request,jsonify
import util

app = Flask(__name__)

@app.route("/classify_image",methods=['GET','POST']) # This is the route to our api call "/" depict the home url http://127.0.0.1:5000
def hello():
    image_data = request.form['image_data']
    response = jsonify(util.classify_image(image_data))
    response.headers.add('Access-Control-Allow-Origin',"*")
    
    return response

if __name__ =="__main__":
    print("Starting flask Server...")
    util.load_saved_artifacts()
    app.run(port=5000)

