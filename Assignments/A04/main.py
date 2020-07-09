#Landen Jones
#07/09/2020
import tkinter as tk
import sys
import os
import json

# GUI window is a subclass of the basic tkinter Frame object
class MainFrame(tk.Frame):
    def __init__(self, master):
        # Call superclass constructor
        tk.Frame.__init__(self, master)
        # Place frame into main window
        self.grid()        
        
        #Get the name of the JsonFile
        jsonFile = sys.argv[1]

        #Checks to see if the file is available
        if os.path.isfile(jsonFile):
            infile = open(jsonFile, "r")
            data = infile.read()
            infile.close
        else:
            print("Error: File doesn't exist!")
        #Loads data into a dictionary from Json data
        playerInfo = json.loads(data)

        #J is the value of the row to be printed on
        j = 0
        #For loop to traverse each dictionary pair and we print to window :)
        for key, value in playerInfo.items():
            #Skip the Screen_Name b/c it is only useful for the window name
            if key != "screen_name":
                result = str(key).ljust(15)
                text = tk.Label(self, text= result, justify= tk.LEFT, anchor="w").grid(sticky = tk.W, column=0,row=j)
                result = ":   " + str(value).strip("[]")
                result = result.replace("'","")
                text = tk.Label(self, text= result, justify= tk.LEFT, anchor="w").grid(sticky = tk.W, column=25,row=j)
                j+=1

# Spawn window
if __name__ == "__main__":

    #--------------------------------------
    #All of this is to just get the screen title b/c I don't know how to pass the variable before I call MainFrame
    jsonFile = sys.argv[1]
    if os.path.isfile(jsonFile):
        infile = open(jsonFile, "r")
        data = infile.read()
        infile.close
    else:
        print("Error: File doesn't exist!")
    playerData = json.loads(data)
    title = "Player: " + playerData["screen_name"]
    #--------------------------------------

    
    # Create main window object
    root = tk.Tk()
    # Set title of window
    root.title(f"{title}")
    # Instantiate HelloWorldFrame object
    display = MainFrame(root)
    # Start GUI
    display.mainloop()
