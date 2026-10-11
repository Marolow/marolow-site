from flask import Flask, render_template_string, url_for

app = Flask(__name__)

# ===== ГЛАВНАЯ СТРАНИЦА =====
HTML_MAIN = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MAROLOW</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', Arial, sans-serif;
            color: #fff;
            overflow-x: hidden;
            background: #000;
            min-height: 100vh;
        }
        #bg-video {
            position: fixed;
            top: 50%; left: 50%;
            min-width: 100%; min-height: 100%;
            transform: translate(-50%, -50%);
            z-index: -2;
            object-fit: cover;
            filter: grayscale(100%) brightness(0.55) contrast(1.2);
        }
        .overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: radial-gradient(ellipse at center, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.7) 60%, rgba(0,0,0,0.95) 100%);
            z-index: -1;
        }
        .content {
            position: relative;
            max-width: 1000px;
            margin: 0 auto;
            padding: 100px 20px 200px;
            text-align: center;
            z-index: 1;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            animation: fadeIn 1.8s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 {
            font-size: 140px;
            font-weight: 900;
            letter-spacing: 2px;
            color: #fff;
            margin-bottom: 60px;
            line-height: 1;
            text-shadow: 
                1px 1px 0 #d0d0d0, 2px 2px 0 #c0c0c0, 3px 3px 0 #b0b0b0,
                4px 4px 0 #a0a0a0, 5px 5px 0 #909090, 6px 6px 0 #808080,
                7px 7px 0 #707070, 8px 8px 0 #606060, 10px 10px 30px rgba(0,0,0,0.9);
            animation: pulse 4s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.03); }
        }
        .features {
            display: flex;
            justify-content: center;
            gap: 25px;
            flex-wrap: wrap;
        }
        .feature {
            background: rgba(255,255,255,0.06);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 20px;
            padding: 35px 40px;
            min-width: 220px;
            transition: 0.4s;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
            text-decoration: none;
            color: #fff;
            display: block;
        }
        .feature:hover {
            transform: translateY(-8px);
            background: rgba(255,255,255,0.1);
            border-color: rgba(255,255,255,0.35);
        }
        .feature h3 {
            font-size: 20px;
            font-weight: 800;
            color: #fff;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }
        .feature p { font-size: 14px; color: #b0b0b0; }
        .feature.support { border-color: rgba(33, 168, 56, 0.4); }
        .feature.support:hover {
            border-color: #21a838;
            box-shadow: 0 15px 50px rgba(33, 168, 56, 0.4);
        }
        .feature.support h3 { color: #21a838; }
        footer {
            position: fixed;
            bottom: 100px; left: 0;
            width: 100%;
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
            letter-spacing: 3px;
            text-transform: uppercase;
            z-index: 1;
        }
        .lang-switch {
            position: fixed;
            bottom: 110px; right: 20px;
            display: flex;
            gap: 5px;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 50px;
            padding: 5px;
            z-index: 100;
        }
        .lang-switch button {
            background: transparent;
            border: none;
            color: #888;
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1px;
            padding: 8px 16px;
            border-radius: 50px;
            cursor: pointer;
            transition: 0.3s;
        }
        .lang-switch button.active { background: #fff; color: #000; }
        .lang-switch button:hover:not(.active) { color: #fff; }

        .music-player {
            position: fixed;
            bottom: 15px; left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 700px;
            background: rgba(255,255,255,0.07);
            backdrop-filter: blur(25px);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 60px;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 10px 50px rgba(0,0,0,0.7);
            z-index: 200;
        }
        .play-btn {
            width: 48px; height: 48px;
            border-radius: 50%;
            background: #fff;
            color: #000;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            transition: 0.3s;
            box-shadow: 0 5px 20px rgba(255,255,255,0.3);
        }
        .play-btn:hover { transform: scale(1.08); }
        .play-btn svg { width: 18px; height: 18px; fill: #000; }
        .track-info { flex: 1; min-width: 0; text-align: left; }
        .track-name {
            font-size: 14px;
            font-weight: 700;
            color: #fff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .track-artist { font-size: 11px; color: #888; margin-top: 2px; }
        .progress-container {
            flex: 2;
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 0;
        }
        .time { font-size: 11px; color: #888; font-weight: 600; flex-shrink: 0; }
        .progress-bar {
            flex: 1;
            height: 4px;
            background: rgba(255,255,255,0.15);
            border-radius: 2px;
            cursor: pointer;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: #fff;
            width: 0%;
            border-radius: 2px;
            transition: width 0.1s linear;
        }
        .volume-container { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
        .volume-icon { width: 18px; height: 18px; fill: #888; cursor: pointer; transition: 0.3s; }
        .volume-icon:hover { fill: #fff; }
        .volume-bar {
            width: 60px; height: 3px;
            background: rgba(255,255,255,0.15);
            border-radius: 2px;
            cursor: pointer;
        }
        .volume-fill { height: 100%; background: #fff; width: 70%; border-radius: 2px; }

        @media (max-width: 768px) {
            h1 { font-size: 64px; margin-bottom: 40px; }
            .feature { min-width: 160px; padding: 25px 25px; }
            .lang-switch { bottom: 110px; right: 15px; }
            footer { bottom: 100px; }
            .music-player { width: 95%; padding: 10px 15px; gap: 10px; }
            .play-btn { width: 40px; height: 40px; }
            .progress-container { display: none; }
            .volume-container { display: none; }
        }
    </style>
</head>
<body>
    <video autoplay muted loop playsinline id="bg-video">
        <source src="{{ url_for('static', filename='smoke.mp4') }}" type="video/mp4">
    </video>
    <div class="overlay"></div>

    <main class="content">
        <h1>MAROLOW</h1>

        <div class="features">
            <a href="/about" class="feature">
                <h3 data-ru="О НАС" data-en="ABOUT US">О НАС</h3>
                <p data-ru="Узнать больше" data-en="Learn more">Узнать больше</p>
            </a>

            <a href="https://t.me/+q-_VuEu1C-o4MmEy" class="feature" target="_blank">
                <h3 data-ru="ТГ КАНАЛ" data-en="TG CHANNEL">ТГ КАНАЛ</h3>
                <p data-ru="Перейти в канал" data-en="Open channel">Перейти в канал</p>
            </a>

            <a href="/support" class="feature support">
                <h3 data-ru="ПОДДЕРЖКА" data-en="SUPPORT">ПОДДЕРЖКА</h3>
                <p data-ru="Помочь проекту" data-en="Support the project">Помочь проекту</p>
            </a>
        </div>
    </main>

    <footer><p>© MAROLOW 2026</p></footer>

    <div class="lang-switch">
        <button id="btn-ru" class="active" onclick="setLang('ru')">RU</button>
        <button id="btn-en" onclick="setLang('en')">EN</button>
    </div>

    <audio id="audio" loop>
        <source src="{{ url_for('static', filename='music.mp3') }}" type="audio/mpeg">
    </audio>

    <div class="music-player">
        <button class="play-btn" onclick="togglePlay()" id="playBtn">
            <svg id="playIcon" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
            </svg>
        </button>

        <div class="track-info">
            <div class="track-name">madk1d, VILLIAN — ДИНАСТИЯ</div>
            <div class="track-artist">MAROLOW</div>
        </div>

        <div class="progress-container">
            <span class="time" id="currentTime">0:00</span>
            <div class="progress-bar" onclick="seek(event)">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <span class="time" id="duration">0:00</span>
        </div>

        <div class="volume-container">
            <svg class="volume-icon" id="volumeIcon" viewBox="0 0 24 24" onclick="toggleMute()">
                <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/>
            </svg>
            <div class="volume-bar" onclick="setVolume(event)">
                <div class="volume-fill" id="volumeFill"></div>
            </div>
        </div>
    </div>

    <script>
        const audio = document.getElementById('audio');
        const playIcon = document.getElementById('playIcon');
        const progressFill = document.getElementById('progressFill');
        const currentTimeEl = document.getElementById('currentTime');
        const durationEl = document.getElementById('duration');
        const volumeFill = document.getElementById('volumeFill');
        let isPlaying = false;
        let isMuted = false;

        function formatTime(s) {
            if (isNaN(s)) return '0:00';
            const m = Math.floor(s / 60);
            const sec = Math.floor(s % 60);
            return m + ':' + (sec < 10 ? '0' : '') + sec;
        }
        function togglePlay() {
            if (isPlaying) {
                audio.pause();
                playIcon.innerHTML = '<path d="M8 5v14l11-7z"/>';
            } else {
                audio.play();
                playIcon.innerHTML = '<path d="M6 4h4v16H6zm8 0h4v16h-4z"/>';
            }
            isPlaying = !isPlaying;
        }
        audio.addEventListener('timeupdate', () => {
            if (audio.duration) {
                progressFill.style.width = (audio.currentTime / audio.duration) * 100 + '%';
                currentTimeEl.textContent = formatTime(audio.currentTime);
            }
        });
        audio.addEventListener('loadedmetadata', () => {
            durationEl.textContent = formatTime(audio.duration);
        });
        function seek(e) {
            const percent = e.offsetX / e.currentTarget.offsetWidth;
            audio.currentTime = percent * audio.duration;
        }
        function setVolume(e) {
            const percent = Math.max(0, Math.min(1, e.offsetX / e.currentTarget.offsetWidth));
            audio.volume = percent;
            volumeFill.style.width = (percent * 100) + '%';
            isMuted = false;
        }
        function toggleMute() {
            isMuted = !isMuted;
            audio.muted = isMuted;
        }
        document.addEventListener('click', function start() {
            if (!isPlaying) {
                audio.play().then(() => {
                    isPlaying = true;
                    playIcon.innerHTML = '<path d="M6 4h4v16H6zm8 0h4v16h-4z"/>';
                }).catch(() => {});
            }
            document.removeEventListener('click', start);
        }, { once: true });

        function setLang(lang) {
            localStorage.setItem('lang', lang);
            document.querySelectorAll('[data-ru]').forEach(el => {
                el.textContent = el.getAttribute('data-' + lang);
            });
            document.getElementById('btn-ru').classList.toggle('active', lang === 'ru');
            document.getElementById('btn-en').classList.toggle('active', lang === 'en');
        }
        window.addEventListener('DOMContentLoaded', () => {
            setLang(localStorage.getItem('lang') || 'ru');
        });
    </script>
</body>
</html>
"""

# ===== СТРАНИЦА "О НАС" =====
HTML_ABOUT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>О НАС — MAROLOW</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', Arial, sans-serif;
            color: #fff; background: #000; min-height: 100vh; overflow-y: auto;
        }
        #bg-video {
            position: fixed;
            top: 50%; left: 50%;
            min-width: 100%; min-height: 100%;
            transform: translate(-50%, -50%);
            z-index: -2;
            object-fit: cover;
            filter: grayscale(100%) brightness(0.45) contrast(1.2);
        }
        .overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: radial-gradient(ellipse at center, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.8) 60%, rgba(0,0,0,0.95) 100%);
            z-index: -1;
        }
        .content {
            position: relative;
            max-width: 800px;
            margin: 0 auto;
            padding: 80px 30px 140px;
            z-index: 1;
        }
        h1 {
            font-size: 72px;
            font-weight: 900;
            letter-spacing: 4px;
            color: #fff;
            margin-bottom: 40px;
            text-align: center;
            text-shadow: 0 0 40px rgba(255,255,255,0.3);
        }
        .about-box {
            background: rgba(255,255,255,0.06);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 24px;
            padding: 50px 45px;
            box-shadow: 0 10px 50px rgba(0,0,0,0.6);
            line-height: 1.9;
            font-size: 16px;
            color: #d0d0d0;
        }
        .about-box p { margin-bottom: 25px; }
        .about-box p:last-child { margin-bottom: 0; }
        .about-box .emoji { filter: grayscale(100%); }
        .about-box a { color: #fff; text-decoration: underline; text-underline-offset: 4px; }
        .about-box a:hover { color: #a0a0a0; }
        .about-box .label { color: #fff; font-weight: 700; }
        .back-btn {
            display: inline-block;
            margin-top: 40px;
            padding: 16px 40px;
            text-decoration: none;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            background: transparent;
            color: #fff;
            border: 2px solid rgba(255,255,255,0.6);
            transition: 0.3s;
        }
        .back-btn:hover { background: #fff; color: #000; }
        footer {
            position: fixed;
            bottom: 0; left: 0;
            width: 100%;
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
        .lang-switch {
            position: fixed;
            bottom: 20px; right: 20px;
            display: flex; gap: 5px;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 50px;
            padding: 5px;
            z-index: 100;
        }
        .lang-switch button {
            background: transparent;
            border: none;
            color: #888;
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1px;
            padding: 8px 16px;
            border-radius: 50px;
            cursor: pointer;
            transition: 0.3s;
        }
        .lang-switch button.active { background: #fff; color: #000; }
        @media (max-width: 768px) {
            h1 { font-size: 44px; }
            .about-box { padding: 30px 25px; font-size: 15px; }
            .lang-switch { bottom: 70px; right: 15px; }
        }
    </style>
</head>
<body>
    <video autoplay muted loop playsinline id="bg-video">
        <source src="{{ url_for('static', filename='smoke.mp4') }}" type="video/mp4">
    </video>
    <div class="overlay"></div>

    <main class="content">
        <h1 data-ru="О НАС" data-en="ABOUT US">О НАС</h1>

        <div class="about-box" id="about-content">
            <div data-lang="ru">
                <p>Приветствую всех! Этот ТГ-канал создан с целью, чтобы покупатели моего бота следили за новыми обновлениями и фичами <span class="emoji">🛫</span></p>
                <p>Итак, представляю свой проект — бот для пр0бiва дон0сов и т.д. Всё, что вам нужно, есть в этом боте <span class="emoji">🚫</span></p>
                <p><span class="label">Обновления</span> <span class="emoji">❗️</span><br>Они будут достаточно частыми в связи с началом разработки бота.</p>
                <p><span class="label">Мои цели</span> <span class="emoji">✏️</span><br>Создать идеальный бот для точного поиска информации и 100-процентной вероятности успеха.</p>
                <p>С самим ботом можете ознакомиться тут:<br><a href="https://t.me/+q-_VuEu1C-o4MmEy" target="_blank">Link <span class="emoji">☑️</span></a></p>
            </div>
            <div data-lang="en" style="display:none;">
                <p>Greetings everyone! This TG channel was created so that buyers of my bot could follow new updates and features <span class="emoji">🛫</span></p>
                <p>So, I present my project — a bot for probing donuts, etc. Everything you need is in this bot <span class="emoji">🚫</span></p>
                <p><span class="label">Updates</span> <span class="emoji">❗️</span><br>They will be quite frequent due to the start of bot development.</p>
                <p><span class="label">My goals</span> <span class="emoji">✏️</span><br>To create the perfect bot for accurate information search and 100% success rate.</p>
                <p>You can check out the bot itself here:<br><a href="https://t.me/+q-_VuEu1C-o4MmEy" target="_blank">Link <span class="emoji">☑️</span></a></p>
            </div>
        </div>

        <div style="text-align:center;">
            <a href="/" class="back-btn" data-ru="← Назад" data-en="← Back">← Назад</a>
        </div>
    </main>

    <footer><p>© MAROLOW 2026</p></footer>

    <div class="lang-switch">
        <button id="btn-ru" class="active" onclick="setLang('ru')">RU</button>
        <button id="btn-en" onclick="setLang('en')">EN</button>
    </div>

    <script>
        function setLang(lang) {
            localStorage.setItem('lang', lang);
            document.querySelectorAll('[data-ru]').forEach(el => {
                el.textContent = el.getAttribute('data-' + lang);
            });
            document.querySelectorAll('#about-content [data-lang]').forEach(el => {
                el.style.display = (el.getAttribute('data-lang') === lang) ? 'block' : 'none';
            });
            document.getElementById('btn-ru').classList.toggle('active', lang === 'ru');
            document.getElementById('btn-en').classList.toggle('active', lang === 'en');
        }
        window.addEventListener('DOMContentLoaded', () => {
            setLang(localStorage.getItem('lang') || 'ru');
        });
    </script>
</body>
</html>
"""

# ===== СТРАНИЦА "ПОДДЕРЖКА" =====
HTML_SUPPORT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Поддержка — MAROLOW</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', Arial, sans-serif; color: #fff; background: #000; min-height: 100vh; }
        #bg-video {
            position: fixed;
            top: 50%; left: 50%;
            min-width: 100%; min-height: 100%;
            transform: translate(-50%, -50%);
            z-index: -2;
            object-fit: cover;
            filter: grayscale(100%) brightness(0.4) contrast(1.2);
        }
        .overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: radial-gradient(ellipse at center, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.85) 60%, rgba(0,0,0,0.98) 100%);
            z-index: -1;
        }
        .content {
            position: relative;
            max-width: 700px;
            margin: 0 auto;
            padding: 80px 30px 140px;
            z-index: 1;
        }
        h1 {
            font-size: 72px;
            font-weight: 900;
            letter-spacing: 4px;
            color: #fff;
            margin-bottom: 20px;
            text-align: center;
            text-shadow: 0 0 40px rgba(255,255,255,0.3);
        }
        .subtitle {
            text-align: center;
            color: #888;
            font-size: 16px;
            letter-spacing: 2px;
            margin-bottom: 50px;
        }
        .sber-card {
            position: relative;
            background: linear-gradient(135deg, #21a838 0%, #0e7a25 100%);
            border-radius: 24px;
            padding: 35px 40px;
            box-shadow: 0 20px 60px rgba(33, 168, 56, 0.4), 0 0 100px rgba(33, 168, 56, 0.2);
            overflow: hidden;
            margin-bottom: 30px;
        }
        .sber-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
        }
        .sber-logo { display: flex; align-items: center; gap: 10px; }
        .sber-logo svg { width: 40px; height: 40px; }
        .sber-logo-text { font-size: 22px; font-weight: 800; color: #fff; }
        .chip {
            width: 50px; height: 38px;
            background: linear-gradient(135deg, #ffd700 0%, #daa520 100%);
            border-radius: 8px;
        }
        .card-number-label {
            font-size: 12px;
            letter-spacing: 3px;
            color: rgba(255,255,255,0.7);
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .card-number {
            font-size: 32px;
            font-weight: 800;
            letter-spacing: 4px;
            color: #fff;
            margin-bottom: 30px;
            font-family: 'Courier New', monospace;
        }
        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .card-holder { font-size: 14px; letter-spacing: 2px; color: rgba(255,255,255,0.9); text-transform: uppercase; }
        .card-holder-label { font-size: 10px; letter-spacing: 2px; color: rgba(255,255,255,0.6); margin-bottom: 4px; }
        .card-brand-name { font-size: 22px; font-weight: 900; color: #fff; }
        .copy-btn {
            display: block;
            width: 100%;
            padding: 20px;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 16px;
            color: #fff;
            font-family: 'Inter', sans-serif;
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            cursor: pointer;
            transition: 0.3s;
        }
        .copy-btn:hover { background: #21a838; border-color: #21a838; }
        .copy-btn.copied { background: #21a838; }
        .info-text {
            text-align: center;
            color: #888;
            font-size: 14px;
            line-height: 1.7;
            margin: 30px 0 40px;
        }
        .back-btn {
            display: inline-block;
            padding: 16px 40px;
            text-decoration: none;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            background: transparent;
            color: #fff;
            border: 2px solid rgba(255,255,255,0.6);
            transition: 0.3s;
        }
        .back-btn:hover { background: #fff; color: #000; }
        footer {
            position: fixed;
            bottom: 0; left: 0;
            width: 100%;
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
        .lang-switch {
            position: fixed;
            bottom: 20px; right: 20px;
            display: flex; gap: 5px;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 50px;
            padding: 5px;
            z-index: 100;
        }
        .lang-switch button {
            background: transparent;
            border: none;
            color: #888;
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            font-weight: 700;
            padding: 8px 16px;
            border-radius: 50px;
            cursor: pointer;
            transition: 0.3s;
        }
        .lang-switch button.active { background: #fff; color: #000; }
        @media (max-width: 768px) {
            h1 { font-size: 44px; }
            .sber-card { padding: 25px 25px; }
            .card-number { font-size: 22px; letter-spacing: 2px; }
            .lang-switch { bottom: 70px; right: 15px; }
        }
    </style>
</head>
<body>
    <video autoplay muted loop playsinline id="bg-video">
        <source src="{{ url_for('static', filename='smoke.mp4') }}" type="video/mp4">
    </video>
    <div class="overlay"></div>

    <main class="content">
        <h1 data-ru="ПОДДЕРЖКА" data-en="SUPPORT">ПОДДЕРЖКА</h1>
        <p class="subtitle" data-ru="Если хочешь помочь проекту — буду благодарен" data-en="If you want to support the project — I'd be grateful">Если хочешь помочь проекту — буду благодарен</p>

        <div class="sber-card">
            <div class="sber-header">
                <div class="sber-logo">
                    <svg viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="white" stroke-width="6"/>
                        <path d="M 30 50 L 45 65 L 72 35" fill="none" stroke="white" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <span class="sber-logo-text">СБЕР</span>
                </div>
                <div class="chip"></div>
            </div>

            <div class="card-number-label" data-ru="НОМЕР КАРТЫ" data-en="CARD NUMBER">НОМЕР КАРТЫ</div>
            <div class="card-number">2202 2050 5038 3865</div>

            <div class="card-footer">
                <div>
                    <div class="card-holder-label" data-ru="ВЛАДЕЛЕЦ" data-en="CARD HOLDER">ВЛАДЕЛЕЦ</div>
                    <div class="card-holder">MAROLOW</div>
                </div>
                <div class="card-brand-name">МИР</div>
            </div>
        </div>

        <button class="copy-btn" onclick="copyCard()" id="copy-btn">
            <span data-ru="СКОПИРОВАТЬ НОМЕР" data-en="COPY NUMBER">СКОПИРОВАТЬ НОМЕР</span>
        </button>

        <p class="info-text" data-ru="Спасибо за любую поддержку! Каждая копейка идёт на развитие проекта 🚀" data-en="Thanks for any support! Every penny goes to project development 🚀">Спасибо за любую поддержку! Каждая копейка идёт на развитие проекта 🚀</p>

        <div style="text-align:center;">
            <a href="/" class="back-btn" data-ru="← Назад" data-en="← Back">← Назад</a>
        </div>
    </main>

    <footer><p>© MAROLOW 2026</p></footer>

    <div class="lang-switch">
        <button id="btn-ru" class="active" onclick="setLang('ru')">RU</button>
        <button id="btn-en" onclick="setLang('en')">EN</button>
    </div>

    <script>
        function copyCard() {
            navigator.clipboard.writeText('2202205050383865').then(() => {
                const btn = document.getElementById('copy-btn');
                const span = btn.querySelector('span');
                const original = span.textContent;
                btn.classList.add('copied');
                span.textContent = '✓ СКОПИРОВАНО';
                setTimeout(() => {
                    btn.classList.remove('copied');
                    span.textContent = original;
                }, 2000);
            });
        }
        function setLang(lang) {
            localStorage.setItem('lang', lang);
            document.querySelectorAll('[data-ru]').forEach(el => {
                if (el.tagName === 'SPAN' && el.parentElement.id === 'copy-btn') return;
                el.textContent = el.getAttribute('data-' + lang);
            });
            document.getElementById('btn-ru').classList.toggle('active', lang === 'ru');
            document.getElementById('btn-en').classList.toggle('active', lang === 'en');
        }
        window.addEventListener('DOMContentLoaded', () => {
            setLang(localStorage.getItem('lang') || 'ru');
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_MAIN)

@app.route("/about")
def about():
    return render_template_string(HTML_ABOUT)

@app.route("/support")
def support():
    return render_template_string(HTML_SUPPORT)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)
