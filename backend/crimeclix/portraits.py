import os
import requests
import json
from flask import Blueprint, request, current_app, send_from_directory

bp = Blueprint("portraits", __name__, url_prefix="/portraits")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/", methods=("GET", "POST"))
def portraits():
    if request.method == "POST":
        response = json.loads(request.data)

        portrait_src = response.get("portrait")

        if not portrait_src:
            return {"error": "portrait is required"}, 400

        portrait = requests.get(portrait_src, allow_redirects=True)

        response = requests.post(
            "https://api.web3.storage/upload",
            headers={"Authorization": "Bearer " +
                     current_app.config["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDlhNDU0RjVFZDUyOWE4MEJmMkY1MmJjMDFhZmUwNjNmOTExNDhhRDkiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2ODIwMDU2ODE1MzIsIm5hbWUiOiJDcmltZXBsaXgifQ.xqWpxSkDCkrei4HOu5ZKdhwPplaETe0SjWCn9UC4zt4"]},
            data=portrait.content,
        ).json()

        return response, 201

    response = requests.get(
        "https://api.web3.storage/user/uploads",
        headers={
            "Authorization": "Bearer " + current_app.config["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDlhNDU0RjVFZDUyOWE4MEJmMkY1MmJjMDFhZmUwNjNmOTExNDhhRDkiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2ODIwMDU2ODE1MzIsIm5hbWUiOiJDcmltZXBsaXgifQ.xqWpxSkDCkrei4HOu5ZKdhwPplaETe0SjWCn9UC4zt4"]
        }
    ).json()
    imgList = []
    for img in response:
        imgList.append(img['cid'])
    return {'data': imgList}


@bp.route("/<path:name>", methods=("GET",))
def portrait(name):
    return send_from_directory(
        os.path.join("..", current_app.config["UPLOAD_FOLDER"]), name
    )
