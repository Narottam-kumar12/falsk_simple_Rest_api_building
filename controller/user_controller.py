from app import app
from model.user_model import user_model
from flask import request
from flask import make_response
obj = user_model()

@app.route("/user/getall")
def signup():
    return obj.user_getall_model()

@app.route("/user/addone", methods=["POST"])
def user_addone_controller():
    print("FORM:", request.form)
    print("JSON:", request.get_json(silent=True))
    return obj.user_addone_model(request.form)


@app.route("/user/update/<int:id>", methods=["PUT"])
def user_update_controller(id):
    return obj.user_update_model(request.args, id)

@app.route("/user/delete/<int:id>", methods=["DELETE"])
def user_delete_controller(id):
    return obj.user_delete_model(id)

@app.route("/user/patch/<int:id>", methods=["PATCH"])
def user_patch_controller(id):
    return obj.user_patch_model(request.form, id)

@app.route("/user/getall/limit/<limit>/page/<page>")
def user_pagination_controller(limit, page):
    return obj.user_pagination_model(limit, page)