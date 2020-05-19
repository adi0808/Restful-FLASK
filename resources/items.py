from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class ItemList(Resource):

    def get(self):
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}


class Item(Resource):
    parser = reqparse.RequestParser()   # class variable and we will use this in post and put
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field is reuired and can't be blank")
    parser.add_argument("store_id",
        type=int,
        required=True,
        help="Every Item needs a store_id")


    #@jwt_required()
    def get(self, name):
        # item = next(filter(lambda a: a["name"] == name, items), None)
        # return {"item": item}, 200 if item else 404  # None is False in boolean
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "No items found for this"}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with the '{}' already exists.".format(name)}, 400   # for bad request 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)  # or "price": data["price"], store_id = data["store_id"] as they are accordingly set so we can use **kwargs
        try:
            item.save_to_db()
        except:
            return {"message": "Error occurred while inserting"}, 500


        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404


    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data["price"]
        else:
            item = ItemModel(name, **data)  # creating new item if doesn't exists

        item.save_to_db()

        return item.json()
