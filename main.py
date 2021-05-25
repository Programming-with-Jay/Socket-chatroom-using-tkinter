# Importing the modules

from tkinter import *
from tkinter.font import BOLD
import socket
import threading
import random
import csv
import pygame

r = lambda: random.randint(0, 255)
color = '#%02X%02X%02X' % (r(), r(), r())
# client connections
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

# Create a new client socket and connect to the server
client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
client.connect(ADDRESS)


# making the GUI
class GUI:
    """
    <summary>
    This is the main class fot the GUI.
    </summary>

    <functions>
    continue_ahead()
    chatroom()
    send_button()
    message_from_server()
    message_to_server()
    update_database()
    play_sound()
    setting_window()
    change_color_window()
    </functions>
    """
    def __init__(self):
        """
        <summary>
        Main Constructor.
        </summary>

        <param>
        ***No params***
        </param>
        """
        self.root = Tk()
        self.root.withdraw()
        self.sign_up = Toplevel()
        self.sign_up.geometry('300x300')
        self.please_detials = Label(self.sign_up,
                                    text="Please sign_up to continue",
                                    font=('Arial', 8, BOLD))
        self.please_detials.place(x=90, y=100)
        self.name_label = Label(self.sign_up,
                                text="Name: ",
                                font=('Arial', 8, BOLD))
        self.name_label.place(x=50, y=130)
        self.input_box = Entry(self.sign_up,
                               highlightthickness=2)
        self.input_box.place(x=100, y=130)
        self.input_box.focus()
        self.continue_button = Button(self.sign_up,
                                      text="Continue",
                                      height=2,
                                      width=10,
                                      bg='grey',
                                      fg='white',
                                      command=lambda: self.continue_ahead(self.input_box.get()))
        self.continue_button.place(relx=0.4, rely=0.55)
        self.root.mainloop()

    def continue_ahead(self, name):
        """
        <summary>
        its the main login controller.
        </summary>
        :param name: takes the name to display on function CHATROOM.
        :return: Null
        """
        self.sign_up.destroy()
        self.chatroom(name)

        recieve = threading.Thread(target=self.message_from_server)
        recieve.start()

    def chatroom(self, name):
        """
        <summary>
        This is the main function for the chatroom that will
        control the chat and will display some buttons and chat fields.
        </summary>
        :param name: takes the name to display on the top.
        :return: Null
        """
        self.user_name = name
        self.root.deiconify()
        self.root.geometry('470x550')
        self.root.configure(bg=color)
        self.root.title('CHATROOM')
        self.heading = Label(self.root,
                             text=self.user_name,
                             bg=color,
                             fg="#EAECEE",
                             font="Helvetica 13 bold",
                             pady=5)
        self.heading.pack()
        self.photo = PhotoImage(file=r"assets/black-settings-button.png")
        self.settings_button = Button(self.root, image=self.photo, pady=5, command=self.setting_window)
        self.settings_button.place(relx=0.9, rely=0.02)
        self.space_for_message = Text(self.root,
                                      width=20,
                                      height=2,
                                      bg="#17202A",
                                      fg="#EAECEE",
                                      font="Helvetica 14",
                                      padx=5,
                                      pady=5)
        self.space_for_message.place(relheight=0.745,
                                     relwidth=1,
                                     rely=0.08)
        self.bottom_design = Label(self.root,
                                   bg="#ABB2B9",
                                   height=40)
        self.bottom_design.place(relwidth=1,
                                 rely=0.925)
        self.message_input = Entry(self.bottom_design,
                                   bg="#616A6B",
                                   fg="#000000",
                                   font="Helvetica 13")
        self.message_input.place(relwidth=0.74,
                                 relheight=0.04,
                                 rely=0.008,
                                 relx=0.011)
        self.message_input.focus()
        self.send_button = Button(self.bottom_design,
                                  text="Send",
                                  font="Helvetica 10 bold",
                                  width=20, bg="#ABB2B9",
                                  command=lambda: self.sendButton(self.message_input.get()))
        self.send_button.place(relx=0.77,
                               rely=0.008,
                               relheight=0.04,
                               relwidth=0.22)
        self.scrollbar = Scrollbar(self.space_for_message)
        self.scrollbar.place(relheight=1,
                             relx=0.974)
        self.scrollbar.config(command=self.space_for_message.yview)
        self.space_for_message.config(state=DISABLED)

    def sendButton(self, msg):
        """
        <summary>
        This function consist of the send button and its code.
        </summary>
        :param msg: the string written by the user on the text field of the chatroom.
        :return: None
        """
        self.space_for_message.config(state=DISABLED)
        self.msg = msg
        self.message_input.delete(0, END)
        self.update_database()
        self.snd = threading.Thread(target=self.message_to_server)
        self.snd.start()

    def message_from_server(self):
        """
        <summary>
        it decodes the string from the server.
        </summary>
        :return:None
        """
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == 'NAME':
                    client.send(self.user_name.encode(FORMAT))
                else:
                    self.play_sound()
                    self.space_for_message.config(state=NORMAL)
                    self.space_for_message.insert(END, message + "\n\n")
                    self.space_for_message.config(state=DISABLED)
                    self.space_for_message.see(END)


            except:
                print("An error has occured from the server.")
                client.close()
                break

    def message_to_server(self):
        """
        <summary>
        it decodes the messages to server.
        </summary>
        :return: None
        """
        self.space_for_message.config(state=DISABLED)
        while True:
            message = (f"{self.user_name}: {self.msg}")
            client.send(message.encode(FORMAT))
            break


    def update_database(self):
        """
        <summary>
        it updates the database or the data to a .txt file and saves the message.
        </summary>
        :return: None
        """
        try:
            rowlist = [[self.user_name, self.msg]]
            with open('database.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rowlist)
                self.play_sound()
        except:
            print("Error occured in database ")

    def play_sound(self):
        """
        <summary>
        it plays a sound when a message is sent or received.
        :return: None
        """
        pygame.mixer.init()
        crash_sound = pygame.mixer.Sound("assets/insight-578.mp3")
        crash_sound.play()

    def setting_window(self):

        self.settings = Tk()
        self.settings.geometry('250x250')
        Label(self.settings, text="COLOR").pack()
        self.color_black = Button(self.settings, bg='black', width=5, height=2,
                                  command=lambda: self.change_color_window('black'))
        self.color_black.place(rely=0.1)
        self.color_white = Button(self.settings, bg='white', width=5, height=2,
                                  command=lambda: self.change_color_window('white'))
        self.color_white.place(rely=0.3)
        self.color_red = Button(self.settings, bg='red', width=5, height=2,
                                command=lambda: self.change_color_window('red'))
        self.color_red.place(rely=0.5)
        self.color_orange = Button(self.settings, bg='orange', width=5, height=2,
                                   command=lambda: self.change_color_window('orange'))
        self.color_orange.place(relx=0.2, rely=0.1)
        self.color_blue = Button(self.settings, bg='blue', width=5, height=2,
                                 command=lambda: self.change_color_window('blue'))
        self.color_blue.place(relx=0.2, rely=0.3)
        self.color_yellow = Button(self.settings, bg='yellow', width=5, height=2,
                                   command=lambda: self.change_color_window('yellow'))
        self.color_yellow.place(relx=0.2, rely=0.5)
        self.color_unknown = Button(self.settings, bg='#58D68D', width=5, height=2,
                                    command=lambda: self.change_color_window('#58D68D'))
        self.color_unknown.place(relx=0.4, rely=0.1)
        self.color_unknown2 = Button(self.settings, bg='#A569BD', width=5, height=2,
                                     command=lambda: self.change_color_window('#A569BD'))
        self.color_unknown2.place(relx=0.4, rely=0.3)
        self.color_unknown3 = Button(
            self.settings,
            bg='#D35400',
            width=5,
            height=2,
            command=lambda: self.change_color_window('#D35400'))
        self.color_unknown3.place(relx=0.4, rely=0.5)

    def change_color_window(self, color):
        self.root.configure(bg=color)
        self.heading.configure(bg=color)


g = GUI()

