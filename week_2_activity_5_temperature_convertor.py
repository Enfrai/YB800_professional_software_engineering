'''
Week 2 - Activity 5: Develop an OOP python project - temperature convertor - Due date: 8:00 AM -15 Aug 2026

Temperature converter
For this project, I want to build a temperature converter that transforms user-enteredtemperatures between Fahrenheit and Celsius. 
The input for Fahrenheit temperatures should startwith an uppercase 'F', and for Celsius, it should start with an uppercase 'C'. 
Hence, the projectneeds to include validation and interpretation of user input.

If the input is in Fahrenheit (e.g, 'F51'), the program should convert it to Celsius, rounding to twodecimal places, 
and output: "F51 degrees Fahrenheit is converted to XX.XX degrees Celsius",where 'XX.XX' is the converted temperature value. 
Conversely, if the input is in Celsius (e.g,'C11'), the program should convert it to Fahrenheit, rounding to two decimal places, 
and output:"C11 degrees Celsius is converted to YY.YY degrees Fahrenheit", where 'YYYY is the convertedtemperature value.

Should the user enter an incorrect format or use the wrong prefix, 
the program should promptthem with: "Invalid input. Please enter the temperature with the correct 'C' or F' prefix.'
'''

from enum import Enum

class TemperatureType(Enum):
    F = 0
    C = 1


class TemperatureConvertor:
    type = None
    value = None

    def __init__(self):
        pass

    def translate(self, s: str) -> bool:
        return True

    def read(self):
        while True:
            value = input('Please enter a temperature with \'C\' for Celsius or \'F\' for Fahrenheit: ').strip()
            value_check = len(value) > 1

            if value_check and value.startswith('C'):
                type = TemperatureType.C
            elif value_check and value.startswith('F'):
                type = TemperatureType.F
            else:
                print('Invalid input. Please enter the temperature with the correct \'C\' or \'F\' prefix (eg. F51 or C15).')
                continue

            try:
                temperature = float(value[1:])
            except ValueError:
                print('Invalid input. Please enter the temperature with the correct \'C\' or \'F\' prefix (eg. F51 or C15).')
                continue

            self.type = type
            self.value = temperature
            break

        return self

    def _format_a_float_string(self, s: str) -> str:
        return s.rstrip('0').rstrip('.')

    def convert_and_print(self):
        if TemperatureType.F == self.type:
            print(f'F{self.value} degrees Fahrenheit is converted to {round((self.value - 32) * 5.0 / 9, 2)} degrees Celsius.')
            # print(self._format_a_float_string(f'F{self.value:.2f}') + 
            #       ' degrees Fahrenheit is converted to ' + 
            #       self._format_a_float_string(f'{((self.value - 32) * 5.0 / 9):.2f}') + 
            #       ' degrees Celsius.')
        elif TemperatureType.C == self.type:
            print(f'C{self.value} degrees Celsius is converted to {round(self.value * 1.8 + 32, 2)} degrees Fahrenheit.')
            # print(self._format_a_float_string(f'C{self.value:.2f}') + 
            #       ' degrees Celsius is converted to ' + 
            #       self._format_a_float_string(f'{(self.value * 1.8 + 32):.2f}') + 
            #       ' degrees Fahrenheit.')
        else:
            raise ValueError('Have to invoke read() before converting.')

def main():
    times = 5
    while times > 0:
        try:
            TemperatureConvertor().read().convert_and_print()
            break
        except ValueError:
            print('Try one more time...')
            times = times - 1


if __name__ == '__main__':
    main()