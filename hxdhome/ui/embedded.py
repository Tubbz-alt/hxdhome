"""
Module Docstring
"""
############
# Standard #
############
import copy
import logging

###############
# Third Party #
###############
import pedl
import numpy as np
from pedl.choices import ColorChoice, AlignmentChoice
from pedl.widgets.embedded import Display
##########
# Module #
##########

logger = logging.getLogger(__name__)


class EmbeddedControl(pedl.VBoxLayout):

    device_spacing = 5
    header_height  = 25

    def __init__(self, group, spacing=10, w=850,
                 theme=ColorChoice.Black):
        #Configuration Notes
        self.group = group
        self.theme = theme

        super(EmbeddedControl, self).__init__(spacing=spacing, **kwargs)

        #Iterate through Device Types
        for screen in self.embedded_types:

            #Find size of embedded window
            (screen_w, screen_h) = pedl.utils.find_screen_size(screen)

            #Find proper number of columns
            cols = max((w + self.device_spacing)
                     //(screen_w + self.device_spacing),1)

            #Initialize device layout
            device_layout = pedl.HBoxLayout(spacing=self.device_spacing)

            #Find widgets of this type
            widgets = sorted([d for d in self.group if d.embedded_screen==d])

            #Add each column of devices to device layout
            for column in np.array_split(widgets, cols):
                l = pedl.VBoxLayout(spacing=self.device_spacing)
                list(map(l.addWidget(self.embed_device(d)) for d in column))
                device_layout.addLayout(l)

            self.addLayout(l)

        #Reinsert header
        self.insertWidget(self.header, 0)


    def create_header(self, width):
        """
        Create a header for the window

        Parameters
        ----------
        width : int
            Width of header

        Returns
        -------
        header : ``pedl.StaticText``
            Header matching theme of window
        """
        return pedl.widgets.StaticText(w=width, h=self.header_height,
                                       text=group.name,
                                       fontColor=ColorChoice.White,
                                       fill=self.theme, lineWidth=3)


    @property
    def embedded_types(self):
        """
        Types of embedded windows to be drawn in control screen, sorted by the
        total number of instance of screen within the given :attr:`.group`
        """
        screens = [d.embedded_screen for d in self.group]
        return list(sorted(set(screens), key=lambda s : screens.count(s)))
