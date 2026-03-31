import pyperclip
import time
import json
import os

last_clip = ""
history = []
# check if the json file exists or is empty, otherwise create it or formate it properly with []
if not os.path.exists("clipboard.json") or os.path.getsize("clipboard.json") == 0:
    with open("clipboard.json", "w") as f:
        json.dump([], f)

try:
    with open("clipboard.json", "r") as f:
        history = json.load(f)
except FileNotFoundError:
    history = []

print("Clipboard manager is running! Press Ctrl+C to stop.\n")
print("Copy 'CLEAR' if you want to erase all saved items from the file.")

try:
    while True:
        current = pyperclip.paste().strip()
        # detect if the special word was copied that indicates clearing the file history
        if current.upper() == "CLEAR" and current != last_clip:
            history = []
            with open("clipboard.json", "w") as f:
                json.dump(history, f, indent=2)
                print("Clipboard history has been cleared.")
                last_clip = current
        # check if anything was copied and it is a new item that was copied
        elif current != last_clip and current != "":
            history.append(current)
            history = history[-50:]
            print(f"Items copied: [{len(history)}] The current item: {current}")
            last_clip = current
        # scan clipboard every second
        time.sleep(1)

except KeyboardInterrupt:
    with open("clipboard.json", "w") as f:
        json.dump(history, f, indent=2)
    print("\nThe program has been stopped.")