import tkinter as tk
from tkinter import ttk
import typing as tp
import tkinter.scrolledtext as tkst
from check_videos import set_text

import font_manager as fonts
import video_library as lib
import library_item as lib_item

class CreateVideoList:
    def __init__(self, window):
        # self.window = window
        window.geometry("1080x500")
        window.title("Create Video PlayList")
        self.init_widget(window)
        self.list_all_videos()
        self.current_playlist: tp.List[str] = []

        # self.list_videos_clicked() ???

        
    def init_widget(self, window):
        # Left section consist of label and list of video
        self.list_lbl = tk.Label(window, text="Video List")
        self.list_lbl.grid(row=0, column=0, padx=10, pady=10)

        # List of all current video
        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        # input of video number
        video_num_lbl = tk.Label(window, text="Video Number")
        video_num_lbl.grid(row=0, column=3, padx=10, pady=10)

        self.video_num_txt = tk.Entry(window, width=3)
        self.video_num_txt.grid(row=0, column=4, padx=10, pady=10)

        # btn to add video to playlist
        add_video_btn = tk.Button(window, text="Add Video", command=self.add_video_clicked)
        add_video_btn.grid(row=1, column=3, padx=10, pady=10)

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=6, sticky="W", padx=10, pady=10)


        # play button that play all video in currnt playlist
        play_btn = tk.Button(window, text="Play", command=self.play_video_all)
        play_btn.grid(row=3, column=3, padx=10, pady=10)

        # Reset btn that reset current playlist
        reset_btn = tk.Button(window, text="Reset", command=self.reset_clicked)
        reset_btn.grid(row=3, column=4, padx=10, pady=10)

        # Display current playlist
        self.list_playlist_lbl = tk.Label(window, text="Playlist")
        self.list_playlist_lbl.grid(row=0, column=5, padx=10, pady=10)

        self.playlist_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.playlist_txt.grid(row=1, column=5, columnspan=3, sticky="W", padx=10, pady=10)

        
    def list_all_videos(self):
        video_list = lib.list_all()
        # set_text(self.list_txt, video_list)
        self.list_txt.insert(tk.END, video_list)
        # self.playlist_txt.insert(tk.END, video_list)


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
        return f"{lib.library[key].name} by {lib.library[key].director} {lib.library[key].stars()} {lib.library[key].play_count} times"

    def list_videos_clicked(self):
        output = ""
        try:
            for key in self.current_playlist:
                output += f"{self.get_info(key)}\n"
        except Exception as e:
            output = f"No playlist to show, {e}"
        set_text(self.playlist_txt, output)

    def play_video_all(self):
        for key in self.current_playlist:
            lib.increment_play_count(key)
        self.status_lbl.config(text="Playlist played")
        self.list_videos_clicked()
    
    def reset_clicked(self):

        self.current_playlist.clear()
        self.list_videos_clicked()
        self.status_lbl.config(text="Playlist reset")

        # self.status_lbl.config(text=f"No playlist to reset , {e}")


if __name__ == '__main__':
    window = tk.Tk()
    fonts.configure()
    CreateVideoList(window)
    window.mainloop()