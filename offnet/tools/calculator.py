import math
import operator

class Calculator:
    """Offline calculator with advanced functions"""
    
    def __init__(self):
        self.operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '^': operator.pow,
            '**': operator.pow,
        }
        
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log10,
            'ln': math.log,
            'sqrt': math.sqrt,
            'abs': abs,
            'round': round,
            'floor': math.floor,
            'ceil': math.ceil,
        }
    
    def calculate(self, expression: str) -> float:
        """Calculate mathematical expression"""
        try:
            # Safe evaluation
            allowed_names = {**self.functions, **math.__dict__}
            code = compile(expression, '<string>', 'eval')
            
            for name in code.co_names:
                if name not in allowed_names:
                    raise NameError(f"Use of {name} not allowed")
            
            return eval(code, {"__builtins__": {}}, allowed_names)
        except Exception as e:
            raise ValueError(f"Calculation error: {e}")
    
    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """Unit conversion"""
        conversions = {
            'length': {
                'm': 1, 'km': 1000, 'cm': 0.01, 'mm': 0.001,
                'mile': 1609.34, 'yard': 0.9144, 'foot': 0.3048, 'inch': 0.0254
            },
            'weight': {
                'kg': 1, 'g': 0.001, 'mg': 0.000001,
                'pound': 0.453592, 'ounce': 0.0283495
            },
            'temperature': {
                'c': lambda x: x,
                'f': lambda x: (x - 32) * 5/9,
                'k': lambda x: x - 273.15
            }
        }
        
        # Find the conversion category
        for category, units in conversions.items():
            if from_unit in units and to_unit in units:
                if category == 'temperature':
                    # Convert to Celsius first, then to target
                    celsius = units[from_unit](value)
                    if to_unit == 'c':
                        return celsius
                    elif to_unit == 'f':
                        return celsius * 9/5 + 32
                    elif to_unit == 'k':
                        return celsius + 273.15
                else:
                    # Simple ratio conversion
                    return value * units[from_unit] / units[to_unit]
        
        raise ValueError(f"Cannot convert from {from_unit} to {to_unit}")
