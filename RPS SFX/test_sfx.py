from sfx import play_result


while True:
    print("\n1. Robot wins")
    print("2. Robot loses")
    print("3. Exit")

    choice = input("Choose: ")

    if choice == "1":
        play_result("win")

    elif choice == "2":
        play_result("lose")

    elif choice == "3":
        break

    else:
        print("Invalid choice")