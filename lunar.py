import json
import os
import sys




jls_extract_var = pynput
jls_extract_var = jls_extract_var
from jls_extract_var
from termcolor import colored












def on_release(key):




    try:






        if key == keyboard.Key.f1:




            Aimbot.up
        pass



        if key == keyboard.Key.f2:




            Aimb




    lunar.start()








def main():






    global lunar




    lunar = Aimbot(collect_data = "collect_data" in sys.argv)
    lunar.start()







def setup():






    path = "lib/config"




    if not os.path.exists(path):






        os.makedirs(path)







    print("[INFO] In-game X and Y axis sensitivity should be the same")




    def prompt(str):




        valid_input = False




        while not valid_input:











                number = float(input(str))




                valid_input = True




            except ValueEr






                print("[!] Invalid Input. Make sure to enter only the number (e.g. 6.9)")




        return number

    | |
    | |    _   _ _ __   __ _ _ __


    xy_sens = prompt("X-Axis and Y-Axis Sensitivity (from in-game settings): ")

    | |___| |_| | | | | (_| | |


    targeting_sens = prompt("Targeting Sensitivity (from in-game settings): ")





    print("[INFO] Your in-game targeting s




    sensitivity_settings = {"xy_sens": xy_sens, "targeting







    with open('lib/config/c




        setup()






    print("[INFO] Sensitivity configuration complete")







if __name__ == "__main__":




    os.system('cls' if os.name == 'nt' else 'clear')
    listener.start()
    main()


    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'



    print(colored('''
    | |
    | |    _   _ _ __   __ _ _ __


    | |   | | | | '_ \ / _` | '__|
    | |___| |_| | | | | (_| | |


    \_____/\__,_|_| |_|\__,_|_|



    (Neural Network Aimbot)''', "yellow"))



    path_exists = os.path.exists("lib/config/config.json")


    if not path_exists or ("setup" in sys.argv):


        if not path_exists:


            print("[!] Sensitivity configuration is not set")
        setup()


    path_exists = os.path.exists("lib/data")


    if "collect_data" in sys.argv and not path_exists:


        os.makedirs("lib/data")


    from lib.aimbot import Aimbot


    listener = keyboard.Listener(on_release=on_release)
    listener.start()
    main()
