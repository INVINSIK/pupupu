from flask import Flask, request, jsonify
import genshin

app = Flask(__name__)

# Функция для получения списка персонажей
def get_characters(ltuid, ltoken, uid):
    # Создаем клиента с помощью ltuid и ltoken
    client = genshin.Client(cookie_token=f"ltuid={ltuid}; ltoken={ltoken}")
    
    # Получаем информацию о персонажах
    user = client.get_game_record(uid)
    characters = user.characters

    # Возвращаем список персонажей
    character_data = {char.name: char.constellation for char in characters}
    return character_data

@app.route("/get_characters", methods=["POST"])
def get_characters_route():
    try:
        # Получаем данные из POST-запроса
        data = request.json
        
        ltuid = data.get("ltuid")
        ltoken = data.get("ltoken")
        uid = data.get("uid")
        
        if not ltuid or not ltoken or not uid:
            return jsonify({"status": "error", "message": "ltuid, ltoken и uid обязательны!"}), 400
        
        # Получаем список персонажей
        characters = get_characters(ltuid, ltoken, uid)
        
        # Возвращаем результат
        return jsonify({
            "status": "success",
            "characters": characters
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Запуск сервера на порту 8080
    app.run(debug=True, host='0.0.0.0', port=8080)
