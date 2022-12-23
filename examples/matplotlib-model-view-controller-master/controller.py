"""
The controller is to be executed as the main app in this MVC pattern demo. 

Assumes a tkinter view.

Contains:

* Controller    Class that handles data and requests to/from the model and 
                the view.
"""

import tkinter as tk
from view import View
import model


class Controller:
    """Class that instantiates a view, and passes data and requests to/from 
    the model and the view.

    Variables are passed between model, view, and controller in the format:

        values = {'base': b, 'exponent': e}

    where b and e are floats.

    The controller assumes the model accepts a values dict and returns an x, 
    y tuple of numpy arrays suitable for a matplotlib plot.

    The controller assumes the view offers the following methods:

    * set_values(values)        used to initialize the view
    * clear() and .plot(x, y)   for clearing the canvas and plotting the 
                                x, y data provided by the model, respectively.

    Controller provides the following method for external use by the view:

    * update_view    Recalculates plot data, and updates view's plot.
    """

    def __init__(self, root):
        """
        Argument:
            root: a tkinter.Tk() object, to be used by the view.
        """
        self.view = View(root, self)
        self.default_values = {'base': 1, 'exponent': 2}
        self.initialize_view()

    def initialize_view(self):
        """Initialize the view's entry widgets and plot canvas."""
        self.view.set_values(self.default_values)
        self.update_view(self.default_values)

    def update_view(self, values):
        """Request x, y plot data from the model, and update the view's plot 
        with the new data.
        
        Argument:
            values: dict in 'values' format
        """
        self.get_plot_data(values)
        self.update_view_plot()

    def get_plot_data(self, values):
        """Send the values to the model and store the plot data returned.
        
        Argument:
            values: dict in 'values' format
            """
        self.plot_data = model.powerplot(**values)

    def update_view_plot(self):
        """Call view's methods to clear and redraw its plot, 
        using Controller's copy of the plot data."""
        self.view.canvas.clear()
        self.view.canvas.plot(*self.plot_data)


if __name__ == '__main__':
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()
