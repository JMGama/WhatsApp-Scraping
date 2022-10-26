i=28
a=1

print("Welcome to the Game")
print("You have to guess a number which is assumed by thr computer you will have 9 attempts \n","Let's Start\n","NOTE:the number is between 1 to 50")
while (a<=9):
        choice = int(input("Enter a umber:"))
        if choice>i:
            print("Leser")
        elif choice<i:
            print("Greater")
        else:
            print("Congrats you are correct\n")
            print(a,"no of guesses he took to finish")
            break
        print(9-a,"no of attempt left")
        a = a + 1
if(a>9):
    print("Game Over")




