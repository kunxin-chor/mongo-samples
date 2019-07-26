def calculateBMI(weight, height):
    if weight <= 0:
       return None
       
    if height <= 0:
       return None
    
    return weight/(height * height)

# By default, this while loop will run forever
while True:
    weight = float(input("Please enter your weight: "))    
    height = float(input("Please enter your height: "))
    
    bmi = calculateBMI(weight, height)
    if bmi is not None:
        print ("Your bmi is ", bmi)
        break # will take us out of the loop
    else:
        print (status)


print("Done")