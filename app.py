from flask import Flask, request, jsonify
import genshin
import asyncio

app = Flask(__name__)

@app.route("/get_characters", methods=["POST"])
def get_characters():
    data = request.json
    ltuid = data.get("ltuid")
    ltoken = data.get("ltoken")
    uid = data.get("uid")

    if not ltuid or not ltoken or not uid:
        return jsonify({"status": "error", "message": "Missing ltuid, ltoken or uid"}), 400

    try:
        # Запускаем асинхронную функцию в обычной синхронной обертке
        result = asyncio.run(fetch_characters(ltuid, ltoken, uid))
        return jsonify({"status": "success", "characters": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


async def fetch_characters(ltuid, ltoken, uid):
    client = genshin.Client()
    client.set_cookies(ltuid=ltuid, ltoken=ltoken)

    record = await client.get_full_genshin_user(uid=int(uid))
    characters = record.characters

    return {
        char.name: char.constellations_unlocked
        for char in characters
    }


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
