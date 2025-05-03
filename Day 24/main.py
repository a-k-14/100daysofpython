# with open("text1.txt", mode="w") as file:
#     file.write("Hello world! \nFrom {Python}")
#     file.write("\nAnother line written to the text file with code")


with open("../../../text1.txt") as file:
    print(file.read())

