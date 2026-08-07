from week_1_to_2_exercise_1 import on_value_error

class BMI:
    def __init__(self, weight: float, height: float):
        self.weight = weight
        self.height = height

    def calculate(self) -> float:
        return round(self.weight / self.height ** 2, 2)

def main():
    try:
        weight = float(input('Please input the weight(kg): '))
        height = float(input('Please input the height(m): '))

        bmi = BMI(weight, height)
        print(f'The BMI is {bmi.calculate()}')
    except ValueError:
        on_value_error(prompt='Please provide weight and height in FLOAT value', f=main)

if __name__ == '__main__':
    main()