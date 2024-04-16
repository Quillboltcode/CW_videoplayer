class LibraryItem:
    def __init__(self, name, director, rating=0, play_count=0, image_path="asset/default_image.png"):
        self.name = name
        self.director = director
        self.rating = rating
        self.play_count = 0
        self.image_path = "asset/default_image.png"
        self.custom_name = ""
        self.custom_director_name = ""

    @property
    def customer_name(self):
        return self.custom_name
    
    @customer_name.setter
    def customer_name(self, name):
        self.custom_name = name
    
    @property
    def customer_director_name(self):
        return self.custom_director_name

    @customer_director_name.setter
    def customer_director_name(self, name):
        self.custom_director_name = name

    def info(self):
        return f"{self.name} - {self.director} {self.stars()}"

    def stars(self):
        stars = ""
        for i in range(self.rating):
            stars += "*"
        return stars
    
    def clear_play_count(self):
        self.play_count = 0
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name and self.director == __value.director and self.rating == __value.rating and self.play_count == __value.play_count
    

class Episode(LibraryItem):
    def __init__(self, name, director, rating=0, image_path="asset/default_image.png",episode_number=0):
        super().__init__(name, director, image_path,rating)
        self.episode_number = episode_number

    @property
    def episode_number(self):
        return self.episode_number
    
    @episode_number.setter
    def episode_number(self, episode_number):
        self.episode_number = episode_number


if __name__ == '__main__':
    item1 = LibraryItem("The Matrix", "Wachowski", 5)
    item1eq = LibraryItem("The Matrix", "Wachowski", 5)
    item_list = [item1, item1eq]
    