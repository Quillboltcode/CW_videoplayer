import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import tkinter.scrolledtext as tkst
import typing as tp
from PIL import Image, ImageTk

import font_manager as fonts
import utils
import video_library as lib


class CreateVideoList(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.configure(background=utils.colors["bg"])
        self.init_widget()
        self.init_search()
        self.list_all_videos()
        self.current_playlist: list[str] = []



        
    def init_widget(self):
        # Left section consist of label and list of video
        self.list_lbl = tk.Label(self, text="Video List", bg=utils.colors["bg"], fg=utils.contrast_color(utils.colors["bg"]))
        self.list_lbl.grid(row=0, column=0, padx=20, pady=10, sticky="E")
        # List all video btn
        self.list_btn = tk.Button(self, text="List All Videos", command=self.list_all_videos, bg = utils.colors["primary"], fg=utils.contrast_color(utils.colors["primary"]))
        self.list_btn.grid(row=0, column=1, padx=20, pady=10, sticky="E")


        # List of all current video
        self.list_txt = tkst.ScrolledText(self, width=36, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=2, sticky="W", padx=10, pady=10, rowspan=3)


        # btn to add video to playlist
        add_video_btn = tk.Button(self, text="Add Video", command=self.add_video_clicked, bg = utils.colors["primary"], fg=utils.contrast_color(utils.colors["primary"]))
        add_video_btn.grid(row=4, column=3, ipadx=22,sticky="ew")

        self.status_lbl = tk.Label(self, text="", font=("Helvetica", 10), bg=utils.colors["bg"], fg=utils.contrast_color(utils.colors["bg"]))
        self.status_lbl.grid(row=5, column=0, columnspan=6, sticky="W", padx=10, pady=10)


        # play button that play all video in currnt playlist
        
        from PIL import Image, ImageTk
        image = Image.open("asset/play.png")
        image = image.resize((20,20))
        download_icon = ImageTk.PhotoImage(image)
        play_btn = tk.Button(self,          
                             text="Play",         
                             command=self.play_video_all, image=download_icon,
                             compound="left",
                             bg=utils.colors["primary"],
                             fg=utils.contrast_color(utils.colors["primary"]),
                             )
        play_btn.image = download_icon
        play_btn.grid(row=4, column=3,  ipadx=22, sticky='ew')

        # Reset btn that reset current playlist
        reset_image = Image.open("asset/reset.png")
        reset_image = reset_image.resize((20, 20))
        reset_image = ImageTk.PhotoImage(reset_image)
        reset_btn = tk.Button(self, 
                              text="Reset", command=self.reset_clicked, justify= "center" ,image=reset_image, compound="left",
                              bg=utils.colors["primary"],
                              fg=utils.contrast_color(utils.colors["primary"]),)
        reset_btn.image = reset_image
        reset_btn.grid(row=3, column=3, sticky="ew")

        # save and load playlist button
        self.save_btn = tk.Button(self, text="Save Playlist", command=self.save_playlist, bg = utils.colors["primary"], fg = utils.contrast_color(utils.colors["primary"]))
        self.save_btn.grid(row=5, column=0, ipadx=22,sticky="ew", pady=10)

        self.load_btn = tk.Button(self, text="Load Playlist", command=self.load_playlist, bg = utils.colors["primary"], fg=utils.contrast_color(utils.colors["primary"]))
        self.load_btn.grid(row=5, column=1, ipadx=22,sticky="ew",pady=10)

        # Display current playlist
        self.list_playlist_lbl = tk.Label(self, text="Playlist", bg=utils.colors["bg"], fg = utils.contrast_color(utils.colors["bg"]))
        self.list_playlist_lbl.grid(row=0, column=5, padx=10, pady=10, sticky="E")

        self.playlist_txt = tkst.ScrolledText(self, width=36, height=12, wrap="none")
        self.playlist_txt.grid(row=1, column=5, columnspan=2, sticky="W", padx=10, pady=10, rowspan=3)

        self.back_btn = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("VideoPlayer"), bg = utils.colors["warning"])
        self.back_btn.grid(row=4, column=5, ipadx=22, sticky="ew", pady=10, padx=10)

    def init_search(self):
        self.search_bar = tk.Entry(self, width=30)
        self.search_bar.grid(row=0, column=2, padx=10, pady=10, columnspan=2,sticky="W", ipadx=10)

        self.search_btn = tk.Button(self, text="Search", command=self.search_video_clicked, bg = utils.colors["primary"], fg=utils.contrast_color(utils.colors["primary"]))
        search_img  = Image.open("asset/search-removebg-preview.png")
        search_img = search_img.resize((20,20))
        search_icon = ImageTk.PhotoImage(search_img)
        self.search_btn.config(image=search_icon, compound="left")
        self.search_btn.image = search_icon
        self.search_btn.grid(row=0, column=5, ipadx=22, sticky="ew", pady=10, padx=10)
        self.search_option = tk.IntVar()
        option = {
            0: 'name',
            1: 'director',
            2: 'rating',
            3: 'play_count'
        }
        self.option_cb = ttk.Combobox(self, textvariable=self.search_option)
        self.option_cb['values'] = [i for _,i in option.items()]
        # prevent typing
        self.option_cb['state'] = 'readonly'
        self.option_cb.grid(row=1, column=3, ipadx=22, sticky="ew", pady=10, padx=10)

    def search_video_clicked(self):
        # get option from search bar
        option = self.search_option.get()
        match option:
            case 'name':
                video_list = self.controller.lib.filter_by_name(self.search_bar.get())
                self.list_txt.delete("1.0", tk.END)
                self.list_txt.insert(tk.END, video_list)
            case 'director':
                video_list = self.controller.lib.filter_by_director(self.search_bar.get())
                self.list_txt.delete("1.0", tk.END)
                self.list_txt.insert(tk.END, video_list)
            case 'rating':
                video_list = self.controller.lib.filter_by_rating(self.search_bar.get())
                self.list_txt.delete("1.0", tk.END)
                self.list_txt.insert(tk.END, video_list)
            case 'play_count':
                video_list = self.controller.lib.filter_by_play_count(self.search_bar.get())
                self.list_txt.delete("1.0", tk.END)
                self.list_txt.insert(tk.END, video_list)

    def list_all_videos(self):
        video_list = self.controller.lib.list_all()
        # set_text(self.list_txt, video_list)
        self.list_txt.delete("1.0", tk.END)
        self.list_txt.insert(tk.END, video_list)
        # self.playlist_txt.insert(tk.END, video_list)

    def save_playlist(self):
        with open("playlist.txt", "w") as f:
            f.write("\n".join(self.current_playlist))
        self.status_lbl.config(text="Playlist saved")

    def load_playlist(self):
        fd = filedialog.askopenfile(mode="r", filetypes=[("Text Files", "*.txt")])
        if fd is None:
            self.status_lbl.config(text="No playlist to load")
            return
        self.current_playlist = fd.read().split()
        self.list_videos_clicked()
        self.status_lbl.config(text="Playlist loaded")



    def add_video_clicked(self):
        video_num = self.video_num_txt.get()
        if  not video_num.isnumeric():
            self.status_lbl.config(text="Wrong input type, please input a number")
            return
        elif int(video_num) > len(lib.library):
            self.status_lbl.config(text="Invalid video number")
            return
        elif int(video_num) <= 0:
            self.status_lbl.config(text="Invalid video number")
            return
        elif video_num in self.current_playlist:
            self.status_lbl.config(text="Video already in playlist")
            return
        else:
            self.current_playlist.append(video_num)
            self.status_lbl.config(text="Video added to playlist")
            self.list_videos_clicked()
    
    def get_info(self, key) -> str:
        """
        returna string of all info of video: name, director,  rating, play_count
        """
        name = self.controller.lib.get_name(key)
        director = self.controller.lib.get_director(key)
        rating = self.controller.lib.get_rating(key)
        play_count = self.controller.lib.get_play_count(key)
        return f"{name} ,{director} ,{rating} ,play times{play_count}"

    def list_videos_clicked(self):
        """
        Retrieves the information of each video in the current playlist and displays it in the playlist text widget.

        Parameters:
            self (object): The instance of the class.
        
        Returns:
            None
        """
        output = ""
        try:
            for key in self.current_playlist:
                output += f"{self.get_info(key)}\n"
        except Exception as e:
            output = f"No playlist to show, {e}"
        utils.set_text(self.playlist_txt, output)

    def play_video_all(self):
        """
        Plays all the videos in the current playlist.

        This function iterates over the keys in the current playlist and checks if each key is present in the library. If a key is not found in the library, an error message is displayed. If a key is found, the play count for that video is incremented. After iterating over all the keys, a success message is displayed and the list of videos is updated.

        Parameters:
        - None

        Returns:
        - None
        """
        if self.current_playlist is None:
            self.status_lbl.config(text="No playlist to play")
            return

        for key in self.current_playlist:
            if key not in lib.library:
                self.status_lbl.config(text=f"Invalid video number {key}")
                continue

            self.controller.lib.increment_play_count(key)

        self.status_lbl.config(text="Playlist played")
        self.list_videos_clicked()
    
    def reset_clicked(self):

        self.current_playlist.clear()
        self.list_videos_clicked()
        self.status_lbl.config(text="Playlist reset")

        # self.status_lbl.config(text=f"No playlist to reset , {e}")
    def write_playlist_clicked(self) -> None:
        """
        Write current playlist to playlist.txt file.

        This function does not take any arguments.
        It does not return anything.
        """
        # Check if current playlist is not empty
        if not self.current_playlist:
            self.status_lbl.config(text="Playlist is empty, nothing to write")
            return
        
        try:
            with open("playlist.txt", "w") as f:
                f.write("\n".join(self.current_playlist))  # type: ignore
        except IOError as e:
            self.status_lbl.config(text=f"Error writing playlist to file: {e}")
        else:
            self.status_lbl.config(text="Playlist written to file")

if __name__ == '__main__':
    window = tk.Tk()
    fonts.configure()
    CreateVideoList(window)
    window.mainloop()