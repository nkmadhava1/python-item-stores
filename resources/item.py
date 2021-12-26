from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
# import sqlite3
from models.item import ItemModel

class Items(Resource):
    def get(self):
        return {"Items": [item.json() for item in ItemModel.query.all()]}
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({"name": row[0], "price": row[1]})
        # connection.close()
        # return {"Items": items}

    # def get(self):
    #     if len(items) != 0:
    #         return items
    #     else:
    #         return {"Message": "No items are available in the items inventory"}
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This cannot be left blank")
    parser.add_argument("store_id", type=int, required=True, help="Every item needs to have a store id")
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"Message": "Item not found"}, 404
        # item = next(filter(lambda i: (i["name"]==name), items), None)
        # # for item in items:
        # #     if item["name"] == name:
        # return {"item": item}, 200 if item else 404
        # else:
        #     return {"Message": "No such item found"}, 404

    def post(self, name):
        # if next(filter(lambda i: (i["name"]==name), items), None):
        #     return {"Message": f"Item with the name {name} already exists"}, 400
        if ItemModel.find_by_name(name):
            return {"Message": f"Item with the name {name} already exists"}, 400
        # data = request.get_json()
        request_data = Item.parser.parse_args()
        # request_data = request.get_json()
        item = ItemModel(name, request_data["price"], request_data["store_id"])
        try:
            item.save_to_db()
        except:
            return {"Message": "An error occurred inserting the item"}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"Message": "Item deleted successfully"}
        # if ItemModel.find_by_name(name):
        #     connection = sqlite3.connect("data.db")
        #     cursor = connection.cursor()
        #     query = "DELETE FROM items WHERE name=?"
        #     cursor.execute(query, (name,))
        #     connection.commit()
        #     connection.close()
        #     return {"Message": f"Item {name} deleted successfully"}
        # return {"Message": f"Item with name {name} does not exist"}
        # global items
        # items = list(filter(lambda i: (i["name"]!=name), items))
        # return {"Message": "Item deleted"}
    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(name):
            item.price = data["price"]
        else:
            item = ItemModel(name, data["price"], data["store_id"])
        item.save_to_db()
        # item = next(filter(lambda i: (i["name"]==name), items), None)
        # if item is None:
        #
        #     items.append(item)
        # else:
        #     item.update(data)
        return item.json()