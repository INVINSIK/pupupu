from flask import Flask, request, jsonify
import genshin

app = Flask(__name__)

@app.route("/get_characters", methods=["POST"])
def get_characters():
    try:
        data = request.json
        ltuid = data.get("ltuid")
        ltoken = data.get("ltoken")
        uid = data.get("uid")

        if not all([ltuid, ltoken, uid]):
            return jsonify({"status": "error", "message": "ltuid, ltoken и uid обязательны"}), 400

        client = genshin.Client()
        client.set_cookies({"ltuid": str(ltuid), "ltoken": str(ltoken)})

        account = client.get_genshin_user(uid)
        characters = {char.name: char.constellation for char in account.characters}

        return jsonify({"status": "ok", "characters": characters})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)