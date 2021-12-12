censored_words = {}

for line in Resource.Load("censored_words.txt").strip().split("\n"):
    if line.startswith("#"):
        continue
    splitted = line.split(",")
    censored_words[splitted[0]] = splitted[1]