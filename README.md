# MG Barbatos LED Control

This project replicates the effects of Kosmos LEDs for the MG Barbatos model using a Raspberry Pi Zero 2 W and a PCA9685 16-channel PWM controller. It includes a Quart-based web interface to control startup, static, breathing, and flicker LED modes.

---

## 🔧 Hardware Requirements

- Raspberry Pi Zero 2 W (or any Pi with I2C support)
- Adafruit PCA9685 16-channel 12-bit PWM Servo Driver
- LEDs: 6x individual (head, chest, 2x shoulders, 2x knees) + 1 RGB common anode for thruster
- 100Ω resistors for all cathodes
- 3.3V to 5V level shifting (if needed)

---

## 📌 PCA9685 to Raspberry Pi Pinout

| PCA9685 Pin | Raspberry Pi Pin | Notes               |
|-------------|------------------|----------------------|
| VCC         | 3.3V (Pin 1)     | Logic level voltage  |
| GND         | GND (Pin 6)      | Ground               |
| SDA         | SDA1 (Pin 3)     | I2C Data             |
| SCL         | SCL1 (Pin 5)     | I2C Clock            |
| V+          | 5V (Pin 2 or 4)  | Power for LEDs       |

---

## 📌 PCA9685 Channel to LED Map

| Channel | LED           |
|---------|---------------|
| 0       | Head          |
| 1       | Chest         |
| 2       | Shoulder L    |
| 3       | Shoulder R    |
| 4       | Knee L        |
| 5       | Knee R        |
| 6       | Thruster Red  |
| 7       | Thruster Green|
| 8       | Thruster Blue |

Each LED's **cathode** connects through a **100Ω resistor** to the PCA9685. The **common anode** connects to **+5V**.

---

## 💡 Raspberry Pi Configuration (Enable I2C)

1. Open configuration tool:

   ```bash
   sudo raspi-config
   ```

2. Go to **Interface Options** → **I2C** → Enable

3. Reboot:

   ```bash
   sudo reboot
   ```

4. Check if PCA9685 is detected:

   ```bash
   i2cdetect -y 1
   ```

   You should see address `0x40` in the grid.

---

## 🚀 Installation Instructions

### 📄 install_barbatos.sh

Use this script to automatically set up the software:

```bash
chmod +x install_barbatos.sh
./install_barbatos.sh
```

This will:

- Install required system packages
- Clone the GitHub repository
- Create a virtual environment
- Install Python dependencies
- Optionally set up systemd service (commented out by default)

---

## 🖥 Running the Web Server

```bash
cd ~/barbatos_rgb_twinkle
source ledvenv/bin/activate
python web_led.py
```

Access the interface at:

```
http://<raspberry-pi-ip>:8080
```

---

## 🌈 LED Modes

| Mode     | Behavior                                                   |
|----------|------------------------------------------------------------|
| Startup  | All LEDs fade in/out with random phase                    |
| Static   | Body LEDs stay on, thruster cycles blue → red → flame     |
| Breathe  | Body LEDs breathe asynchronously, thruster continues cycle|
| Flicker  | Body LEDs flicker randomly, thruster continues cycle      |

---

## 🧰 Troubleshooting

- `ModuleNotFoundError: No module named 'lgpio'`  
  → Run:  
  ```bash
  sudo apt install python3-lgpio
  ```

- I2C not detected (`0x40` missing)  
  → Double check wiring and `raspi-config` settings.

---

## 📁 Project Structure

```
barbatos_rgb_twinkle/
├── web_led.py           # Quart web server
├── led_modes_async.py   # LED animations
├── ledvenv/             # Virtual environment
├── install_barbatos.sh  # Installer script
```

---

## 📜 License & Credits

- Inspired by Kosmos MG Barbatos LED kit
- Developed by [@azkikr316](https://github.com/azkikr316)
- Powered by Adafruit Blinka + CircuitPython

---

✨ Enjoy your custom Gundam lighting experience!
