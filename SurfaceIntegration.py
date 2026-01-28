import numpy as np
from AlphaGenericTools import AlphaGeneric


'''import sympy as sp
x,y,z = sp.symbols("x y z")
f = sp.lambdify((x,y,z), sp.sympify(user_str), "numpy")'''

def SurfaceIntegral(lower_limit, upper_limit, beta_func, gamma_func, restOfIntegral_func):

    X = np.linspace(lower_limit, upper_limit, 500)
    dx = abs(X[1] - X[0]) # must be unsigned as it is used to find dA (an area) which can only be positive (in this case)

    Force_z = 0
    Force_x = 0

    for x in X:
        Alpha_z, Alpha_x = AlphaGeneric(beta_func(x), gamma_func(x))
        Force_z += Alpha_z * restOfIntegral_func(x) * dx
        Force_x += Alpha_x * restOfIntegral_func(x) * dx

    return Force_z, Force_x


class SemiSubmergedVerticalPlate():

    def __init__(self, width, depth):
        self.width = width
        self.lower_limit = 0
        self. upper_limit = depth

    @staticmethod
    def beta(z):
        return np.pi / 2
    
    @staticmethod
    def gamma(z):
        return 0
    
    def restOfIntegral(self, z):
        return z * self.width
    


class HalfSubmergedHorizontalCylinder():

    def __init__(self, width, radius):
        self.width = width
        self.radius = radius
        self.lower_limit = 0
        self.upper_limit = np.pi / 2

    @staticmethod
    def beta(theta):
        return np.pi / 2 - theta
    
    @staticmethod
    def gamma(theta):
        return 0
    
    def restOfIntegral(self, theta):
        return self.radius * self.radius * self.width * np.sin(theta)
    

class HalfSubmergedSphere():

    def __init__(self, radius):
        self.radius = radius
        self.lower_limit = 0
        self.upper_limit = np.pi / 2

    @staticmethod
    def beta(theta):
        return np.pi / 2 - theta
    
    @staticmethod
    def gamma(theta):
        return 0
    
    def restOfIntegral(self, theta):
        return 2 * self.radius ** 3 * np.sin(theta) * np.cos(theta)


if __name__ == '__main__':

    MyPlate = SemiSubmergedVerticalPlate(20, 10)
    MyPlate.Force_z, MyPlate.Force_x = SurfaceIntegral(MyPlate.lower_limit, MyPlate.upper_limit, MyPlate.beta, MyPlate.gamma, MyPlate.restOfIntegral)
    print(f'Semi-Submerged Vertical Plate:\nZ Force - {np.round(MyPlate.Force_z, 3)} N\nX Force - {np.round(MyPlate.Force_x, 3)} N\n')

    MyCylinder = HalfSubmergedHorizontalCylinder(20, 10)
    MyCylinder.Force_z, MyCylinder.Force_x = SurfaceIntegral(MyCylinder.lower_limit, MyCylinder.upper_limit, MyCylinder.beta, MyCylinder.gamma, MyCylinder.restOfIntegral)
    print(f'Half-Submerged Horizontal Cylinder:\nZ Force - {np.round(MyCylinder.Force_z, 3)} N\nX Force - {np.round(MyCylinder.Force_x, 3)} N\n')

    MySphere = HalfSubmergedSphere(10)
    MySphere.Force_z, MySphere.Force_x = SurfaceIntegral(MySphere.lower_limit, MySphere.upper_limit, MySphere.beta, MySphere.gamma, MySphere.restOfIntegral)
    print(f'Half-Submerged Sphere:\nZ Force - {np.round(MySphere.Force_z, 3)} N\nX Force - {np.round(MySphere.Force_x, 3)} N\n')


