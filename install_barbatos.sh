#!/bin/bash

# Get current user and target directory
USER_HOME=$(eval echo "~$USER")
TARGET_DIR="$USER_HOME/barbatos_rgb_twinkle"
REPO_URL="https://github.com/azkikr316/MG-Barbatos-LED.git"
VENV_DIR="$TARGET_DIR/ledvenv"

echo "📦 Installing MG Barbatos LED control to: $TARGET_DIR"

# Step 1: Install dependencies
echo "🔧 Installing system packages..."
sudo apt update && sudo apt install -y \
  python3-pip python3-venv python3-lgpio \
  git i2c-tools build-essential libffi-dev

# Step 2: Clone repository
if [ -d "$TARGET_DIR" ]; then
  echo "🔁 Repository already exists. Pulling latest updates..."
  cd "$TARGET_DIR" && git pull
else
  echo "⬇️ Cloning repository..."
  git clone "$REPO_URL" "$TARGET_DIR"
fi

# Step 3: Setup virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Step 4: Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install \
  adafruit-circuitpython-pca9685 \
  adafruit-blinka \
  quart

# Step 5: Check I2C connection
echo "🔍 Verifying I2C device (PCA9685)..."
i2cdetect -y 1

# Step 6 (optional): Create systemd service (uncomment to enable)
# SERVICE_NAME="barbatos_led"
# SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
# echo "🛠 Setting up systemd service..."
# sudo bash -c "cat > $SERVICE_FILE" <<EOF
# [Unit]
# Description=Barbatos LED Controller
# After=network.target

# [Service]
# WorkingDirectory=$TARGET_DIR
# ExecStart=$VENV_DIR/bin/python web_led.py
# Restart=always
# User=$USER
# Environment=PYTHONUNBUFFERED=1

# [Install]
# WantedBy=multi-user.target
# EOF

# sudo systemctl daemon-reexec
# sudo systemctl daemon-reload
# sudo systemctl enable $SERVICE_NAME
# sudo systemctl start $SERVICE_NAME

echo "✅ Installation complete!"
echo "👉 To start manually:"
echo "   cd $TARGET_DIR"
echo "   source ledvenv/bin/activate"
echo "   python web_led.py"
