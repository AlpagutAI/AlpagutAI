import os
import json
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("OPENAI_API_KEY bulunamadi.")
    raise SystemExit

client = OpenAI(api_key=API_KEY)

# Her kullanıcının ayrı sohbet hafızası
sessions = {}


HTML = r"""
<!DOCTYPE html>
<html lang="tr">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Alpağut Yapay Zeka</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #090a0d;
    color: white;
    font-family: Arial, sans-serif;
    height: 100vh;
    overflow: hidden;
}

/* HEADER */

.header {
    height: 105px;
    background: #111318;
    border-bottom: 1px solid #292c33;

    display: flex;
    align-items: center;
    justify-content: center;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-mark {
    width: 48px;
    height: 48px;

    border: 2px solid white;
    border-radius: 15px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 27px;
    font-weight: bold;
}

.logo-text {
    font-size: 27px;
    font-weight: bold;
}

.logo-sub {
    position: absolute;
    margin-top: 62px;

    color: #777;
    font-size: 10px;

    letter-spacing: 4px;
}

/* STATUS */

.status {
    height: 35px;

    display: flex;
    align-items: center;
    justify-content: center;

    color: #888;
    font-size: 12px;
}

/* CHAT */

.chat {
    height: calc(100vh - 220px);

    overflow-y: auto;

    padding: 20px 15px 120px;

    display: flex;
    flex-direction: column;
}

.message {
    max-width: 85%;

    padding: 15px 18px;

    margin-bottom: 14px;

    border-radius: 20px;

    font-size: 16px;

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

/* ALT */

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

    gap: 9px;

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

    font-size: 16px;
}

button {
    width: 55px;
    height: 55px;

    border: none;

    border-radius: 50%;

    font-size: 21px;

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

button:active {
    transform: scale(.94);
}


/* TELEFON */

@media(max-width:700px) {

    .header {
        height: 95px;
    }

    .logo-mark {
        width: 44px;
        height: 44px;

        font-size: 24px;
    }

    .logo-text {
        font-size: 24px;
    }

    .logo-sub {
        margin-top: 58px;
    }

    .message {
        max-width: 92%;
        font-size: 15px;
    }

}

</style>

</head>


<body>


<div class="header">

    <div class="logo">

        <div class="logo-mark">
            A
        </div>

        <div class="logo-text">
            Alpağut
        </div>

        <div class="logo-sub">
            YAPAY ZEKA
        </div>

    </div>

</div>


<div class="status" id="status">

    Alpağut hazır

</div>


<div class="chat" id="chat">

    <div class="message ai">

Merhaba! 👋

Ben Alpağut Yapay Zeka.

Bu sohbet boyunca söylediklerini
hatırlayabilirim.

Nasıl yardımcı olabilirim?

    </div>

</div>


<div class="bottom">

    <div class="input-area">

        <input
            id="message"
            type="text"
            placeholder="Alpağut'a yaz..."
            autocomplete="off"
        >

        <button
            class="mic"
            onclick="voice()">

            🎙️

        </button>

        <button
            class="send"
            onclick="sendMessage()">

            ➤

        </button>

    </div>

</div>


<script>


const input =
    document.getElementById("message");

const chat =
    document.getElementById("chat");

const statusBox =
    document.getElementById("status");


/* ENTER */

input.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);


/* MESAJ EKLE */

function addMessage(text, type) {

    const div =
        document.createElement("div");

    div.className =
        "message " + type;

    div.innerText = text;

    chat.appendChild(div);

    chat.scrollTop =
        chat.scrollHeight;

}


/* MESAJ GÖNDER */

async function sendMessage() {

    const text =
        input.value.trim();

    if (!text) {

        return;

    }


    addMessage(
        text,
        "user"
    );


    input.value = "";


    statusBox.innerText =
        "Alpağut düşünüyor...";


    try {

        const response =
            await fetch(
                "/chat",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: text
                    })

                }
            );


        const data =
            await response.json();


        if (data.reply) {

            addMessage(
                data.reply,
                "ai"
            );

            speak(
                data.reply
            );

        }

        else {

            addMessage(
                "Hata: " +
                (data.error || "Bilinmeyen hata"),
                "ai"
            );

        }


    }

    catch(error) {

        addMessage(
            "Sunucuya bağlanılamadı.",
            "ai"
        );

    }


    statusBox.innerText =
        "Alpağut hazır";

}


/* SESLİ KOMUT */

function voice() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Bu tarayıcı sesli konuşmayı desteklemiyor."
        );

        return;

    }


    const recognition =
        new SpeechRecognition();


    recognition.lang =
        "tr-TR";


    recognition.continuous =
        false;


    recognition.interimResults =
        false;


    recognition.onstart =
        function() {

            statusBox.innerText =
                "🎙️ Seni dinliyorum...";

        };


    recognition.onresult =
        function(event) {

            const text =
                event.results[0][0]
                    .transcript;


            input.value =
                text;


            sendMessage();

        };


    recognition.onerror =
        function() {

            statusBox.innerText =
                "Ses algılanamadı.";

        };


    recognition.onend =
        function() {

            statusBox.innerText =
                "Alpağut hazır";

        };


    recognition.start();

}


/* SESLİ CEVAP */

function speak(text) {

    if (!window.speechSynthesis) {

        return;

    }


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(
            text
        );


    speech.lang =
        "tr-TR";


    speech.rate =
        0.95;


    speech.pitch =
        1;


    speech.volume =
        1;


    speech.onstart =
        function() {

            statusBox.innerText =
                "🔊 Alpağut konuşuyor...";

        };


    speech.onend =
        function() {

            statusBox.innerText =
                "Alpağut hazır";

        };


    window.speechSynthesis
        .speak(speech);

}

</script>


</body>

</html>
"""


class Handler(BaseHTTPRequestHandler):


    def get_session(self):

        session_id = None

        if "Cookie" in self.headers:

            cookie =
                cookies.SimpleCookie(
                    self.headers["Cookie"]
                )

            if "ALPAGUT_SESSION" in cookie:

                session_id =
                    cookie["ALPAGUT_SESSION"].value


        if not session_id:

            session_id =
                str(uuid.uuid4())

            sessions[session_id] = {
                "response_id": None
            }


            self.send_header(
                "Set-Cookie",
                f"ALPAGUT_SESSION={session_id}; "
                "Path=/; HttpOnly; SameSite=Lax"
            )


        if session_id not in sessions:

            sessions[session_id] = {
                "response_id": None
            }


        return session_id


    def send_json(
        self,
        data,
        status=200
    ):

        result =
            json.dumps(
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


        self.wfile.write(
            result
        )


    def do_GET(self):

        if self.path != "/":

            self.send_response(404)

            self.end_headers()

            return


        result =
            HTML.encode("utf-8")


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


        self.wfile.write(
            result
        )


    def do_POST(self):

        if self.path != "/chat":

            self.send_response(404)

            self.end_headers()

            return


        try:

            length =
                int(
                    self.headers.get(
                        "Content-Length",
                        0
                    )
                )


            body =
                self.rfile.read(
                    length
                )


            data =
                json.loads(
                    body.decode("utf-8")
                )


            user_message =
                data.get(
                    "message",
                    ""
                ).strip()


            if not user_message:

                self.send_json(
                    {
                        "error":
                        "Mesaj boş."
                    },
                    400
                )

                return


            # Kullanıcı oturumunu bul
            session_id = None

            if "Cookie" in self.headers:

                cookie =
                    cookies.SimpleCookie(
                        self.headers["Cookie"]
                    )

                if "ALPAGUT_SESSION" in cookie:

                    session_id =
                        cookie[
                            "ALPAGUT_SESSION"
                        ].value


            if not session_id:

                session_id =
                    str(uuid.uuid4())


            if session_id not in sessions:

                sessions[session_id] = {
                    "response_id": None
                }


            previous_response =
                sessions[
                    session_id
                ]["response_id"]


            # OpenAI isteği

            request_data = {

                "model":
                    "gpt-4o-mini",

                "instructions":
                    """
Sen Alpağut Yapay Zeka'sın.

Türkçe konuş.

Samimi, doğal,
yardımsever ve anlaşılır ol.

Kullanıcıyla normal bir insanla
konuşuyormuş gibi iletişim kur.

Kullanıcının önceki mesajlarını
dikkate al.

Gereksiz yere uzun cevap verme.

Bilmediğin bir şeyi kesinmiş
gibi söyleme.
"""
            }


            if previous_response:

                request_data[
                    "previous_response_id"
                ] = previous_response


            request_data[
                "input"
            ] = user_message


            response =
                client.responses.create(
                    **request_data
                )


            reply =
                response.output_text


            # Son cevabı hafızada tut
            sessions[
                session_id
            ]["response_id"] =
                response.id


            result =
                json.dumps(
                    {
                        "reply":
                            reply
                    },
                    ensure_ascii=False
                ).encode("utf-8")


            self.send_response(200)


            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8"
            )


            self.send_header(
                "Content-Length",
                str(len(result))
            )


            self.send_header(
                "Set-Cookie",
                f"ALPAGUT_SESSION={session_id}; "
                "Path=/; HttpOnly; SameSite=Lax"
            )


            self.end_headers()


            self.wfile.write(
                result
            )


        except Exception as e:

            self.send_json(
                {
                    "error":
                        str(e)
                },
                500
            )


print("")
print("==============================")
print("   ALPAGUT YAPAY ZEKA V3")
print("==============================")
print("")


PORT =
    int(
        os.environ.get(
            "PORT",
            5000
        )
    )


print(
    f"Port: {PORT}"
)


server =
    HTTPServer(
        ("0.0.0.0", PORT),
        Handler
    )


server.serve_forever()
