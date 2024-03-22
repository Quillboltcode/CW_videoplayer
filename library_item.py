class LibraryItem:
    def __init__(self, name, director, rating=0):
        self.name = name
        self.director = director
        self.rating = rating
        self.play_count = 0

    def info(self):
        return f"{self.name} - {self.director} {self.stars()}"

    def stars(self):
        stars = ""
        for i in range(self.rating):
            stars += "*"
        return stars
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name and self.director == __value.director and self.rating == __value.rating and self.play_count == __value.play_count
    

if __name__ == '__main__':
    item1 = LibraryItem("The Matrix", "Wachowski", 5)
    item1eq = LibraryItem("The Matrix", "Wachowski", 5)
    item_list = [item1, item1eq]
    