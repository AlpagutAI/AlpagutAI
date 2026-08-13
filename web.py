import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("OPENAI_API_KEY bulunamadi.")
    
    raise SystemExit

client = OpenAI(api_key=api_key)

HTML = r"""
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Alpağut Yapay Zeka</title>

<style>
body {
    margin: 0;
    background: #090a0d;
    color: white;
    font-family: Arial, sans-serif;
}

.header {
    height: 110px;
    background: #111318;
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom: 1px solid #292c33;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-mark {
    width: 50px;
    height: 50px;
    border: 2px solid white;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    font-weight: bold;
}

.logo-text {
    font-size: 28px;
    font-weight: bold;
}

.status {
    text-align: center;
    color: #888;
    font-size: 13px;
    padding: 10px;
}

.chat {
    height: calc(100vh - 230px);
    overflow-y: auto;
    padding: 20px;
}

.message {
    max-width: 85%;
    padding: 15px 18px;
    margin-bottom: 14px;
    border-radius: 20px;
    font-size: 17px;
    line-height: 1.5;
    white-space: pre-wrap;
}

.ai {
    background: #202329;
    margin-right: auto;
    border-bottom-left-radius: 5px;
}

.user {
    background: #315bdc;
    margin-left: auto;
    border-bottom-right-radius: 5px;
}

.bottom {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #111318;
    border-top: 1px solid #292c33;
    padding: 10px;
}

.input-area {
    display: flex;
    gap: 10px;
    max-width: 900px;
    margin: auto;
}

input {
    flex: 1;
    height: 55px;
    border: none;
    outline: none;
    border-radius: 30px;
    padding: 0 20px;
    font-size: 17px;
}

button {
    width: 55px;
    height: 55px;
    border: none;
    border-radius: 50%;
    font-size: 22px;
    cursor: pointer;
}

.mic {
    background: #292c33;
    color: white;
}

.send {
    background: #315bdc;
    color: white;
}
</style>
</head>

<body>

<div class="header">
    <div class="logo">
        <div class="logo-mark">A</div>
        <div class="logo-text">Alpağut</div>
    </div>
</div>

<div class="status" id="status">
    Alpağut hazır
</div>

<div class="chat" id="chat">

<div class="message ai">
Merhaba! 👋

Ben Alpağut Yapay Zeka.

🎙️ Mikrofon düğmesine basarak
benimle konuşabilirsin.

🔊 Cevaplarımı da sesli vereceğim.
</div>

</div>

<div class="bottom">

<div class="input-area">

<input
id="message"
type="text"
placeholder="Alpağut'a yaz..."
>

<button class="mic" onclick="voice()">🎙️</button>

<button class="send" onclick="sendMessage()">➤</button>

</div>

</div>


<script>

const input = document.getElementById("message");
const chat = document.getElementById("chat");
const statusBox = document.getElementById("status");


input.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});


function addMessage(text, type) {

    const div = document.createElement("div");

    div.className = "message " + type;

    div.innerText = text;

    chat.appendChild(div);

    chat.scrollTop = chat.scrollHeight;

}


async function sendMessage() {

    const text = input.value.trim();

    if (!text) return;

    addMessage(text, "user");

    input.value = "";

    statusBox.innerText = "Alpağut düşünüyor...";

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text
            })

        });

        const data = await response.json();

        if (data.reply) {

            addMessage(data.reply, "ai");

            speak(data.reply);

        } else {

            addMessage(
                "Hata: " + data.error,
                "ai"
            );

        }

    } catch (error) {

        addMessage(
            "Sunucuya bağlanılamadı.",
            "ai"
        );

    }

    statusBox.innerText = "Alpağut hazır";

}


/* 🎙️ SESLİ KONUŞMA */

function voice() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        alert(
            "Tarayıcı sesli konuşmayı desteklemiyor."
        );

        return;
    }

    const recognition =
        new SpeechRecognition();

    recognition.lang = "tr-TR";

    recognition.continuous = false;

    recognition.interimResults = false;


    recognition.onstart = function() {

        statusBox.innerText =
            "🎙️ Seni dinliyorum...";

    };


    recognition.onresult = function(event) {

        const text =
            event.results[0][0].transcript;

        input.value = text;

        sendMessage();

    };


    recognition.onerror = function() {

        statusBox.innerText =
            "Ses algılanamadı.";

    };


    recognition.onend = function() {

        statusBox.innerText =
            "Alpağut hazır";

    };


    recognition.start();

}


/* 🔊 SESLİ CEVAP */

function speak(text) {

    if (!window.speechSynthesis) {

        return;
    }

    window.speechSynthesis.cancel();

    const speech =
        new SpeechSynthesisUtterance(text);

    speech.lang = "tr-TR";

    speech.rate = 0.95;

    speech.pitch = 1;

    speech.volume = 1;


    speech.onstart = function() {

        statusBox.innerText =
            "🔊 Alpağut konuşuyor...";

    };


    speech.onend = function() {

        statusBox.innerText =
            "Alpağut hazır";

    };


    window.speechSynthesis.speak(speech);

}

</script>

</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):

        result = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(result))
        )

        self.end_headers()

        self.wfile.write(result)


    def do_GET(self):

        if self.path == "/":

            result = HTML.encode("utf-8")

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                str(len(result))
            )

            self.end_headers()

            self.wfile.write(result)

        else:

            self.send_response(404)

            self.end_headers()


    def do_POST(self):

        if self.path != "/chat":

            self.send_response(404)

            self.end_headers()

            return


        try:

            length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            body = self.rfile.read(length)

            data = json.loads(
                body.decode("utf-8")
            )

            user_message = data.get(
                "message",
                ""
            ).strip()


            if not user_message:

                self.send_json({
                    "error": "Mesaj boş."
                }, 400)

                return


            response = client.responses.create(

                model="gpt-4o-mini",

                instructions="""
Sen Alpağut Yapay Zeka'sın.
Türkçe konuş.
Samimi, yardımsever ve anlaşılır ol.
Kısa ve doğal cevaplar ver.
""",

                input=user_message
            )


            reply = response.output_text


            self.send_json({
                "reply": reply
            })


        except Exception as e:

            self.send_json({
                "error": str(e)
            }, 500)


print("")
print("==============================")
print("     ALPAGUT YAPAY ZEKA V2")
print("==============================")
print("")
print("Bilgisayar: http://localhost:5000")
print("Telefon:    http://172.20.10.9:5000")
print("")
print("Durdurmak icin CTRL+C")
print("")


server = HTTPServer(
    ("0.0.0.0", 5000),
    Handler
)

server.serve_forever()
