"""
Week 1 - Activity 1.2: Optimization - BMI calculator project

Optimize the code below and try to remove the use of `this` where possible (explain why or why not). 
The goal of this activity is to better understand how `this` works and when it is needed. 
Share your optimized code by posting the GitHub link here.
"""

def isfloat(n):
    """ 
    If string can be converted to floating number 
    returns that number, otherwise returns false
    """
    try:
        n=float(n)
        return n
    except ValueError:
        return False

def inputfloat(hint):
    """ 
    Prints hint and asks to enter number.
    Repeats until decimal number is entered.
    """
    ret = False
    while ret is False:
        ret = isfloat(input(hint))
        if ret is False:
            print("Please enter number")
    return ret 

class BMIcalculator:
    def getdata(self):
        """
        Get weight in kgs and height in cms.
        Height is entered in cetimetres and stored in metres
        """

        self.w = inputfloat("Please enter your weight in kilograms:")
        self.h = inputfloat("Please enter your height in centimetres:")/100

    def calculate(self):
        """
        Calculate and return bmi
        """

        return round(self.w/(self.h*self.h),2)


def main():
    print("\n","="*42,"\n")
    print("Hello, let's calculate your BMI.");
    
    calc = BMIcalculator()
    print()
    calc.getdata()
    bmi=calc.calculate()
    print(f"Your BMI is {bmi}")
    print("\n","="*42,"\n")

if __name__ == "__main__":
    main()