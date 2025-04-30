import uvicorn
import genshin
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os

port = int(os.environ.get("PORT", 8080))
uvicorn.run(app, host="0.0.0.0", port=port)

app = FastAPI()

class AuthData(BaseModel):
    ltuid: str
    ltoken: str
    uid: str

@app.post("/characters")
async def get_characters(data: AuthData):
    try:
        # 1. Создаем клиент
        client = genshin.Client()
        client.set_cookies(ltuid=data.ltuid, ltoken=data.ltoken)

        # 2. Получаем игровые аккаунты и устанавливаем нужный
        accounts = await client.get_game_accounts()
        account = next(acc for acc in accounts if str(acc.uid) == str(data.uid))
        client.set_game_accounts(account)

        # 3. Получаем список персонажей
        characters = await client.get_characters()

        # 4. Преобразуем результат
        result = {
            "uid": account.uid,
            "nickname": account.nickname,
            "characters": [
                {
                    "name": char.name,
                    "element": char.element.name if char.element else None,
                    "rarity": char.rarity,
                    "level": char.level,
                    "constellation": char.constellation,
                }
                for char in characters
            ]
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Ошибка: {str(e)}")

