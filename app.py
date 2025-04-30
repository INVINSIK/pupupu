import os
import genshin
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class AuthData(BaseModel):
    ltuid: str
    ltoken: str
    uid: str
    nickname: str

@app.post("/characters")
async def get_characters(data: AuthData):
    try:
        # Создаем клиент и логинимся
        client = genshin.Client()
        client.set_cookies(ltuid=data.ltuid, ltoken=data.ltoken)

        # Получаем персонажей
        chars = await client.get_genshin_characters(uid=int(data.uid))

        result = {
            "nickname": data.nickname,
            "uid": data.uid,
            "characters": [
                {
                    "name": char.name,
                    "constellation": char.constellation,
                    "level": char.level,
                    "element": char.element.value,
                }
                for char in chars
            ]
        }

        return result

    except genshin.errors.InvalidCookies as e:
        raise HTTPException(status_code=401, detail="Неверные куки: ltuid/ltoken недействительны")
    except genshin.errors.GenshinException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Ошибка: {repr(e)}")

# Запуск на правильном порту
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
