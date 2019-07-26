def calculateBMI(weight, height):
    return weight/(height * height)

# By default, this while loop will run forever
while(True):
    weight = float(input("Please enter your weight: "))    
    height = float(input("Please enter your height: "))
    
    try:
        bmi = calculateBMI(weight, height)
        print ("Your bmi is ", bmi)
        break # will take us out of the loop
    except:
        print("We have some issues calculating your BMI")

print("Done")