# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

import tkinter as tk
from tkinter import *


LARGE_FONT= ("Verdana", 12)


class Chatter(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Chatter | Instant Messaging")
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, NewUser, ExistingUser, FriendsList, Chat):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        button = tk.Button(self, text="New User", font=LARGE_FONT,
                            command=lambda: controller.show_frame(NewUser))
        button.pack(fill=X)

        button2 = tk.Button(self, text="Existing User", font=LARGE_FONT,
                            command=lambda: controller.show_frame(ExistingUser))
        button2.pack(fill=X)


class NewUser(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        rad2 = Radiobutton(self, text='Existing User', value=1,
                           command=lambda: controller.show_frame(ExistingUser))
        rad1 = Radiobutton(self, text='New User', value=2)
        rad1.grid(column=0, row=0)
        rad2.grid(column=1, row=0)

        userlbl = Label(self, text="Username") 
        userlbl.grid(column=0, row=2) 
        usertxt = Entry(self,width=15)
        usertxt.grid(column=1, row=2)

        passlbl = Label(self, text="Password")
        passlbl.grid(column=0, row=3) 
        passtxt = Entry(self, width=15)
        passtxt.grid(column=1, row=3)

        pass2lbl = Label(self, text="Confirm")
        pass2lbl.grid(column=0, row=4) 
        pass2txt = Entry(self, width=15)
        pass2txt.grid(column=1, row=4)

        firstNamelbl = Label(self, text="First Name")
        firstNamelbl.grid(column=0, row=5) 
        firstName = Entry(self,width=15)
        firstName.grid(column=1, row=5)

        lastNamelbl = Label(self, text="Last Name")
        lastNamelbl.grid(column=0, row=6) 
        lastName = Entry(self,width=15)
        lastName.grid(column=1, row=6)

        addresslbl = Label(self, text="Address")
        addresslbl.grid(column=0, row=7) 
        address = Entry(self,width=15)
        address.grid(column=1, row=7)

        emaillbl = Label(self, text="Email")
        emaillbl.grid(column=0, row=8) 
        email = Entry(self,width=15)
        email.grid(column=1, row=8)

        def createClicked():
            print("account")
            controller.show_frame(FriendsList)

        btn = Button(self, text="Create Account", command=createClicked) 
        btn.grid(column=1, row=9)

        #button1 = tk.Button(self, text="Back to Home",
        #                    command=lambda: controller.show_frame(StartPage))
        #button1.pack()

        #button2 = tk.Button(self, text="Existing User",
        #                    command=lambda: controller.show_frame(ExistingUser))
        #button2.pack()


class ExistingUser(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        rad1 = Radiobutton(self, text='New User', value=2,
                           command=lambda: controller.show_frame(NewUser))
        rad1.grid(column=0, row=0)
        rad2 = Radiobutton(self, text='Existing User', value=1)
        rad2.grid(column=1, row=0)

        userlbl = Label(self, text="Username") 
        userlbl.grid(column=0, row=2) 
        usertxt = Entry(self,width=15)
        usertxt.grid(column=1, row=2)

        passlbl = Label(self, text="Password")
        passlbl.grid(column=0, row=3) 
        passtxt = Entry(self, width=15)
        passtxt.grid(column=1, row=3)

        def loginClicked():
            print("login")
            controller.show_frame(FriendsList)

        btn = Button(self, text="Login", command=loginClicked) 
        btn.grid(column=1, row=9)        

class FriendsList(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = Label(self, text="Friends List", font = LARGE_FONT)
        label.pack(side=TOP)

        fList = Listbox(self, selectmode = EXTENDED)
        fList.insert(END, "Dawn")
        fList.insert(END, "Derek")
        fList.pack(side=TOP)

        def chatClicked():
            controller.show_frame(Chat)

        def deleteClicked():
            selected = fList.curselection()
            for i in reversed(selected):
                fList.delete(i)

        chatBtn = Button(self, text="Chat", command=chatClicked) 
        chatBtn.pack()

        delBtn = Button(self, text="Delete", command=deleteClicked) 
        delBtn.pack() 

        
class Chat(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        text = Text(self, height=15, width=50)
        text.grid(column=0, row=0)

        entry = Entry(self,width = 50)
        entry.grid(column=0, row=1)

        def sendClicked():
            print("Send")
            
        sendBtn = Button(self, text = "Send", command=sendClicked)
        sendBtn.grid(column=0, row=2)


#root = Chatter()
#root.geometry("400x300")

Chatter().geometry("400x300").mainloop()

