from library_item import LibraryItem
import os
import errno
import polars as pl
library = {}
library["01"] = LibraryItem("Tom and Jerry", "Fred Quimby", 4)
library["02"] = LibraryItem("Breakfast at Tiffany's", "Blake Edwards", 5)
library["03"] = LibraryItem("Casablanca", "Michael Curtiz", 2)
library["04"] = LibraryItem("The Sound of Music", "Robert Wise", 1)
library["05"] = LibraryItem("Gone with the Wind", "Victor Fleming", 3)

class VideoLibrary:
    def __init__(self, filename="library.csv"):
        """
        Initializes the object with an empty library dictionary.
        Tries to read from a file and populate the library if the file exists.
        If the file is not found, the library populate with default data.
        """
        self.library: dict[LibraryItem] = {}
        try:
            self.read_from_file(filename=filename)
        except FileNotFoundError as F:
            self.library = library

    def write_to_file(self, filename):
        """
        Writes the contents of the library to a file with the given filename.

        :param filename: A string representing the name of the file to write to.
        :type filename: str
        :return: None
        :rtype: None
        """

        if os.path.exists(filename):
            os.remove(filename)
        with open(filename,'w') as file:
            # add header to csv file
            file.write("key,name,director,rating,play_count,custom_name,custom_director\n")
            for key in self.library:
                item = self.library[key]
                file.write(f"{key},{item.name},{item.director},{item.rating},{item.play_count},{item.custom_name},{item.custom_director}\n")

    def read_from_file(self, filename):
        '''Read from csv file in format key, name, director, rating, play_count
        Check if file exists'''

        with open(filename,'r') as file:
            # skip header to csv file
            file.readline()
            for line in file:
                key, name, director, rating, play_count,custom_name,custom_director = line.split(',')
                self.library[str(key)] = LibraryItem(name, director, int(rating),custom_name,custom_director)

    def filter_by_name(self, query):
        """
        Filter the library by name if the query string match any name in the library item add it to the output dictionary and return it 
       
        """
        output = {}
        for _,value in self.library.items():
            if query.lower() in value.name.lower() or query.lower() in value.custom_name.lower():
                output[_] = value
            
        return output
    

    def filter_by_rating(self, rating):
        """ Any library item that has rating greater than or equal to the given rating will be added to the output dictionary and returned. """
        output = {}
        for key in self.library:
            item = self.library[key]
            if item.rating >= rating:
                output[key] = item
        return output
    
    def filter_by_play_count(self, play_count):
        """ Any library item that has play_count greater than or equal to the given play_count will be added to the output dictionary and returned. """
        output = {}
        for key in self.library:
            item = self.library[key]
            if item.play_count >= play_count:
                output[key] = item
        return output
    
    def search_by_director(self, director):
        """
        Search for library_item by director name and return a dictionary with the key as the library item key and the value as the library item object. Any director name that matches the query will be added to the output dictionary and returned.For example:
        query = "blake" will return all director with blake in the name "john blake" and "blake edwards"
        """
        output = {}
        for key in self.library:
            item = self.library[key]
            if director.lower() in item.director.lower()or director.lower() in item.custom_director.lower():
                output[key] = item
        return output
        
    def update_video(self, key, name, director, rating):
        """
        Method to allow update of video details in library given a key in the library
        Only allow to change rating, customize name and director
        """
        try:
            item = self.library[key]
            item.custom_name = name
            item.custom_director = director
            item.rating = rating
        except KeyError:
            return
        
    def change_image_path_for_item(self, key, new_path):
        """
        Set new image path to image
        To do : Check if path exists
        
        """
        try:
            item = self.library[key]
            item.image_path = new_path
        except KeyError:
            return
        
    def _write_to_play_count_file(self,filename:str,key:int,play_count:int):
        # Update play_count colunm in library.csv where key = key in library  
        df = pl.read_csv(self.filename)
        df = df.with_columns(pl.when(pl.col('key') == key).then(play_count).otherwise(pl.col('play_count')))
        df.to_csv(self.filename)
        

    def list_all(self):
        output = ""
        for key, value in self.library.items():
            output += f"{key} {value.info()}\n"
        return output


    def get_name(self,key):
        try:
            item = library[key]
            return item.name
        except KeyError:
            return None


    def get_director(self, key):
        try:
            item = self.library[key]
            return item.director
        except KeyError:
            return None


    def get_rating(self, key):
        try:
            item = self.library[key]
            return item.rating
        except KeyError:
            return -1


    def set_rating(self, key, rating):
        try:
            item = self.library[key]
            item.rating = rating
        except KeyError:
            return


    def get_play_count(self, key):
        try:
            item = self.library[key]
            return item.play_count
        except KeyError:
            return -1


    def increment_play_count(self, key):
        try:
            item = self.library[key]
            item.play_count += 1
        except KeyError:
            return
    

if __name__ == '__main__':
    print(VideoLibrary(filename='abc.csv').list_all())