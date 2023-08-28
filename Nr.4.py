from gpiozero import LED, Button
import time
import sqlite3

class CustomLED:
    def __init__(self, pin):
        self.led = LED(pin)
        self.state = False

    def toggle(self):
        self.state = not self.state
        self.led.value = self.state

    def set_state(self, state):
        self.state = state
        self.led.value = self.state

class CustomButton:
    def __init__(self, pin):
        self.button = Button(pin)

    def is_pressed(self):
        return self.button.is_pressed

# GPIO-Pins
LED_PIN = 17
BUTTON_PIN = 18

# Initialisierung
led = CustomLED(LED_PIN)
button = CustomButton(BUTTON_PIN)

# Datenbankverbindung
db = sqlite3.connect('data.db')
cursor = db.cursor()
with open("data_table.sql", "r") as table:
    sql = table.read()
    cursor.executescript(sql)

def update_database(time_stamp, led_on):
    cursor.execute('INSERT INTO data (time_stamp, led_on) VALUES (?, ?)', (time_stamp, int(led_on)))
    db.commit()

try:
    while True:
        if button.is_pressed():
            led.toggle()

            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            state_text = 'TRUE' if led.state else 'FALSE'
            
            update_database(timestamp, led.state)
            
            while button.is_pressed():
                pass  # Warte, bis der Taster losgelassen wird

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    db.close()
