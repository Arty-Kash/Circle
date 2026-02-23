# --- 準備：ライブラリのインストール ---
!pip install fastapi uvicorn pyngrok nest-asyncio matplotlib

import nest_asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from pyngrok import ngrok
import matplotlib.pyplot as plt
import io
import base64

# --- APIの基本設定 ---
app = FastAPI()

# 別の端末（JavaScript）からの通信を許可する設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# JavaScriptから届くデータの形式定義
class CircleRequest(BaseModel):
    radius: float

@app.post("/draw_circle")
async def draw_circle(request: CircleRequest):
    # 1. 円を描画する
    plt.figure(figsize=(4, 4))
    circle = plt.Circle((0.5, 0.5), request.radius * 0.05, color='blue', fill=True) # 半径を調整
    ax = plt.gca()
    ax.add_patch(circle)
    ax.set_aspect('equal')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.axis('off') # 枠線を消す

    # 2. 描画した絵をメモリ上のデータ（Buffer）に保存する
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close() # メモリ解放
    buf.seek(0)
    
    # 3. 画像データを「文字列（Base64）」に変換する
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    return {"image_data": img_str}

# --- サーバーの起動 ---
# ngrokのトークンをここに入れてください
ngrok.set_auth_token("39zaWf2ZjAF5ns7LTsJ14H0yK2j_77WxJ1YDcFekDhiJT2Cem")

# 公開用URLを発行
public_url = ngrok.connect(8000)
print(f"JavaScriptに貼り付けるURLはこれです: {public_url.public_url}/draw_circle")

nest_asyncio.apply()
uvicorn.run(app, host="0.0.0.0", port=8000)