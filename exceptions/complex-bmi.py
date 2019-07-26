def calculateBMI(weight, height):
    if weight <= 0:
       return 0, "Weight must be larger than 0"
       
    if height <= 0:
       return 0, "Height must be larger than 0"
    
    return weight/(height * height), "success"

# By default, this while loop will run forever
while True:
    weight = float(input("Please enter your weight: "))    
    height = float(input("Please enter your height: "))
    
    bmi, status,x,y,z,a = calculateBMI(weight, height)
    if status == 'success':
        print ("Your bmi is ", bmi)
        break # will take us out of the loop
    else:
        print (status)


print("Done")