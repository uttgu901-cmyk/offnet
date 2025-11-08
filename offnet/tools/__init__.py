import math

class Calculator:
    def calculate(self, expression: str):
        try:
            # Безопасное вычисление
            allowed = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                      'sqrt': math.sqrt, 'log': math.log10, 'pi': math.pi, 'e': math.e}
            return eval(expression, {"__builtins__": {}}, allowed)
        except:
            raise ValueError("Invalid expression")
