#__________________ Keeps Track of Total Orders __________________#

def Order_Number_See() :
    with open("Orders.txt", "r") as file :
        file.seek(12)
        f = file.read()
        return int(f)

def Order_Number_Change(number : int) :
    with open("Orders.txt", "r+") as file :
        file.seek(12)
        if Order_Number_See() == 999 :
            number -= 899
        file.write(str(number))
