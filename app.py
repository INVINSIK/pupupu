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

        if not ltuid or not ltoken or not uid:
            return jsonify({"status": "error", "message": "Все поля обязательны!"}), 400

        client = genshin.Client()
        client.set_cookies(ltuid=ltuid, ltoken=ltoken)

        record = client.get_full_genshin_user(uid=uid)
        characters = record.characters

        result = {
            char.name: char.constellations_unlocked
            for char in characters
        }

        return jsonify({"status": "success", "characters": result})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
