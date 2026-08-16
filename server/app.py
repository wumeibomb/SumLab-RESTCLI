from flask import Flask, jsonify, request, render_template
import requests, argparse, json


app = Flask(__name__)

foodDB = [
    {
        'id': 1,
        'code': 3017624010701,
        'product': {
        'product_name': "Nutella",
        'ingredients': "Sugar"
        }
    },
    {
        'id': 2,
        'code': 3760049790672,
        'product': {
        'product_name': "La Boulangerie viennoises",
        'ingredients': "Flour"
        }
    },
    {
        'id': 3,
        'code': 3284230001991,
        'product': {
        'product_name': "Brioche tressee pur beurre",
        'ingredients': "Flour"
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
def fetch_inventory(args):
    if request.method == "POST":
        data = request.get_json()

        post_product = {
            "id": len(foodDB) + 1,
            "code": f"{args.barcode}",
            'product': {
                'product_name': f"{args.name}",
                'ingredients': f"{args.ingredient}"
            }
        }

        foodDB.append(post_product)
        output = {"data": post_product, "message": "PRODUCT ADDED"}
        return jsonify(output), 201

    INVENTORY = {
        "data": foodDB
    }

    print(INVENTORY)
    return jsonify(INVENTORY), 200

#specfic item:
@app.route('/inventory/<int:barcode>', methods=["GET"])
def show_food(barcode):
    url = f"https://world.openfoodfacts.net/api/v2/product/{barcode}?fields=product_name,ingredients"
    
    try:
        products = requests.get(url, timeout=5)
        
        products.raise_for_status()

        product_data = products.json()
        
        product_test = product_data.get('product')

        id_test = 1
        product_output = {
            "id": id_test + 1,
            "code": product_data["code"],
            "product": {
            "name": product_test["product_name"],
            "ingredients": product_test["ingredients"][0]['text']
            }
        }

        return jsonify({"message": "FOOD OUTPUT", "data": product_output}), 200
    except requests.exceptions.HTTPError as http_error:
        return jsonify({ "error" : http_error})
    #get request for product name via barcode


@app.route('/inventory/<int:id>', methods=["PATCH"])
def update_product(id,args):
    data = request.get_json()

    #FIX THIS
    for each in foodDB:
        if each.id == id:

            update_inventory = {
                'id': id,
                'code': f"{args.barcode}",
                'product': {
                'product_name': f"{args.product_name}",
                'ingredients': f"{args.ingredients}"
                }
            }

    foodDB.append(update_inventory)
    output = {
        'message': "SUCCESSFUL...",
        'data': foodDB
    }
    return jsonify(output), 200

@app.route('/inventory/<int:id>', methods=["DELETE"])
def delete_product(id):

    for each in foodDB:
        if each('id') == id:
            return ("Deleted Event"), 204
        else: 
            return ("Event not found"), 404


def main():
    parser = argparse.ArgumentParser(description="REST API SUMLAB CLI...")
    subparsers = parser.add_subparsers()
    fetch_parser = subparsers.add_parser("Inventory", help= "List the inventory products")
    #fetch_parser.add_argument("Inventory")
    fetch_parser.set_defaults(func=fetch_inventory) #view inventory
#show food from barcode  -   update certain item  -  delete_item  -  add to inventory
    
    food_parser = subparsers.add_parser("FOODTEST", help= "Add food barcode to get info")
    food_parser.add_argument('barcode')

    update_parser = subparsers.add_parser("Update")
    update_parser.add_argument('product_name')
    update_parser.add_argument('ingredients')
    

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    app.run(port = 5000, debug= True)