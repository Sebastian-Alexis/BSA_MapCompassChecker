# BSA MapCompassChecker

The BSA MapCompassChecker is a specialized tool designed for use in Troop 691's 2024 Camporee game, specifically tailored for the Compass & Map Relay Game. This repository contains the software required to run the BSA Map and Compass Checker, a device built to validate combinations entered by participants during the game. The software is intended to be run on a Raspberry Pi equipped with an I2C LCD display and a 4x4 keypad for input.

## Description

The main.py script interfaces with an I2C LCD display and a matrix keypad, allowing game participants to enter combinations. The script displays prompts on the LCD and checks the entered combination against a predefined list of valid combinations. Correct combinations display a specific code on the LCD, assisting in the game's progression. When 2 correct awnsers are given, a full 4 digit combination code is dispalyed. This code can be changed, but currently it unlocks a 4 digit lock, which when presented to a leading scout, ends the timer that determines a patrol's score.

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- I2C LCD display
- Matrix Keypad
- Jumper wires for connections

## Software Requirements

- Python 3.x
- RPi.GPIO library
- RPi_I2C_driver (for the LCD display)

## Setup Instructions

1. **Hardware Setup**:

   - Connect the I2C LCD display to the Raspberry Pi I2C pins (SDA, SCL, VCC, GND).
   - Connect the matrix keypad to the designated GPIO pins as per the `main.py` script configuration.

2. **Software Setup**:

   - Ensure Python 3.x is installed on your Raspberry Pi.
   - Install necessary Python libraries using pip:
     ```
     pip install RPi.GPIO
     pip install RPi_I2C_driver
     ```
   - Clone this repository to your Raspberry Pi:
     ```
     git clone https://github.com/Sebastian-Alexis/BSA_MapCompassChecker.git
     ```
   - Navigate to the cloned repository:
     ```
     cd BSA_MapCompassChecker
     ```

3. **Running the Script**:

   - Execute the script with Python 3:
     ```
     python3 main.py
     ```

4. **Automatically Start on Pi Launch**:
   - **Using rc.local**:
     - Open the `rc.local` file in an editor:
       ```
       sudo nano /etc/rc.local
       ```
     - Before the `exit 0` line at the end of the file, add the following line, adjusting the path to where your script is located:
       ```
       python3 /home/pi/BSA_MapCompassChecker/main.py &
       ```
     - Save the file and exit the editor. The script will now run at boot.

## Game Instructions

- Refer to the `Compass & Map Relay Game.pdf` for detailed instructions on setting up and running the game.

## Troubleshooting

- Ensure all connections are secure and correct according to the script.
- Verify that the I2C address of your LCD is correctly set in the `RPi_I2C_driver` initialization within the `main.py` script.
- If the keypad is not registering inputs correctly, check the GPIO pin configuration and ensure they match the keypad wiring.

## Contributing

Contributions to the BSA MapCompassChecker project are welcome. Please submit pull requests or open issues for any improvements or bug fixes. If you have any questions, please send them to sebastianralexis@gmail.com

## License

This project is licensed under the MIT License - see the LICENSE file for details.
