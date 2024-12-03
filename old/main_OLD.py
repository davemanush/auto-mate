import os
import pyautogui, sys
from threading import Thread
from time import sleep
from pynput import keyboard

print('Press Ctrl-C to quit.')
class ButtonPosition:
  def __init__(self, x, y, waitTimeBefore):
    self.x = x
    self.y = y
    self.waitTimeBefore = waitTimeBefore

class Configs:
  def __init__(self, automationIsOn, activePressId, activeSetupButtonActive, activeSetupButtonWaitValue, activeSetupButtonInSetup, runInProgress):
    self.automationIsOn = automationIsOn
    self.activeSetupButtonActive = activeSetupButtonActive
    self.activeSetupButtonInSetup = activeSetupButtonInSetup
    self.activeSetupButtonId = activePressId
    self.activeSetupButtonWaitValue = activeSetupButtonWaitValue
    self.runInProgress = runInProgress



config = Configs(False, -1, False, "", False, False)
pressSequencePositons = []

def runAutomation(conf, pressSequencePos, repeats):
    print("running")
    for x in range(1, repeats):
        for button in repeats:
            os.system('clear')
            print(f'Crafting in progress {x}/{repeats}')
            sleep(button.waitTimeBefore)
            print(str(button.x) + " " + str(button.y))
            pyautogui.moveTo(button.x, button.y)
            pyautogui.mouseDown(button='left')
            pyautogui.mouseUp(button='left')

def on_press(key, config):
    try:
        if key.char == 'b':
            os.system('clear')
            if config.activeSetupButtonInSetup:
                print("Setup Is active, only numeric button are enabled")
                return
            if config.activeSetupButtonActive:
                print("Setup for button is active, press \"i\" and provide wait value")
                return
            x, y = pyautogui.position()
            pressSequencePositons.append(ButtonPosition(x, y, -1))
            config.activeSetupButtonId = len(pressSequencePositons) -1
            config.activeSetupButtonActive = True
        if key.char == 'a':
            os.system('clear')
            sleep(0.2)
            if config.activeSetupButtonInSetup:
                print("Setup Is active, only numeric button are enabled")
                return
            if config.activeSetupButtonActive:
                print("Setup for button is active, press \"i\" and provide wait value")
                return
            print("How many repeats?\n")
            repeats = input()
            if not repeats.isnumeric():
                repeats.isalnum()
                print("[ERROR] Input contains non-numeric characters. Restart automation!")
                return
            runAutomation(config, pressSequencePositons, repeats)
               #thread = Thread(target=runAutomation, args=(config, pressSequencePositons))
               #thread.start()
               #thread.join()
        if key.char == 'i':
            os.system('clear')
            if config.activeSetupButtonInSetup:
                if config.activeSetupButtonWaitValue == "":
                    print("No wait time for button was set up, please only use numbers to set up value!")
                    return
                if not config.activeSetupButtonWaitValue.isnumeric():
                    print("Wait value contains non-numeric characters, please retry adding wait time!")

                    config.activeSetupButtonWaitValue = ""
                    return
                button = pressSequencePositons[config.activeSetupButtonId]
                button.waitTimeBefore = int(config.activeSetupButtonWaitValue)
                config.activeSetupButtonActive = False
                config.activeSetupButtonInSetup = False
                config.activeSetupButtonWaitValue = ""
                print(f'Button was saved with Coordinates X:Y - {button.x}:{button.y} and wait time before button press: {button.waitTimeBefore}')
            else:
                config.activeSetupButtonInSetup = True
        if str(key.char).isnumeric():
            os.system('clear')
            if not config.activeSetupButtonInSetup:
                print("Button is not set up currently.")
                return
            if not config.activeSetupButtonActive:
                print("Setup for button is active, press \"i\" and provide wait value")
                return
            config.activeSetupButtonWaitValue = config.activeSetupButtonWaitValue + key.char
    except AttributeError:
        os.system('clear')
        pass

try:
    with keyboard.Listener(on_press=lambda event: on_press(event, config=config)) as listener:
        listener.join()
    listener.start()
except KeyboardInterrupt:
    print('Exiting...')
    exit(1)