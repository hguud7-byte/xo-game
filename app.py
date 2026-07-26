from flask import Flask, render_template_string
import os

app = Flask(__name__)

# كود واجهة اللعبة (HTML + CSS + JavaScript)
HTML_CODE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لعبة XO</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            background-color: #0f172a;
            color: #fff;
        }
        h1 { margin-bottom: 10px; font-size: 2.5rem; color: #38bdf8; }
        .status { font-size: 1.3rem; margin-bottom: 20px; color: #f8fafc; }
        .board {
            display: grid;
            grid-template-columns: repeat(3, 100px);
            grid-template-rows: repeat(3, 100px);
            gap: 10px;
        }
        .cell {
            width: 100px;
            height: 100px;
            background-color: #1e293b;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
        }
        .cell:hover { background-color: #334155; transform: scale(1.02); }
        .cell.x { color: #f43f5e; }
        .cell.o { color: #38bdf8; }
        button {
            margin-top: 25px;
            padding: 10px 24px;
            font-size: 1rem;
            font-weight: bold;
            background-color: #38bdf8;
            color: #0f172a;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background-color: #0284c7; color: #fff; }
    </style>
</head>
<body>

    <h1>🎮 لعبة XO</h1>
    <div class="status" id="status">دور اللاعب: <span style="color: #f43f5e;">X</span></div>
    
    <div class="board" id="board">
        <div class="cell" onclick="makeMove(this, 0)"></div>
        <div class="cell" onclick="makeMove(this, 1)"></div>
        <div class="cell" onclick="makeMove(this, 2)"></div>
        <div class="cell" onclick="makeMove(this, 3)"></div>
        <div class="cell" onclick="makeMove(this, 4)"></div>
        <div class="cell" onclick="makeMove(this, 5)"></div>
        <div class="cell" onclick="makeMove(this, 6)"></div>
        <div class="cell" onclick="makeMove(this, 7)"></div>
        <div class="cell" onclick="makeMove(this, 8)"></div>
    </div>

    <button onclick="resetGame()">إعادة اللعب 🔄</button>

    <script>
        let currentPlayer = 'X';
        let gameState = ["", "", "", "", "", "", "", "", ""];
        let gameActive = true;

        const winningConditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ];

        function makeMove(cell, index) {
            if (gameState[index] !== "" || !gameActive) return;

            gameState[index] = currentPlayer;
            cell.innerText = currentPlayer;
            cell.classList.add(currentPlayer.toLowerCase());

            checkResult();
        }

        function checkResult() {
            let roundWon = false;
            for (let condition of winningConditions) {
                let [a, b, c] = condition;
                if (gameState[a] && gameState[a] === gameState[b] && gameState[a] === gameState[c]) {
                    roundWon = true;
                    break;
                }
            }

            if (roundWon) {
                document.getElementById('status').innerHTML = `🎉 الفائز هو اللاعب: <b style="color:${currentPlayer === 'X' ? '#f43f5e' : '#38bdf8'}">${currentPlayer}</b>`;
                gameActive = false;
                return;
            }

            if (!gameState.includes("")) {
                document.getElementById('status').innerText = '🤝 تعادل!';
                gameActive = false;
                return;
            }

            currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
            document.getElementById('status').innerHTML = `دور اللاعب: <b style="color:${currentPlayer === 'X' ? '#f43f5e' : '#38bdf8'}">${currentPlayer}</b>`;
        }

        function resetGame() {
            currentPlayer = 'X';
            gameState = ["", "", "", "", "", "", "", "", ""];
            gameActive = true;
            document.getElementById('status').innerHTML = `دور اللاعب: <b style="color:#f43f5e">X</b>`;
            document.querySelectorAll('.cell').forEach(cell => {
                cell.innerText = '';
                cell.classList.remove('x', 'o');
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
