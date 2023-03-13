import pyrebase
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
def addCompanyUser():
    if request.method == "POST":
        data = request.get_json()
        print(data)

        users = db.child("companyUsers").get()
        if (users.val() == None):
            length = 0
        else:
            length = len(users.val())
        # length = len(users.val())

        data["user"]["comID"] = "com"+str(length)
        data["user"]["remaining"] = 100
        data["company"]["id"] = "com"+str(length)
        data["company"]["remaining"] = 100

        db.child("companyUsers").child(length).push(data["user"])
        db.child("company").child(length).push(data["company"])

        return "Done"

    return "Error"


@app.route('/addInvestor', methods=["POST"])
def addInvestor():
    if (request.method == "POST"):
        data = request.get_json()
        print(data)

        db.child("investor").push(data)

        return "Done"

    return "Error"


@app.route('/addStock', methods=["POST"])
def addStock():
    if request.method == "POST":
        data = request.get_json()
        # print(data)

        comUser = db.child("companyUsers").get()
        # print(len(com.val()))
        # length = len(comUser.val())
        remaining = 0
        length = 0
        for i in comUser.val():
            length += 1
            flag = 0
            print("Data", i)
            if (i != None):
                for j in i:
                    keyNew = j
                    # print(i[j])
                    comUserN = i[j]
                    if (comUserN["comID"] == data["id"]):
                        remaining = comUserN["remaining"]
                        flag = 1
                        break

            if flag == 1:
                break

        # print(investments)
        remaining = remaining-data["amount"]
        print("Remaining", remaining)

        if remaining < 0:
            return "No Equity"

        investmentsInv = []
        balance = 0

        user = db.child("investor").get()
        for i in user.val():
            key = i
            inv = user.val()[key]
            # print(inv, key)
            if (inv["email"] == data["email"]):
                print(inv)
                investmentsInv = inv["investments"]
                balance = inv["balance"]
                break

        if (investmentsInv != ""):
            investmentsInv.append({
                "id": data["id"],
                "amount": data["equity"],
                "equity": data["amount"]
            })
        else:
            investmentsInv = [{
                "id": data["id"],
                "amount": data["equity"],
                "equity": data["amount"]
            }]

        # print(balance)
        balance = balance-data["equity"]

        if (balance < 0):
            return "No Balance"

        # print(investmentsInv, balance)

        db.child("investor").child(key).update({"investments": investmentsInv})
        db.child("investor").child(key).update({"balance": balance})

        com = db.child("company").get()
        # print(len(com.val()))
        # length = len(com.val())
        # print("Length: ", length)
        investments = {}
        length = 0
        for i in com.val():
            length += 1
            flag = 0
            # print(i)
            if (i != None):
                for j in i:
                    key = j
                    # print(i[j])
                    com = i[j]
                    if (com["id"] == data["id"]):
                        investments = com["investments"]
                        flag = 1
                        break

                if flag == 1:
                    break

        # print(investments)
        investments.append({
            "amount": data["equity"],
            "equity": data["amount"],
            "email": data["email"]
        })

        # print(investments)
        db.child("company").child(
            length-1).child(key).update({"investments": investments})
        
        comUser = db.child("companyUsers").get()
        # print(len(com.val()))
        # length = len(comUser.val())
        remaining = 0
        length = 0
        for i in comUser.val():
            length += 1
            flag = 0
            # print(i)
            if (i != None):
                for j in i:
                    keyNew = j
                    # print(i[j])
                    comUserN = i[j]
                    if (comUserN["comID"] == data["id"]):
                        remaining = comUserN["remaining"]
                        flag = 1
                        break

            if flag == 1:
                break

        # print(investments)
        remaining = remaining-data["amount"]
        print(remaining)

        db.child("companyUsers").child(length-1).child(keyNew).update({"remaining": remaining})

        com = db.child("company").get()
        length = 0
        for i in com.val():
            length += 1
            flag = 0
            # print(i)
            if (i != None):
                for j in i:
                    key = j
                    com = i[j]
                    if (com["id"] == data["id"]):
                        flag = 1
                        break
                
                if flag == 1:
                    break

        db.child("company").child(length-1).child(key).update({"remaining": remaining})

        return "Done"

    return "Error"


if __name__ == "__main__":
    app.run(debug=True)