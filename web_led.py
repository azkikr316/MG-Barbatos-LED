from quart import Quart, render_template_string, request
import asyncio
from led_modes_async import (
    run_mode, mode_startup, mode_static, mode_breathe, mode_flicker
)

app = Quart(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>MG Barbatos LED Control</title>
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 40px; }
        button { margin: 10px; padding: 12px 24px; font-size: 16px; border: none; border-radius: 8px; }
        .startup { background-color: #9b59b6; }
        .mode1 { background-color: #2980b9; }
        .mode2 { background-color: #27ae60; }
        .mode3 { background-color: #e67e22; }
    </style>
</head>
<body>
    <h1>MG Barbatos LED Control</h1>
    <form method="post">
        <button name="mode" value="startup" class="startup">Startup Mode</button>
        <button name="mode" value="1" class="mode1">Mode 1 - Static Glow</button>
        <button name="mode" value="2" class="mode2">Mode 2 - Breathing</button>
        <button name="mode" value="3" class="mode3">Mode 3 - Flicker</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
async def control():
    if request.method == "POST":
        form = await request.form
        mode = form.get("mode")
        if mode == "startup":
            await run_mode(mode_startup)
        elif mode == "1":
            await run_mode(mode_static)
        elif mode == "2":
            await run_mode(mode_breathe)
        elif mode == "3":
            await run_mode(mode_flicker)
    return await render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
