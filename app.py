from flask import Flask, render_template_string
import os

app = Flask(__name__)

# كود واجهة اللعبة كامل مع خيار اللعب ضد الروبوت
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
            min-height: 100vh;
            margin: 0;
            background-color: #0f172a;
            color: #fff;
        }
        h1 { margin-bottom: 10px; font-size: 2.2rem; color: #38bdf8; }
        .mode-selector {
            margin-bottom: 15px;
            display: flex;
            gap: 10px;
        }
        .mode-btn {
            padding: 8px 16px;
            font-size: 0.9rem;
            background-color: #1e293b;
            color: #94a3b8;
            border: 2px solid #334155;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .mode-btn.active {
            background-color: #38bdf8;
            color: #0f172a;
            border-color: #38bdf8;
            font-weight: bold;
        }
        .status { font-size: 1.2rem; margin-bottom: 20px; color: #f8fafc; }
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
        .reset-btn {
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
        .reset-btn:hover { background-color: #0284c7; color: #fff; }
    </style>
</head>
<body>

    <h1>🎮 لعبة XO</h1>

    <div class="mode-selector">
        <button class="mode-btn active" id="btn-bot" onclick="setMode('bot')">ضد الروبوت 🤖</button>
        <button class="mode-btn" id="btn-pvp" onclick="setMode('pvp')">لاعب ضد لاعب 👥</button>
    </div>

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

    <button class="reset-btn" onclick="resetGame()">إعادة اللعب 🔄</button>

    <script>
        let currentPlayer = 'X';
        let gameState = ["", "", "", "", "", "", "", "", ""];
        let gameActive = true;
        let vsBot = true;

        const winningConditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ];

        function setMode(mode) {
            vsBot = (mode === 'bot');
            document.getElementById('btn-bot').classList.toggle('active', vsBot);
            document.getElementById('btn-pvp').classList.toggle('active', !vsBot);
            resetGame();
        }

        function makeMove(cell, index) {
            if (gameState[index] !== "" || !gameActive) return;

            gameState[index] = currentPlayer;
            cell.innerText = currentPlayer;
            cell.classList.add(currentPlayer.toLowerCase());

            if (checkResult()) return;

            currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
            
            if (vsBot && currentPlayer === 'O' && gameActive) {
                document.getElementById('status').innerHTML = `🤖 الروبوت يفكر...`;
                setTimeout(botMove, 500);
            } else {
                document.getElementById('status').innerHTML = `دور اللاعب: <b style="color:${currentPlayer === 'X' ? '#f43f5e' : '#38bdf8'}">${currentPlayer}</b>`;
            }
        }

        function botMove() {
            if (!gameActive) return;

            // ذكاء اصطناعي بسيط: البحث عن الفوز أولاً، ثم منع الخصم، أو الاختيار العشوائي
            let emptyIndexes = gameState.map((val, idx) => val === "" ? idx : null).filter(val => val !== null);
            
            if (emptyIndexes.length === 0) return;

            let chosenIndex = findBestMove('O') ?? findBestMove('X') ?? emptyIndexes[Math.floor(Math.random() * emptyIndexes.length)];

            const cells = document.querySelectorAll('.cell');
            gameState[chosenIndex] = 'O';
            cells[chosenIndex].innerText = 'O';
            cells[chosenIndex].classList.add('o');

            if (checkResult()) return;

            currentPlayer = 'X';
            document.getElementById('status').innerHTML = `دور اللاعب: <b style="color:#f43f5e">X</b>`;
        }

        function findBestMove(player) {
            for (let condition of winningConditions) {
                let [a, b, c] = condition;
                let values = [gameState[a], gameState[b], gameState[c]];
                let playerCounts = values.filter(v => v === player).length;
                let emptyCounts = values.filter(v => v === "").length;

                if (playerCounts === 2 && emptyCounts === 1) {
                    if (gameState[a] === "") return a;
                    if (gameState[b] === "") return b;
                    if (gameState[c] === "") return c;
                }
            }
            return null;
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
                let winnerName = vsBot && currentPlayer === 'O' ? '🤖 الروبوت' : `اللاعب ${currentPlayer}`;
                document.getElementById('status').innerHTML = `🎉 الفائز هو: <b style="color:${currentPlayer === 'X' ? '#f43f5e' : '#38bdf8'}">${winnerName}</b>`;
                gameActive = false;
                return true;
            }

            if (!gameState.includes("")) {
                document.getElementById('status').innerText = '🤝 تعادل!';
                gameActive = false;
                return true;
            }

            return false;
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
