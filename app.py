app.py

from flask import Flask, render_template
import lgpio

app = Flask(__name__)

CHIP = 0
LED1_PIN = 17
LED2_PIN = 27

h = lgpio.gpiochip_open(CHIP)
lgpio.gpio_claim_output(h, LED1_PIN)
lgpio.gpio_claim_output(h, LED2_PIN)

pins = {
    17: {'name': 'GPIO 17'},
    27: {'name': 'GPIO 27'}
}

def get_state(pin):
    return lgpio.gpio_read(h, pin) == 1

@app.route("/")
def main():
    templateData = {
        'pins': {p: {'name': pins[p]['name'], 'state': get_state(p)} for p in pins}
    }
    return render_template('main.html', **templateData)

@app.route("/<int:changePin>/<action>")
def action(changePin, action):
    if changePin in pins:
        if action == "on":
            lgpio.gpio_write(h, changePin, 1)
        elif action == "off":
            lgpio.gpio_write(h, changePin, 0)
    templateData = {
        'pins': {p: {'name': pins[p]['name'], 'state': get_state(p)} for p in pins}
    }
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
