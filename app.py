from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

foodDB = [
    {
        'id': 1,
        'code': 3017624010701,
        'product_name': "Nutella",
        'ingredients': "Sugar"
    }
]
@app.route('/')
def index():
    return render_template('index.html')

#addd approute for the api with a get request and a post request
#cli for the API
#testing?
#add. edit view an delete inventory environemtns(our own database)
#get methid for the api BARCODE OR NAME
#display all and display one

@app.route('/inventory', methods = ["GET", "POST"])
#all items
def fetch_inventory():
    pass


#specfic item:
@app.route('/inventory/<int:barcode>', methods=["GET"])
def show_food(barcode):
    url = f"https://world.openfoodfacts.net/api/v2/product/{barcode}?fields=product_name,ingredients"
    
    try:
        products = requests.get(url, timeout=5)
        
        products.raise_for_status()

        product_data = products.json()

        product_test = product_data.get('product')
        
        product_output = {
            "id": product_data["code"],
            "name": product_test["product_name"],
            "ingredients": product_test["ingredients"][0]["text"]
            #need to add a few more ingredients...
        }

        return jsonify({"message": "FOOD OUTPUT", "data": product_output}), 200
    except requests.exceptions.HTTPError as http_error:
        return jsonify({ "error" : http_error})
    #get request for product name via barcode


@app.route('/inventory/<int:id>', methods=["PATCH"])
def update_item(id):
    data = request.get_json()

    id_tes = data['id']
    update_inventory = {
        'id':  id_tes + 1,
        'code': id,
        'product_name': "Nutella",
        'ingredients': "Sugar"
    }


@app.route('/inventory/<int:id>', methods=["DELETE"])
def delete_item():
    pass


if __name__ == "__main__":
    app.run(port = 5000, debug= True)

