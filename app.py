from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Функция для получения списка персонажей
def get_characters(ltuid, ltoken, uid):
    url = "https://bbs-api-os.hoyolab.com/game_record/genshin/api/character"
    headers = {
        "Cookie": f"ltuid={ltuid}; ltoken={ltoken}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Referer": "https://act.hoyolab.com/",
        "x-rpc-app_version": "2.34.1",
        "x-rpc-client_type": "5",
    }
    
    params = {
        "role_id": uid,
        "server": "os_euro",  # Убедись, что ты правильно указал сервер
    }
    
    # Отправляем GET запрос
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Ошибка API: {response.text}")
    
    data = response.json()
    
    if data['retcode'] != 0:
        raise Exception(f"Ошибка API: {data.get('message', 'Неизвестная ошибка')}")
    
    return data['data']['characters']

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
    app.run(debug=True)
