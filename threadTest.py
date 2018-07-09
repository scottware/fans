import threading
import time
import sys
import weather

targetTemp = 70.0


def background():
    while True:
        # temp = weather.outsideTemp()
        temp = 123.4
        print(f"{targetTemp} {temp}")
        time.sleep(5)

def back2():
    while True:
        print("hello")
        time.sleep(4)


thread = threading.Thread(target=background)
thread.daemon = True
thread.start()

# thread2 = threading.Thread(target=back2)
# thread2.daemon = True
# thread2.start()


while True:
    userInput = input("> ")
    if userInput=="a":
        pass
    if userInput == "exit":
        sys.exit()
    else:
        print(f"input *{userInput}*")
        try:
            targetTemp = float(userInput)
        except:
            print(f"ERROR {userInput}")
            exit()
        # targetTemp=float(userInput)
