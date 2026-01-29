import os
from flask import Flask, request, redirect
import redis

app = Flask(__name__)

redis_host = os.environ.get('REDIS_HOST', 'redis')
db = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            wpis = request.form.get('wpis')
            if wpis:
                db.lpush('guestbook', wpis)
                return redirect('/')

        wpisy = db.lrange('guestbook', 0, 19)
    except Exception as e:
        return f"Błąd polaczenia z bazą danych: {str(e)}"

    wpisy_html = ''.join(f'<div class="entry">{w}</div>' for w in wpisy)
    
    html = f'''
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Księga Gości - DevOps</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f0f2f5;
                display: flex;
                justify-content: center;
                padding-top: 50px;
                margin: 0;
            }}
            .container {{
                background-color: white;
                width: 100%;
                max-width: 500px;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            h1 {{
                text-align: center;
                color: #333;
                margin-top: 0;
            }}
            form {{
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
                border-bottom: 2px solid #f0f2f5;
                padding-bottom: 20px;
            }}
            input {{
                flex-grow: 1;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                outline: none;
            }}
            input:focus {{
                border-color: #007bff;
            }}
            button {{
                padding: 12px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
                transition: background 0.2s;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
            .entry {{
                background-color: #f8f9fa;
                padding: 15px;
                margin-bottom: 10px;
                border-radius: 8px;
                border-left: 4px solid #007bff;
                color: #555;
            }}
            .empty {{
                text-align: center;
                color: #aaa;
                font-style: italic;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Księga Gości</h1>
            
            <form method="POST">
                <input type="text" name="wpis" placeholder="Wpisz swoje imię..." required autocomplete="off">
                <button type="submit">Dodaj</button>
            </form>

            <div class="list">
                {wpisy_html if wpisy else '<p class="empty">Brak wpisów. Badź pierwszy!</p>'}
            </div>
        </div>
    </body>
    </html>
    '''
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
