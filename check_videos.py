import tkinter as tk
import tkinter.scrolledtext as tkst


import video_library as lib
import font_manager as fonts
import utils


class CheckVideos(tk.Frame):
    def __init__(self, parent, controller):
        """
        Contruct a tk.Frame object as child of parent tk.Tk object
        :param parent: parent tk.Tk object
        :param controller: tk.Tk object that is the parent of this frame

        """
        tk.Frame.__init__(self, parent)
        self.controller: tk.Tk = controller
        self.configure(background=utils.colors["bg"])
        self.create_widgets()
        self.list_videos_clicked()
        

    def create_widgets(self):
        """
        Create the widgets for this frame
        """
        list_videos_btn = tk.Button(
            self,
            text="List All Videos",
            command=self.list_videos_clicked,
            bg=utils.colors["primary"],
            fg=utils.contrast_color(utils.colors["primary"]),
        )
        list_videos_btn.grid(row=0, column=0, padx=10, pady=10)

        enter_lbl = tk.Label(self, text="Enter Video Number",bg=utils.colors["bg"],fg=utils.contrast_color(utils.colors["bg"]))
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)

        self.input_txt = tk.Entry(self, width=3)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)

        check_video_btn = tk.Button(
            self,
            text="Check Video",
            command=self.check_video_clicked,
            bg=utils.colors["primary"],
            fg=utils.contrast_color(utils.colors["primary"]),
        )
        check_video_btn.grid(row=0, column=3, padx=10, pady=10)

        self.list_txt = tkst.ScrolledText(self, width=48, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        self.video_txt = tk.Text(self, width=24, height=4, wrap="none")
        self.video_txt.grid(
            row=1, column=3, columnspan=2, sticky="NW", padx=10, pady=10
        )

        self.status_lbl = tk.Label(self, text="", font=("Helvetica", 10),bg=utils.colors["bg"],fg=utils.contrast_color(utils.colors["bg"]))
        self.status_lbl.grid(
            row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10
        )
        # When press the button "Back" change the frame to "VideoPlayer" and destroy ImageFrame
        self.back_btn = tk.Button(
            self, text="Back", command=lambda: [self.controller.show_frame("VideoPlayer"), self.image_frame.destroy()], bg=utils.colors["primary"], fg=utils.contrast_color(utils.colors["primary"]), 
        )
        self.back_btn.grid(row=0, column=4, sticky="NW", padx=10, pady=10)

        self.image_frame = ImageFrame()
        self.image_frame.pack()


    def check_video_clicked(self):
        """
        When the user clicks the "Check Video" button, this method will be called to display the video details
        """
        key = self.input_txt.get()
        name = lib.VideoLibrary().get_name(key)
        if name is not None:  # check if the video exists
            director = self.controller.lib.get_director(key)
            rating = lib.VideoLibrary().get_rating(key)
            play_count = lib.VideoLibrary().get_play_count(key)
            video_details = f"{name}\n{director}\nrating: {rating}\nplays: {play_count}"
            utils.set_text(self.video_txt, video_details)
            self.image_frame.set_image()
        else:
            utils.set_text(self.video_txt, f"Video {key} not found")
        self.status_lbl.configure(text="Check Video button was clicked!")

    def list_videos_clicked(self) -> None:
        """
        This method will be called when the user clicks the "List Videos" button
        This method also run when the GUI is first launched
        """
        video_list = lib.VideoLibrary().list_all()  # list all the videos
        utils.set_text(self.list_txt, video_list)  # Set the text in the list widget
        self.status_lbl.configure(
            text="List Videos button was clicked!"
        )  # Set the status label


class ImageFrame(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.img = tk.PhotoImage(file="asset/default_image.png")
        self.img = self.img.subsample(4, 4)
        self.label = tk.Label(self, image=self.img)
        # self.label.grid(row=0, column=0)

    def set_image(self):
        self.label.grid(row=0,column=0)
        # self.label.configure(image=self.img)
        

    def destroy(self) -> None:
        return super().destroy()

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()  # create a TK object
    fonts.configure()  # configure the fonts
    CheckVideos(window, window)  # open the CheckVideo GUI
    window.mainloop()  # run the window main loop, reacting to button presses, etc
