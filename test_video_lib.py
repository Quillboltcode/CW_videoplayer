import pytest
import video_library as lib
from library_item import LibraryItem
import utils

def test_eq_librabry_item():
    """
    Need this to work before other test could run
    """
    item1 = LibraryItem("The Matrix", "Wachowski", 5)
    item1eq = LibraryItem("The Matrix", "Wachowski", 5)
    # item_list = [item1, item1eq]

    assert item1 == item1eq


class TestVideoLibrary:
    def test_init(self):
        """
        Test if the library cannot read from a file
        """
        
        with pytest.raises(FileNotFoundError):
            lib.VideoLibrary(filename='abc.csv')

    def test_database(self):
        """
        Test if the library is initialized with the correct data
        """
        test_lib_init = lib.VideoLibrary(filename="library.csv")
        test_dict = {}
        with open("library.csv", "r") as f:
            f.readline()
            for line in f:
                key, name, director, rating, play_count = line.split(",")
                test_dict[key] = LibraryItem(name, director, int(rating))
        assert test_lib_init.library == test_dict

    def test_update_video(self):
        test_lib_init = lib.VideoLibrary()
        test_lib_init.update_video("01", "The Matrix", "Wachowski", 5)
        assert test_lib_init.library["01"] == LibraryItem("The Matrix", "Wachowski", 5)


class TestSearch:
    """
    Searching test require a test file csv file with name, director, rating, play_count
    """
   
    def setup_method(self) -> None:
        self.test_lib = lib.VideoLibrary()
        self.test_lib.read_from_file("test_library.csv")

    def test_query_matches_one_item(self):
        query = "Tom and Jerry"
        self.setup_method()
        assert self.test_lib.filter_by_name(query) == {
            "01": LibraryItem('Tom and Jerry', 'Fred Quimby', 4, 0)
        }

    def test_query_matches_multiple_items(self):
        query = "The Silence of the Lambs"

        assert self.test_lib.filter_by_name(query) == {
            "10": LibraryItem("The Silence of the Lambs", "Jonathan Demme", 4, 0),
            "11": LibraryItem("The Silence of the Lambs", "Jonathan Demme", 3, 0),
            "12": LibraryItem("The Silence of the Lambs", "Jonathan Demme", 2, 0),
            "13": LibraryItem("The Silence of the Lambs", "Jonathan Demme", 1, 0),
        }

    def test_query_matches_no_items(self):
        query = "Nonexistent"

        assert self.test_lib.filter_by_name(query) == {}

    
    def test_filter_by_rating(self):
        
        query = 5
        self.setup_method()
        assert self.test_lib.filter_by_rating(query) == {
            "02": LibraryItem("Breakfast at Tiffany's",'Blake Edwards',5,0),
            "08": LibraryItem("The Godfather: Part II",'Francis Ford Coppola',5,0)
        }

    def test_invalid_rating(self):
        query = 10
        self.setup_method()
        assert self.test_lib.filter_by_rating(query) == {}


    @pytest.mark.parametrize('key ,expected',[("01",1),("02",1),("03",1)])
    def test_increase_play_count(self,key,expected):
        self.setup_method()
        self.test_lib.increment_play_count(key)
        assert self.test_lib.library[key].play_count == expected