import numpy as np

def calculator():
    print("\n--- NumPy Calculator ---")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Power")
    print("6. Square Root")
    print("7. Exit")

    while True:
        choice = input("\nEnter your choice (1-7): ")

        if choice == "7":
            print("Calculator closed.")
            break

        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Invalid choice!")
            continue

        a = float(input("Enter first number: "))

        if choice in ["1", "2", "3", "4", "5"]:
            b = float(input("Enter second number: "))

        if choice == "1":
            print("Result:", np.add(a, b))

        elif choice == "2":
            print("Result:", np.subtract(a, b))

        elif choice == "3":
            print("Result:", np.multiply(a, b))

        elif choice == "4":
            if b == 0:
                print("Error: Division by zero")
            else:
                print("Result:", np.divide(a, b))

        elif choice == "5":
            print("Result:", np.power(a, b))

        elif choice == "6":
            if a < 0:
                print("Error: Cannot find square root of negative number")
            else:
                print("Result:", np.sqrt(a))


calculator()