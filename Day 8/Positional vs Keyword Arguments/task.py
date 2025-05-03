def calculate_love_score(name1, name2):
    check1 = ["t", "r", "u", "e"]
    check2 = ["l", "o", "v", "e"]
    count1 = 0
    count2 = 0

    for n in name1+name2:
        if n.lower() in check1:
            count1 += 1

    for n in name1+name2:
        if n.lower() in check2:
            count2 += 1

    print(f"Total {count1}{count2}")


calculate_love_score(name1="Angela Yu", name2="Jack Bauer")
calculate_love_score("Kanye West", "Kim Kardashian")