import pyrebase
from flask import Flask, request

app = Flask(__name__)

app.config["SECRET_KEY"] = "faslkdfjlaskdfjl;sdkfj"

firebaseConfig = {
    "apiKey": "AIzaSyApm0UL76BHxiC36wzJZRCxQH0tsfMlOPU",
    "authDomain": "ecell-d5d2c.firebaseapp.com",
    "databaseURL": "https://ecell-d5d2c-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "ecell-d5d2c",
    "storageBucket": "ecell-d5d2c.appspot.com",
    "messagingSenderId": "443301337374",
    "appId": "1:443301337374:web:1c055dab09946ba6e9110f",
    "measurementId": "G-H31BLZLNGT"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()


@app.route('/getinvestor/<string:id>', methods=["GET"])
def getinvestor(id):
    investor = db.child("investor").child(id).get()
    if investor.val() == None:
        return "No Data"
    return investor.val()


@app.route('/addCompanyUser', methods=["POST"])
def addinvestor():
    if request.method == "POST":
        data = request.get_json()
        print(data)

        db.child("companyUsers").child("3").push(data)

        return "Done"

    return "Error"


if __name__ == "__main__":
    app.run(debug=True)
