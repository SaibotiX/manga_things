import pyperclip

def clip():
    tmp = pyperclip.waitForNewPaste()
    voc = " " + tmp + "\n"
    return voc

while True:
    vocabulary = clip()
    
    with open("../tools/sentences.txt", 'a') as f:
        f.write(vocabulary)

