import json
import keyboard

running = True

def on_hotkey():
    global running
    running = False

# Register the hotkey
keyboard.add_hotkey('ctrl+shift+a', on_hotkey)

# Your forever loop
count = 0
while running:
    # Your code here
    count = count + 1

# Clean up


#def verify_data(data):
#    for data_instance in data:
#        if data_instance.get("Verify") == "N":
#            print("Verify: ")
#            print(json.dumps(data_instance, indent=4))
#
#            user_input = input("(C)orrect or (D)elete: ")
#
#            if user_input.upper() == "C":
#                data_instance["Verify"] = "Y"
#            else:
#                data.remove(data_instance)
#                
#    return data
#
#dict1 =[{"Probe1" : 1,
#         'Verify':'N'},
#        {"Probe2" : 2,
#         'Verify':'Y'},
#        {"Probe3" : 3,
#        'Verify':'N'}]
#
#test = json.dumps(dict1, indent=4)
#print('test', test)
#
#dict1 = verify_data(dict1)
#print(json.dumps(dict1, indent=4))
#
