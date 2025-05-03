alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def caesar(mode, user_message, shift_amount):
    updated_text = ""
    message = ""

    if mode.lower() == "decode":
        shift_amount = -shift_amount
        message = "decoded"
    elif mode.lower() == "encrypt":
        message = "encoded"

    for n in user_message:
        if n not in alphabet:
            updated_text += n
        else:
            old_index = alphabet.index(n.lower())
            new_index = (old_index + shift_amount) % len(alphabet)
            updated_text += alphabet[new_index]

    print(f"Here's the {message} result: {updated_text}")

# TODO-2: Inside the 'encrypt()' function, shift each letter of the 'original_text' forwards in the alphabet
#  by the shift amount and print the encrypted text.

# TODO-4: What happens if you try to shift z forwards by 9? Can you fix the code?

# TODO-3: Call the 'encrypt()' function and pass in the user inputs. You should be able to test the code and encrypt a
#  message.

to_continue = True

while to_continue:
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
    if direction.lower() != "encode" and direction.lower() != "decode":
        print("Invalid option!")
        break
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))

    caesar(direction.lower(), text, shift)

    repeat = input("Type 'yes' if you want to go again. Otherwise type 'no'.\n")
    if repeat.lower() == "no":
        to_continue = False