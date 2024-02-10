import RPi_I2C_driver
import RPi.GPIO as GPIO
import time

mylcd = RPi_I2C_driver.lcd()
mylcd.backlight(1)
mylcd.lcd_clear()


mylcd.lcd_display_string("Enter Combo:", 1)


L1 = 16
L2 = 20
L3 = 21
L4 = 5
C1 = 6
C2 = 13
C3 = 19
C4 = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

combo_input = ""
valid_combinations = ['ALPETO', 'XIOTLA', 'AEITOP', 'XTOPLI', 'AIXOLP', 'EXLIPA', 'LOATPI', 'ETXAOI', 'LAXTEO', 'ETPIOA', 'ITEPOL', 'TXALPO', 'ILOTXP', 'TLAPXE', 'ILXATO', 'OTALIX', 'PXLOEA', 'OEIPAX', 'PAIETL', 'OITAEL', 'XILEPT', 'AOEXLP', 'XLTAEO', 'AOPTLX', 'XAILOT', 'LOPIAE', 'ETLIAX', 'LIXTEA', 'EOTXIL', 'LEXPTA', 'TPILXO', 'IAXPOL', 'TAOEXL', 'IEAXPT', 'TAPIXE', 'PLIXEA', 'OEXPTL', 'POXATL', 'OTPEAX', 'PXTIAE', 'APLXTO', 'XLEAPO', 'APOTIL', 'XPOEIA',
                      'AOXEIT', 'ELOIXP', 'LXIAPT', 'ELPAXO', 'LAPOTI', 'EXOALT', 'IEOPXT', 'TEAPOL', 'IOTPLE', 'TLEOXP', 'OTLXPI', 'PEIAOT', 'OXIPTA', 'PIOXEL', 'XPEOIL', 'ALXETP', 'XEILPO', 'ALIXEP', 'LPTIXO', 'ETAOIP', 'LIOETP', 'ETOXAI', 'TOELPI', 'IPETAO', 'TPOEXI', 'IOPXAE', 'POITEL', 'OLAPTX', 'PLOXEA', 'OTIALE', 'AIPXEO', 'XAPLTO', 'ALTIXE', 'XOALTI', 'EIXAOL', 'LAEPIO', 'EIPAXO', 'ETPXEI', 'IOAPXE', 'TOLIEX', 'IOLEAT', 'TILPAO', 'OAXIEP', 'PLEIAT', 'OATPLI', 'PLXTOA']

used_combinations = set()
code_displayed_half = False
code_displayed_full = False
blink = True


def initialize():
    global combo_input, used_combinations, code_displayed_half, code_displayed_full, blink
    combo_input = ""
    used_combinations.clear()
    code_displayed_half = False
    code_displayed_full = False
    blink = True
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Enter Combo:", 1)
    mylcd.lcd_display_string("      Code:____", 2)


def update_display():
    global code_displayed_half, code_displayed_full
    if combo_input in valid_combinations and combo_input not in used_combinations:
        if code_displayed_half:
            mylcd.lcd_display_string("      Code:2791", 2)
            code_displayed_full = True
        else:
            mylcd.lcd_display_string("      Code:27__", 2)
            code_displayed_half = True
        used_combinations.add(combo_input)


def reset_display():
    global combo_input
    combo_input = ""
    if not code_displayed_half:
        mylcd.lcd_display_string("      Code:____", 2)


def update_display():
    global code_displayed_half, code_displayed_full
    if combo_input in valid_combinations:
        if code_displayed_half:
            mylcd.lcd_display_string("      Code:2791", 2)
            code_displayed_full = True
        else:
            mylcd.lcd_display_string("      Code:27__", 2)
            code_displayed_half = True


def check_combo():
    global combo_input
    if combo_input == "******":
        reset()
    else:
        if combo_input in valid_combinations and combo_input not in used_combinations:
            update_display()
            used_combinations.add(combo_input)
            combo_input = ""
        elif combo_input not in valid_combinations or combo_input in used_combinations:
            mylcd.lcd_display_string("Incorrect   ", 1)
            time.sleep(2)
            mylcd.lcd_display_string("Enter Combo:", 1)
            reset_display()


def backspace():
    global combo_input
    if combo_input:
        combo_input = combo_input[:-1]


def reset():
    initialize()


def readLine(line, characters):
    global combo_input, blink
    GPIO.output(line, GPIO.HIGH)

    if GPIO.input(C1) == 1:
        combo_input += characters[0]
    elif GPIO.input(C2) == 1:
        combo_input += characters[1]
    elif GPIO.input(C3) == 1:
        if characters[2] == "C":
            backspace()
        else:
            combo_input += characters[2]
    elif GPIO.input(C4) == 1:
        if characters[3] == "*":
            reset()
            return
        else:
            combo_input += characters[3]

    GPIO.output(line, GPIO.LOW)

    display_code = "Code:27__" if code_displayed_half and not code_displayed_full else "Code:____"
    display_code = "Code:2791" if code_displayed_full else display_code
    cursor = "_" if len(combo_input) < 6 and blink else ""
    mylcd.lcd_display_string(
        combo_input + cursor.ljust(6 - len(combo_input)) + " " + display_code, 2)

    if len(combo_input) == 6:
        check_combo()


time.sleep(5)

try:
    initialize()
    while True:
        readLine(L1, ["I", "O", "X", "L"])
        readLine(L2, ["T", "E", "A", "P"])
        readLine(L3, ["7", "8", "9", "C"])
        readLine(L4, ["*", "0", "#", "D"])
        blink = not blink
except KeyboardInterrupt:
    print("\nProgram stopped")
