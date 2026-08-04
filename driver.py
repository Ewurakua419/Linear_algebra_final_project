from players import Players
import sys


ans= -1
def choice(val):
    choice = int(input(val))
    if choice == 0:
        sys.exit("Goodbye!")
    return choice


print('==== Player Analysis ====\n  Choose dataset')
start=""
while start not in ["y" ,"n"]:
    start= str(input(" Would you like to use your own dataset y/n: ")).lower().strip()
    if start not in ["y", "n"]:
        print("Please type either y / n")
numy=str(input("Is there a specific number of players you want to check for ? y/n : ")).lower().strip()
num=0
if numy=="y":
    try:
        num=int(input("Please enter how many users: "))
    except ValueError:
        print("Invalid number. Using all players.")

if start == "y":
    filename = str(input("Please enter your file, ensure that it is a .csv file and ends with .csv: ")).strip()
    player=Players(file=filename, num=num)

else:
    player=Players(num=num)

while ans!=0:
    print('==== Player Analysis ====\n 1. Substitution mode \n 2. Check most similar players \n Enter 0 to exit \n')
    try:
        ans=choice('Please Enter your choice: ')
        if ans==1:

            print(   "==== Substition mode ====\n  " )
            try:
                ans1=0
                while ans1!=-1:
                    name= str(input("Enter Player name: ")).strip()
                    try:
                        pass#player.s
                        remove=""

                        while remove not in ["y" ,"n"]:
                            remove=str(input("Remove player? y/n: "))
                        if remove=="y":
                            player.remove(name)
                        print("==== Substition mode ====\n 1. Continue\n  Enter -1 to go back to Player Analysis \n Enter -2 to restart Substitution mode\n Enter 0 to exit program\n")
                        try:
                            ans1=choice('PLease enter your choice:')
                            if ans1== -2 :
                                continue
                            elif ans1==-1:
                                break
                        except ValueError:
                            print('Make sure it is a number like 1,2,3 or 4')
                    except Exception as e:
                        print(e)
                        ans1=-1
            except ValueError:
                print('Make sure it is a number like 1,2,3 or 4')

        elif ans==2:
            print(
                "==== Most Similar Players ====\n 1. Visualization \n 2. Check most similar players \n Enter 0 to exit \n Enter -2 to return to Player Analysis\n"
            )
            
            while True:
                try:
                    ans1=choice('PLease Enter your choice: ')

                    if ans1== -2:
                        break

                    else:
                        player.euclidean_distance()
                        if ans1==1:#heatmap
                            player.comparism()
                        elif ans1==2:#list of similar players
                            print( "==== Most Similar Players ====\n How many similar players do you want to see ")
                            try:
                                ans2=choice('PLease Enter your choice: ')
                                if ans2>0:
                                    print(player.similarity(num=ans2))
                                else:
                                    print(player.similarity())
                            except ValueError:
                                print('Make sure it is a number like 1,2,3 or 4')

                except Exception as e:
                    print(e)
                    print('Make sure it is a number like 1,2,3 or 4')

        
        else:
            print('Invalid choice')
    except ValueError:
        print('Make sure it is a number like 1,2,3 or 4')
