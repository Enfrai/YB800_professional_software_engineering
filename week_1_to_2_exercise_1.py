def on_value_error(prompt: str, f: callable):
    key = input(f'{prompt} q to exit, any other key to try again...')
    if key != 'q' and key != 'Q':
        f()
    else:
        print('Quit!')
        exit(0)

def calculate_average():
    """
    EXERCISE 1
    1. Ask the user to input 3 test scores & assign them to test1, test2, test3. These 3 variables should accept float values.
    2. Find their average.
    3. Assign the result to a variable named average and print its value
    """
    try:
        test1 = float(input('Please input the first float value: '))
        test2 = float(input('the second: '))
        test3 = float(input('and the third: '))
        average = (test1 + test2 + test3) / 3
        print(f'The average of these three is {average}.')
    except ValueError:
        on_value_error(prompt='You have to input FLOAT values.', f=calculate_average)

def calculate_sum_and_product():
    """
    Problem 1: Simple Math Input/Output
    """
    try:
        # Receive two numbers input from user, and convert them to integer type
        num1 = int(input('Please input an integer number: '))
        num2 = int(input('the other integer number: '))

        # do sum calculation
        sum = num1 + num2

        # do multipulation
        mul = num1 * num2

        # print the result
        print(f'The sum of {num1} and {num2} is {sum}.')
        print(f'The production of {num1} times {num2} is {mul}.')
    except ValueError:
        on_value_error(prompt='You have to input INTEGER values.', f=calculate_sum_and_product)

def calculate_bmi():
    """
    Problem 2: Build a BMI Calculator
    Objective: Create a Python script that asks the user for the weight and height and then calculates the Body Mass Index (BMI) score. You can try to use F-strings for output.
    Notes: BMI score = An individual's weight in kilograms by the square of the height in meters
    """
    try:
        weight = float(input('Please input the weight(kg): '))
        height = float(input('Please input the height(m): '))

        bmi = weight * height ** 2
        print(f'The BMI is {bmi}')
    except ValueError:
        on_value_error(prompt='Please provide weight and height in FLOAT value', f=calculate_bmi)

def main():
    calculate_average()
    print('---------------------------------')
    calculate_sum_and_product()
    print('---------------------------------')
    calculate_bmi()


if __name__ == '__main__':
    main()