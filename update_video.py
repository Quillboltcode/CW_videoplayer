import tkinter as tk
import font_manager as fm
import video_library as lib

class UpdateVideo:
    def __init__(self, window) -> None:
        window.title("Update Video")
        window.geometry("800x400")
        self.window = window
        
        self.init_widgets()
        self.fill_video()
        self.form_video_widget()
        
    def init_widgets(self):
        self.label = tk.Label(self.window , text="Update Video")
        self.label.grid(row=0, column=0)

        self.video_number_txt = tk.Entry(self.window, width=3)
        self.video_number_txt.grid(row=0, column=1, sticky=tk.W)

        self.video_list_info = tk.Listbox(self.window, width=40, height=10)
        self.video_list_info.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        self.video_list_info.bind("<<ListboxSelect>>", self.video_info_selected)

        self.update_btn = tk.Button(self.window, text="Update", command=self.update_video_clicked)
        self.update_btn.grid(row=2, column=0, sticky=tk.W)

    def form_video_widget(self):
        self.video_name_lbl = tk.Label(self.window, text="Video Name")
        self.video_name_lbl.grid(row=0, column=3, sticky=tk.W)

        self.video_name_txt = tk.Entry(self.window, width=30)
        self.video_name_txt.grid(row=0, column=4, sticky=tk.W)

        self.video_director_lbl = tk.Label(self.window, text="Video Director")
        self.video_director_lbl.grid(row=1, column=3, sticky=tk.W)

        self.video_director_txt = tk.Entry(self.window, width=30)
        self.video_director_txt.grid(row=1, column=4, sticky=tk.W)

        self.video_rating_lbl = tk.Label(self.window, text="Video Rating")
        self.video_rating_lbl.grid(row=2, column=3, sticky=tk.W)

        self.video_rating_txt = tk.Entry(self.window, width=30)
        self.video_rating_txt.grid(row=2, column=4, sticky=tk.W)


    def update_video_clicked(self):
        try:
            from library_item import LibraryItem
            index = self.video_number_txt.get()
            name = self.video_name_txt.get()
            director = self.video_director_txt.get()
            rating = self.video_rating_txt.get()
            video = LibraryItem(name, director, rating)
            lib.library[index] = video
        except Exception as e:
            print(e)

    @staticmethod
    def get_video_name(index):
        return lib.get_name(index), lib.get_director(index), lib.get_rating(index)
    
    @staticmethod
    def convert_int_to_string(index: int):
        return '0'+str(index+1)

    def video_info_selected(self, event):
        index = self.video_list_info.curselection()[0]

        name , director, rating = self.get_video_name(self.convert_int_to_string(index))
        self.video_name_txt.delete(0, tk.END)
        self.video_name_txt.insert(0, name)

        self.video_director_txt.delete(0, tk.END)
        self.video_director_txt.insert(0, director)

        self.video_rating_txt.delete(0, tk.END)
        self.video_rating_txt.insert(0, rating)

    def fill_video(self):
        for i in range(len(lib.library)):
            name , director, rating = self.get_video_name(self.convert_int_to_string(i))
            self.video_list_info.insert(tk.END, f"{i+1}. {name} - {director} {rating}")


if __name__ == '__main__':
    window = tk.Tk()
    fm.configure()
    UpdateVideo(window)
    window.mainloop()