# Demonstrate the use of Python classes
# Two classes are defined. Power and a subclass of Power named RealPower

class Power(object):
    """
    Class that calculates the power of a given number
    """
    
    default_exponent = 2    # If no parameter is given, use 2 as the exponent
    
    def __init__(self, exponent = default_exponent):
        self.exponent = exponent
        
    def of(self, x):
        return x ** self.exponent
    
class RealPower(Power):
    """
    A subclass of Power. It overrides the of method by adding additional checks for Real number
    """
    
    def of(self, x):
        if isinstance(self.exponent, int) or x >= 0:
            return x ** self.exponent
        raise ValueError('Fractional powers of negative numbers of imaginary')
    
print('Power: ', Power)
print('Power.default_exponent:', Power.default_exponent)
square = Power()    # Object to find square
root = Power(0.5)   # Object to find root
print('square: ', square)
print('square of 3: ', square.of(3))
print('root of 3: ', root.of(3))
print('root of -3: ', root.of(-3))
real_root = RealPower(0.5)  # Object to find Real root
print('Real root of -3: ', real_root.of(-3))
print('Done')