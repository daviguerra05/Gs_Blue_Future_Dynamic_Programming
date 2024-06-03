import matplotlib.pyplot as plt
from colorama import Fore
from itertools import combinations
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from numpy import sqrt, array
from numpy.random import randint
from Sensor import Sensor
from time import sleep

def distance_between_two_points(A,B):
    return sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2 + (B[2] - A[2])**2)

def verify_two_esphere_collision(sensor1, sensor2):
    return distance_between_two_points(sensor1.center, sensor2.center) <= sensor1.radius + sensor1.radius

def any_collision(sensors):
    for sensor1, sensor2 in combinations(sensors,2):
        if verify_two_esphere_collision(sensor1,sensor2):
            return True
    return False

def allocate_sensors(num_sensors,radius,axis_size):
    sensors = []
    # Starting coordenates
    coord = [0,0,0]
    # Main loop to allocate sensors
    while len(sensors) < num_sensors:
        newCoord = coord.copy()
        for _ in range(3):
            axis = randint(0,3) # Choose a random coordenate to take a step
            # Check if the chosen coordanate is in the first half 
            if newCoord[axis] <= axis_size//2:
                newCoord[axis] += randint(radius, axis_size-newCoord[axis]-radius) # Add step
            else:
                newCoord[axis] -= randint(radius, newCoord[axis]) # Subtract a step
        
        # Create new sensor if the new coordinate
        newSensor = Sensor(newCoord,radius)
        # Check if its new reading area collides with another sensor
        if any(verify_two_esphere_collision(newSensor, sensor) for sensor in sensors):
            continue # Start Again
        # Add to list
        sensors.append(newSensor)
        # Set the current coordenate to the new one, for next step calculus.
        coord = newCoord.copy()
    return sensors

def detect_garbage(sensors,garbage):
        garbage_detected = []
        for sensor in sensors:
            for lixo in garbage:
                if distance_between_two_points(lixo.center,sensor.center) <= sensor.radius:
                    garbage_detected.append(lixo)
        return garbage_detected 

def garbage_in_region(garbage,region_ratio,i,axis):
    # Checks if a given garbage is in a determined region.
    return region_ratio*(i-1) < garbage.center[axis] <= region_ratio*i 

def concentration_area(detected_garbage,axis_size,num_subregions):
    region_ratio = axis_size//num_subregions
    subs = []
    # Calculates the higher garbage concentration for each axis
    for axis in range(3):
        # Count garbage for each subregion in axis
        region_counts = [sum(garbage_in_region(garbage,region_ratio,i,axis) for garbage in detected_garbage) for i in range(1,num_subregions+1)]
        # Get the max index
        max_index = region_counts.index(max(region_counts))
        # Append the subregion with higher garbage concentration     
        subs.append(max_index+1)
    return subs

def view_concentration_area(x_lim,y_lim,z_lim,garbage_detected,axis_size):
    # Create cube vertices
    vertices = array([[x_lim[0], y_lim[0], z_lim[0]],
                        [x_lim[1], y_lim[0], z_lim[0]],
                        [x_lim[1], y_lim[1], z_lim[0]],
                        [x_lim[0], y_lim[1], z_lim[0]],
                        [x_lim[0], y_lim[0], z_lim[1]],
                        [x_lim[1], y_lim[0], z_lim[1]],
                        [x_lim[1], y_lim[1], z_lim[1]],
                        [x_lim[0], y_lim[1], z_lim[1]]])

    # Setting cube faces using its vertices
    faces = [[vertices[j] for j in [0, 1, 2, 3]],
            [vertices[j] for j in [4, 5, 6, 7]], 
            [vertices[j] for j in [0, 3, 7, 4]],
            [vertices[j] for j in [1, 2, 6, 5]],
            [vertices[j] for j in [0, 1, 5, 4]],
            [vertices[j] for j in [2, 3, 7, 6]]]
    
    # Plot 3d graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Adding faces to 3d axis
    ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
    # Plotting garbages on the graph
    for garbage in garbage_detected:
            ax.scatter(garbage.x,garbage.y,garbage.z,marker='v',color=garbage.color)
    # Setting axises limits
    ax.set_xlim(0, axis_size)
    ax.set_ylim(0, axis_size)
    ax.set_zlim(0, axis_size)
    # Adding labels
    ax.set_title('Garbage Concentration')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # Show graph
    plt.show()

def analyze_garbage_data(detected_garbage,num_garbage, num_sensors, axis_size):
    # Calculate garbage detection percentage
    detected_percentage = (len(detected_garbage)/num_garbage)*100
    # Output analysis
    print(Fore.BLUE+"\nGarbage Analisis"+Fore.RESET)
    print('-'*10)
    print(f'{Fore.GREEN + str(len(detected_garbage)) + Fore.RESET} garbage out of {num_garbage} were found using {Fore.RED+str(num_sensors)+Fore.RESET} sensors.')
    print(f'Given a total of {Fore.GREEN+str(round(detected_percentage,2))+Fore.RESET}% garbage detected.')
    # Determine subregions
    numSubregioes = 2
    c_a = concentration_area(detected_garbage,axis_size,numSubregioes)
    x_lim_inf = axis_size//numSubregioes*(c_a[0]-1)
    x_lim_sup = axis_size//numSubregioes*c_a[0]
    y_lim_inf = axis_size//numSubregioes*(c_a[1]-1)
    y_lim_sup = axis_size//numSubregioes*c_a[1]
    z_lim_inf = axis_size//numSubregioes*(c_a[2]-1)
    z_lim_sup = axis_size//numSubregioes*c_a[2]
    # Output concentration area
    print(f'\nThe higher {Fore.YELLOW}concentration{Fore.RESET} of garbage is in the area where: \
            \n{x_lim_inf} < {Fore.YELLOW}x{Fore.RESET} <= {x_lim_sup} \
            \n{y_lim_inf} < {Fore.YELLOW}y{Fore.RESET} <= {y_lim_sup} \
            \n{z_lim_inf} < {Fore.YELLOW}z{Fore.RESET} <= {z_lim_sup}')
    #Visualization
    match input('\nDo you want to visualize the garbage concentration area render?\nAnswer (y/n): '):
        case "n":
            pass        
        case _:
            print(Fore.YELLOW+'\nClose next window to return.'+Fore.RESET)
            sleep(2) # Two seconds
            view_concentration_area((x_lim_inf,x_lim_sup),(y_lim_inf,y_lim_sup),(z_lim_inf,z_lim_sup),detected_garbage,axis_size)
    print('\nReturning to simulation menu...')
    sleep(0.5)

def view_sensors_distribution(sensors, garbage, axis_size,anim):
    #Plot 3d Graph
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111,projection="3d") 
    # Setting axises limits
    ax.set_xlim(0, axis_size)
    ax.set_ylim(0, axis_size)
    ax.set_zlim(0, axis_size)
    # Adding labels
    ax.set_xlabel('axis X')
    ax.set_ylabel('axis Y')
    ax.set_zlabel('axis Z')
    # Plotting sensors
    for i,sensor in enumerate(sensors):
        ax.scatter(sensor.x,sensor.y,sensor.z,color=sensor.color)
        # Plotting reading sphere surface
        ax.plot_surface(sensor.reading_area[0],sensor.reading_area[1],sensor.reading_area[2], color=sensor.color, alpha=0.3)
        # Counter
        ax.set_title(f'Total sensors: {i+1}')
        # Animation
        if anim: plt.pause(0.0001)
    # Plotting garbage
    for g in garbage:
        ax.scatter(g.x,g.y,g.z,marker='v',color=g.color)
    # Show graph
    plt.show()