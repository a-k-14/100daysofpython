#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
    
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

with open("./input/Names/invited_names.txt") as names_file:
    names = []
    for line in names_file:
        # strip the new line character
        name = line.strip()
        names.append(name)
    # names = file.readlines()
    # print(names)

with open("./input/Letters/starting_letter.txt") as letter_file:
    content = letter_file.read()
    for name in names:
        file_name = f"letter_for_{name}.txt"
        message = content.replace("[name]", name)
        with open(f"./Output/ReadyToSend/{file_name}", mode="w") as new_file:
            new_file.write(message)
