from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"Message": "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"Message": "This store name already exists"}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"Message": "An error occurred while creating the store"}, 500
        return store.json(), 201

    def delete(self, name):
        if StoreModel.find_by_name(name):
            store = StoreModel(name)
            try:
                store.delete_from_db()
            except:
                return {"Message": "An error occurred while deleting the store"}, 500
            return {"Message": f"Store {name} was deleted successfully"}
        return {"Message": f"Store with the name {name} is not found"}

class StoreList(Resource):
    def get(self):
        return {"Stores": [store.json() for store in StoreModel.query.all()]}