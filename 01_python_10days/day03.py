Inputscore = int(input("enter the Marks scored: "))
if Inputscore >= 90 and Inputscore <= 100:
    print("Grade A")
elif Inputscore >= 80 and Inputscore < 90:
    print("Grade B")
elif Inputscore >= 70 and Inputscore < 80:
    print("Grade C")
elif Inputscore <= 69:
    print("Fail")
else:
    print("enter marks within 100 value ")