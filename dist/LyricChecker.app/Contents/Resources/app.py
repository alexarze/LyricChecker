from Tkinter import *
import func

class App:

    def __init__(self, master):

        # Initialize master
        self.master = master
        master.config(bg='pink')
        
        # Initialize the left frame for date input
        leftFrame = Frame(master)
        leftFrame.config(padx=50)
        leftFrame.pack(side=LEFT, fill=BOTH, expand=True)

        # Initialize the right frame for data display
        frame2 = Frame(master, bg='orange')
        frame2.pack(side=RIGHT, expand=True, fill=BOTH)
        
        # Interior frame within the left frame
        inputFrame = Frame(leftFrame)
        inputFrame.pack_configure(anchor=CENTER, expand=True)

        # Data input pieces
        Label(inputFrame, text="Artist:", anchor=W).pack(fill=X)

        self.artistTitleField = Entry(inputFrame, )
        self.artistTitleField.bind("<Key>", self.artistTitleChanged)
        self.artistTitleField.bind("<Return>", self.returnPressed)
        self.artistTitleField.pack(fill=X)

        Label(inputFrame, text="Album:", anchor=W).pack(fill=X)

        self.albumTitleField = Entry(inputFrame)
        self.albumTitleField.bind("<Key>", self.albumTitleChanged)
        self.albumTitleField.bind("<Return>", self.returnPressed)
        self.albumTitleField.pack(fill=X)

        # Submit button to run script
        self.submitButton = Button(inputFrame, text="Submit")
        self.submitButton.bind("<Button-1>", self.submit)
        self.submitButton.pack(side=LEFT)

        # Clear button to clear the text view
        self.clearButton = Button(inputFrame, text="Clear", command=self.clear)
        self.clearButton.pack(side=BOTTOM, anchor=W)

        # Scrollbar for text view
        self.scrollbar = Scrollbar(master)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Text view
        self.outputField = Text(
            frame2,
            relief=SUNKEN,
            state=DISABLED,
            yscrollcommand=self.scrollbar.set
            )
        self.outputField.pack(expand=True, fill=BOTH)

        self.scrollbar.config(command=self.outputField.yview)

        # configuring text tags
        self.outputField.tag_configure("EXPLICIT", foreground="red")
        self.outputField.tag_configure("CLEAN", foreground="green")
        self.outputField.tag_configure("ERROR", foreground="blue")
        self.outputField.tag_configure("NORMAL", foreground="black")
    
    def artistTitleChanged(self, event):
        return
    
    def albumTitleChanged(self, event):
        return
    
    def returnPressed(self, event):
        self.submit("")
    
    def output(self, string, color_tag="NORMAL"):
        self.outputField.config(state=NORMAL)               # set the state to normal for editing
        self.outputField.insert(END, string, color_tag)     # insert the text with color tag
        self.outputField.see(END)                           # scroll to bottom to follow text
        self.master.update_idletasks()                      # update the frame so the text is live
        self.outputField.config(state=DISABLED)             # set the state to disabled since editing is done
    
    def submit(self, event):
        if self.artistTitleField.get() != "" and self.albumTitleField.get() != "":
            func.printInfo(self, self.albumTitleField.get(), self.artistTitleField.get())
    
    def clear(self):
        self.outputField.config(state=NORMAL)
        self.outputField.delete('1.0', self.outputField.index(END))
        self.outputField.config(state=DISABLED)