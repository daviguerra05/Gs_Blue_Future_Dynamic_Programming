from numpy import linspace, meshgrid, pi, sin, cos 

class Sensor:
    def calculateReadingArea(self):
        # Setting sphere parameters
        theta = linspace(0, 2 * pi, 100)  # theta angle
        phi = linspace(0, pi, 100)  # phi angle
        # Crete a grid for phi and theta
        theta, phi = meshgrid(theta, phi)
        #Calculate sphere x,y and z
        x = self.x + self.radius * sin(phi) * cos(theta)
        y = self.y + self.radius * sin(phi) * sin(theta)
        z = self.z + self.radius * cos(phi)
        return (x,y,z)
    
    def __init__(self,center,radius) -> None:
        self.center = center
        self.x= center[0]
        self.y= center[1]
        self.z= center[2]
        self.color = 'orangered'
        self.radius = radius
        self.reading_area = self.calculateReadingArea()   