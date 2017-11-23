with open(r"c:\temp\汉字_anki.txt", "w") as outF:
    for line in open(r"c:\temp\汉字.txt"):
        outF.write("%s\t\n" % line.strip())
