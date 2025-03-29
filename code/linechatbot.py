from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
import os
import threading
from google.generativeai import configure, GenerativeModel

# 初始化
line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])
configure(api_key=os.environ["GEMINI_API_KEY"])
model = GenerativeModel("gemini-2.0-flash")

try:
    model.generate_content("你可以開始幫我回答了")  # 預熱
    print("[Gemini] 預熱成功")
except Exception as e:
    print("[Gemini] 預熱失敗", e)

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK", 200

conversation_memory = {}
MAX_MEMORY_LENGTH = 5

# 非同步回覆的處理函數
def generate_and_reply(user_input, user_id):
    try:
        # 初始化使用者對話紀錄
        if user_id not in conversation_memory:
            conversation_memory[user_id] = []

        # 新增當前問題到記憶
        conversation_memory[user_id].append({"role": "user", "content": user_input})

        # 擷取最近幾輪對話
        history = conversation_memory[user_id][-MAX_MEMORY_LENGTH:]

        # 組成 Gemini 用的提示詞（只取 content）
        prompt = "你是一位專業的人工智慧領域工作者，請根據以下對話回覆使用者：\n"
        for msg in history:
            role = "使用者" if msg["role"] == "user" else "AI"
            prompt += f"{role}：{msg['content']}\n"

        # 送出 Gemini 回覆
        res = model.generate_content(prompt)
        reply = res.text
        print("[Gemini 回覆]", reply)

        # 記錄 AI 回覆
        conversation_memory[user_id].append({"role": "ai", "content": reply})

        # 限制對話長度（FIFO）
        conversation_memory[user_id] = conversation_memory[user_id][-MAX_MEMORY_LENGTH:]

    except Exception as e:
        print("[Gemini ERROR]", e)
        reply = "⚠️ AI 回覆失敗，請稍後再試。"

    # 推送訊息給 LINE 使用者
    line_bot_api.push_message(
        user_id,
        TextSendMessage(text=reply)
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text
    user_id = event.source.user_id

    # 立即先回一段話（避免 webhook timeout）
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="思考中...🧠 請稍候幾秒！")
    )

    # 開 thread 處理 AI 回覆
    threading.Thread(target=generate_and_reply, args=(user_input, user_id)).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)