import Sylvia
from colorama import Fore
from Garbage import Garbage
from numpy.random import randint
from sys import stdout
from time import sleep
from pygame import mixer
from threading import Thread

def play_music():
    mixer.music.load('song.mp3')
    mixer.music.set_volume(0.4) # 40% volume
    mixer.music.play()

def stop_music():
    mixer.music.stop()

def valid_int_input(msg):
    while True:
        try:
            response = int(input(msg))
            break
        except ValueError:
            print(Fore.RED+'Incorrect input... Enter an Integer'+Fore.RESET)            
    return response

def set_simulation_parameters():
    match input("\nDo you want to use simulation default values?\nAnswer(y/n): ").replace(' ','').lower():
        case "n":
            axis_size = valid_int_input('\nPlease inform the cube axes values: ') 
            reading_radius  = valid_int_input('Please inform the sensor reading sphere radius: ') 
            num_sensors = valid_int_input('Please inform the number of sensors: ')
            num_garbage = valid_int_input('Please inform the total number of garbage:')
        case _:
            # Default values
            axis_size,reading_radius,num_sensors,num_garbage = 100,15,10,1000
    
    return axis_size,reading_radius,num_sensors,num_garbage

def run_simulation():
    # Setting the parameters for the simulation
    axis_size,reading_radius,num_sensors,num_garbage = set_simulation_parameters()
    # Alocating sensors in 3d space
    sensors = Sylvia.allocate_sensors(num_sensors,reading_radius,axis_size)
    # Alocating garbage in 3d space
    garbage = [Garbage(randint(0,axis_size,3)) for _ in range(num_garbage)]
    # Check all garbage in sensors reading areas
    detected_garbage = Sylvia.detect_garbage(sensors,garbage)

    print(Fore.GREEN+'\nSimulation created successfully!'+Fore.RESET)
    # Loop
    while True:
        print(Fore.MAGENTA+'\nGarbage Sensors Simulation'+Fore.RESET)
        print('-'*15)
        match input('Choose:\n1.Visualize the simulation render\n2.Get garbage data analisis\n3.Exit to main menu\n\nAnswer (index): ').replace(' ',''):
            case '1':
                print(Fore.YELLOW+'\nClose next window to return.'+Fore.RESET)
                sleep(2) # Two seconds
                Sylvia.view_sensors_distribution(sensors,garbage,axis_size,anim=True)
            case '2':
                Sylvia.analyze_garbage_data(detected_garbage,num_garbage,num_sensors,axis_size)
            case '3':
                break
            case _:
                print(Fore.RED+'\nThis action doesn´t exist... Try again'+Fore.RESET) 

def typewriter(text):
    for char in text:
        stdout.write(char)
        stdout.flush()
        sleep(0.1)
    print()  # Move to the next line after the text is printed

def see_credits():
    # Pygame mixer init
    mixer.init()
    # Thread to play the song in parallel
    music_thread = Thread(target=play_music)
    music_thread.start()
    print(Fore.YELLOW+'\nCredits'+Fore.RESET)
    print('-'*20)
    typewriter('\n‖ Project Sylvia ‖\nA garbage sensor detector distribution simulation and analysis.')
    typewriter('\nDevelop by:\n• Davi Passanha de Sousa Guerra RM 551605\n• Rui Amorim Siqueira RM 98436\n• Cauã Gonçalvez de Jesus RM 97648')
    typewriter('\nEnjoy. Thanks :)')
    input('\nEnter any key to return ')
    stop_music()

def main():
    print('\nGlobal Solution - Dynamic Programming')
    # Main Loop
    while True:
        print(f"\n{Fore.CYAN}Sylvia{Fore.RESET} - Garbage Sensor Detectors Simulation")
        print("-"*15)
        match input('Choose:\n1.Start Simulation\n2.Credits\n3.Quit\n\nAnswer (index): ').replace(' ',''):
            case '1':
                run_simulation()
            case '2':
                see_credits()
            case '3':
                break
            case _:
                print(Fore.RED+'\nThis action doesn´t exist... Try again'+Fore.RESET) 

if __name__ == '__main__':
    main()