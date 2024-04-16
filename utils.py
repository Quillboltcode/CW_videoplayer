

# create utility function for video player

def set_text(text_widget, content):
    """Set the text content of a text widget."""
    text_widget.delete("1.0", "end")
    text_widget.insert("1.0", content)

# define colour buttons based on https://bootswatch.com/vapor/
colors = {
            "primary": "#6e40c0",
            "secondary": "#ea38b8",
            "success": "#3af180",
            "info": "#1da2f2",
            "warning": "#ffbd05",
            "danger": "#e34b54",
            "light": "#44d7e8",
            "dark": "#170229",
            "bg": "#190831",
            "fg": "#32fbe2",
            "selectbg": "#461a8a",
            "selectfg": "#ffffff",
            "border": "#060606",
            "inputfg": "#bfb6cd",
            "inputbg": "#30115e",
            "active": "#17082E",
}
    
def convert_str_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b


RGB = 'rgb'

"""
https://stackoverflow.com/questions/1855884/determine-font-color-based-on-background-color

"""

def contrast_color(color, model=RGB, darkcolor='#000', lightcolor='#fff'):
    """Returns the best matching contrasting light or dark color for
    the given color.
    
    Parameters:

        color (Any):
            The color value to evaluate.

        model (str):
            The model of the color value to be evaluated. 'rgb' by 
            default.

        darkcolor (Any):
            The color value to be returned when the constrasting color 
            should be dark.

        lightcolor (Any):
            The color value to be returned when the constrasting color
            should be light.

    Returns:

        str:
            The matching color value.
    """

    r, g, b = convert_str_to_rgb(color)

    luminance = ((0.299 * r) + (0.587 * g) + (0.114 * b))/255
    if luminance > 0.5:
        return darkcolor
    else:
        return lightcolor


def compare_2_dict_value(dict1, dict2):
    for key in dict1:
        if dict1[key] != dict2[key]:
            return False
    return True

