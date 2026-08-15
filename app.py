from flask import Flask, jsonify, request, render_template
import requests, argparse, json


app = Flask(__name__)

foodDB = [
    {
        'id': 1,
        'product': {
        'product_name': "Nutella",
        'ingredients': "Sugar"
        }
    },
    {
        'id': 2,
        'product': {
        'product_name': "Lemonade",
        'ingredients': "Lemon"
        }
    },
    {
        'id': 3,
        'product': {
        'product_name': "Plantain chips",
        'ingredients': "Plantain"
        }
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
    #MAKE [POST REQUEST]
    INVENTORY = {
        "data": foodDB
    }
    return jsonify(INVENTORY), 200

#specfic item:
@app.route('/inventory/<int:barcode>', methods=["GET"])
def show_food(args):
    url = f"https://world.openfoodfacts.net/api/v2/product/{args.barcode}?fields=product_name,ingredients"
    
    try:
        products = requests.get(url, timeout=5)
        
        products.raise_for_status()

        product_data = products.json()

        product_test = product_data.get('product')

        id_test = 1
        product_output = {
            "id": id_test + 1,
            "code": product_data["code"],
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
    for each in data:
        if each['id'] == id:
            id_tes = int(id)
            update_inventory = {
                'id':  id_tes + 1,
                'product': {
                    'product_name': data['product_name'],
                    'ingredients': data['ingredients']
        }
    }

    foodDB.append(update_inventory)
    output = {
        'message': "SUCCESSFUL...",
        'data': foodDB
    }
    return jsonify(output), 200

@app.route('/inventory/<int:id>', methods=["DELETE"])
def delete_item():
    pass


if __name__ == "__main__":
    app.run(port = 5000, debug= True)

def main():
    parser = argparse.ArgumentParser(description="REST API SUMLAB CLI...")
    subparsers = parser.add_subparsers()
    fetch_parser = subparsers.add_parser("Inventory")
    fetch_parser.set_defaults(func=fetch_inventory) #view inventory
#show food from barcode  -   update certain item  -  delete_item  -  add to inventory
    
    food_parser = subparsers.add_parser("FOODTEST")
    food_parser.add_argument('barcode')