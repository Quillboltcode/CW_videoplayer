
import tkinter as tk                
from tkinter import font as tkfont  
from tkinter import scrolledtext as tkst 
import utils
import video_library as lib
from create_video_list import CreateVideoList
from update_video import UpdateVideo
from check_videos import CheckVideos

import font_manager as fonts  
class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.lib = lib.VideoLibrary(filename="library.csv")
        self.title = "root"
        
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # self.title = "The Application My Boss Wants Me To Make"
        fonts.configure()
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (VideoPlayer, CheckVideos, CreateVideoList, UpdateVideo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("VideoPlayer")

    def show_frame(self, page_name, width=10, height=10):
        '''Show a frame for the given page name
        uncomment to have the ability to resize the frame root toplevel

        :param width: width of the frame
        :param height: height of the frame

        '''
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        
        # frame.winfo_toplevel().geometry(f"{width}x{height}")
        # self.resize_frame(frame, 1080, 720)
        frame.grid()
        frame.winfo_toplevel().geometry("")
        frame.tkraise()

        

# class StartPage(tk.Frame):

class VideoPlayer(tk.Frame):
    """
    CLass video player that is the parent of the other frames in the application
    This work like a main menu 
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        self.configure(background=utils.colors["bg"],)
        # self.controller.title = "Video Player"
        # self.controller.fonts = fonts.configure()
        self.create_widgets()

    def create_widgets(self):
        self.header_label = tk.Label(self, text="Select an option",background=utils.colors["bg"],fg=utils.contrast_color(utils.colors["bg"]))
        self.header_label.grid(row=0, columnspan=3, padx=10, pady=10)

        self.status_label = tk.Label(self, font=("Helvetica", 10),background=utils.colors["bg"],fg=utils.contrast_color(utils.colors["bg"]))
        self.status_label.grid(row=2, columnspan=3, padx=10, pady=10)

        self.create_page_buttons()

    def create_button(self, text, row, column, command=None):
        button = tk.Button(self, text=text, command=command,background=utils.colors["primary"],foreground=utils.contrast_color(utils.colors["dark"]))
        button.grid(row=row, column=column, padx=10, pady=10)
        return button


    def create_page_buttons(self):
        self.create_button("Check Videos", 1, 0, lambda: self.controller.show_frame("CheckVideos"),
        )
        self.create_button("Create Video List", 1, 1, lambda: self.controller.show_frame("CreateVideoList"))
        self.create_button("Update Video", 1, 2, lambda: self.controller.show_frame("UpdateVideo"))

def start_program():
    app = App()
    return app

if __name__ == "__main__":
    start_program().mainloop()
