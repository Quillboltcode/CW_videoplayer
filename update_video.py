from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from video_player import App
import tkinter as tk
# from video_player import App, VideoPlayer
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import font_manager as fm
import video_library as lib
from tkinter import ttk
import utils

class UpdateVideo(tk.Frame):
    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)
        self.controller: App = controller
        self.set_up()
        self.init_widgets()
        self._fill_video()
        self.form_video_widget()
        
    def set_up(self):
        """
        Set window name to UpdateVideo
        """
        # self.controller.title("UpdateVideo")
        self.configure(bg=utils.colors["bg"])
        
    def init_widgets(self):
        self.video_list_info = tk.Listbox(self, width=36, height=10, selectforeground=utils.colors['selectfg'],activestyle='underline')
        self.video_list_info.grid(row=1, column=0, sticky=tk.W, rowspan=4, columnspan=2)
        self.video_list_info.bind("<<ListboxSelect>>", self.video_info_selected)

        self.update_btn = tk.Button(self, text="Confirm", command=self.update_video_clicked, bg= utils.colors["secondary"],fg=utils.contrast_color(utils.colors["secondary"]))
        self.update_btn.grid(row=4, column=4, padx=10, sticky=tk.W)

        self.create_btn = tk.Button(self, text="Create", command=self.create_video_clicked, bg = utils.colors["secondary"],fg=utils.contrast_color(utils.colors["secondary"]))
        self.create_btn.grid(row=4, column=3, padx=10, sticky=tk.W)

        self.back_btn = tk.Button(self, text="Back", command=lambda : self.controller.show_frame("VideoPlayer"), bg= utils.colors["warning"])
        self.back_btn.grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)

        self.open_image_btn = tk.Button(self, text="Change Image", command=self.open_image_clicked, bg= utils.colors["warning"])
        self.open_image_btn.grid(row=4, column=2, sticky=tk.W, padx=10, pady=10)

    def _fill_video(self):
        self.video_list_info.delete(0, tk.END)
        for i in range(len(lib.library)):
            name , director, rating = self.get_video_name(self.convert_int_to_string(i))
            # self.video_list_info.delete(0, tk.END)
            self.video_list_info.insert(tk.END, f"{i+1}. {name} - {director} {rating}")

    def form_video_widget(self, bg=utils.colors["bg"]):
        self.label = tk.Label(self, text="Video list", bg=bg, fg=utils.contrast_color(bg))
        self.label.grid(row=0, column=0)

        self.video_name_lbl = tk.Label(self, text="Video Name", bg=bg, fg=utils.contrast_color(bg))
        self.video_name_lbl.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)

        self.video_director_lbl = tk.Label(self, text="Video Director", bg=bg, fg = utils.contrast_color(bg))
        self.video_director_lbl.grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)

        self.video_rating_lbl = tk.Label(self, text="Video Rating", bg=bg, fg=utils.contrast_color(bg))
        self.video_rating_lbl.grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)

        self.video_name_txt = tk.Entry(self)
        self.video_name_txt.grid(row=1, column=3, columnspan=2, sticky=tk.E)

        self.video_director_txt = tk.Entry(self)
        self.video_director_txt.grid(row=2, column=3, columnspan=2, sticky=tk.E)

        self.video_rating_txt = tk.Entry(self)
        self.video_rating_txt.grid(row=3, column=3, columnspan=2, sticky=tk.E)

        self.image_frame = tk.Label(self, text="Image", bg=bg, fg=utils.contrast_color(bg))
        self.image_frame.grid(row=5, column=1, columnspan=2, sticky=tk.E, padx=10, pady=10)

    def update_video_clicked(self):
        """
        Update a video info in video_library.library
        Can only change video name, director and rating
        """
        # from library_item import LibraryItem
        index = self.video_list_info.curselection()[0]
        name = self.video_name_txt.get()
        director = self.video_director_txt.get()
        rating = self.video_rating_txt.get()
        # video = LibraryItem(name, director, rating)
        lib.VideoLibrary().update_video(self.convert_int_to_string(index), name, director, rating)
        self._fill_video()

    @staticmethod
    def get_video_name(index):
        """
        Returns the name, director, and rating of a video at the specified index in the video library.

        :param index: An integer representing the index of the video in the video library.
        :type index: int
        :return: A tuple containing the name, director, and rating of the video at the specified index.
        :rtype: tuple
        """
        return lib.VideoLibrary().get_name(index), lib.VideoLibrary().get_director(index), lib.VideoLibrary().get_rating(index)

    
    @staticmethod
    def convert_int_to_string(index: int):
        """
        Converts an integer to a string by appending a '0' to it and returning the resulting string.

        Parameters:
            index (int): The integer to be converted to a string.

        Returns:
            str: The resulting string after converting the integer.
        """
        return '0'+str(index+1)

    def video_info_selected(self, event):
        """
        Updates the video information displayed in the GUI when a video is selected from the list.

        Parameters:
            event (Event): The event object representing the selection event.

        Returns:
            None
        """
        index = self.video_list_info.curselection()[0]

        name , director, rating = self.get_video_name(self.convert_int_to_string(index))

        self.video_name_txt.delete(0, tk.END)
        self.video_name_txt.insert(0, name)

        self.video_director_txt.delete(0, tk.END)
        self.video_director_txt.insert(0, director)

        self.video_rating_txt.delete(0, tk.END)
        self.video_rating_txt.insert(0, rating)
            
    def open_image_clicked(self):
        """
        Open a dialog box to select an image file and update the video library with the selected image.
        Add image validation: Check if the selected file is a valid image file.
        Add feature to preview image in new window: Display the selected image in a new window.
        To do: Check if any Library Item has been selected then allow update image, else error message
        """
        supported_formats = ['.jpg', '.jpeg', '.png']
        selected_index = self.video_list_info.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a Library Item")
            return
        else:
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
            if file_path:
                if not self._is_supported_image(file_path, supported_formats):
                    messagebox.showerror("Error", "Please select a valid image file.")
                    return

                selected_index = selected_index[0]
                selected_key = self.convert_int_to_string(selected_index)
                self.controller.lib.change_image_path_for_item(selected_key, file_path)
                self._fill_video()
                self._preview_image(file_path)
 

    @staticmethod
    def _is_supported_image(file_path, supported_formats):
        return file_path.lower().endswith(tuple(supported_formats))

    def _preview_image(self, file_path):
        """Put the image into frame"""
        pil_img = Image.open(file_path)
        resized_img = pil_img.resize((400, 225), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized_img)
        # Resize the image before display

        self.image_frame.configure(image=img)
        self.image_frame.image = img


    def create_video_clicked(self):
        """
        Allow create new video in video_library.library = {key:str, value: LibraryItem}
        TO DO: 
        - Add new video to library
        - Check if video exists in library
        - Update video_list
        """
        from library_item import LibraryItem
        name = self.video_name_txt.get()
        director = self.video_director_txt.get()
        rating = self.video_rating_txt.get()
        video = LibraryItem(name, director, rating)

        key = name.lower() # Use lower case name as key

        if key in lib.library: # Check if video exists in library
            messagebox.showwarning('Video already exists', f'Video "{name}" already exists')
            return

        lib.library[key] = video # Add new video to library
        self._fill_video() # Update video_list
        



if __name__ == '__main__':
    window = tk.Tk()
    fm.configure()
    UpdateVideo(window,window)
    window.mainloop()