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
from pedl.choices          import ColorChoice, AlignmentChoice
from pedl.widgets.embedded import Display

##########
# Module #
##########

logger = logging.getLogger(__name__)

class EmbeddedControl(pedl.VBoxLayout):
    """
    Generic Large Embedded Window

    Simply contains an overhead title for the window, the remainder of the
    layout should be filled by subclasses

    Parameters
    ----------
    title : str
        Desired titled of Layout

    Attributes
    ----------
    header_height : int
        Height of overhead title

    header_color : :``pedl.ColorChoice``
        Color of title

    target_width : int
        Width of the EmbeddedGroup Window
    """
    header_height  = 25
    header_color   = ColorChoice.Black
    target_width   = 850

    def __init__(self, title):
        super(EmbeddedControl, self).__init__(alignment=AlignmentChoice.Center)
        self.title = title
        self.addWidget(self.header)


    def header(self):
        """
        Header for the window
        """
        return pedl.widgets.StaticText(w=self.target_width,
                                       h=self.header_height,
                                       text=self.title,
                                       fontColor=ColorChoice.White,
                                       fill=self.header_color, lineWidth=3)


class EmbeddedGroup(EmbeddedControl):
    """
    An EmbeddedControl screen for an arbitrary group of screens
    """
    #TODO Add back button
    device_spacing = 5
    type_spacing   = 10

    def __init__(self, group, **kwargs):
        #Configuration Notes
        self.group = group

        super(EmbeddedGroup, self).__init__(title=self.group.name,
                                            spacing=self.type_spacing,
                                            **kwargs)

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


    def embed_device(self, d):
        """
        Create an embedded device

        Parameters
        ----------
        d : ``happi.Device``
            Device to create embedded screen
        """
        return EmbeddedWindow(displays=[Display(d.name,
                                                d.embedded_screen,
                                                d.macros)],
                              autosize=True)


    @property
    def embedded_types(self):
        """
        Types of embedded windows to be drawn in control screen, sorted by the
        total number of instance of screen within the given :attr:`.group`
        """
        screens = [d.embedded_screen for d in self.group]
        return list(sorted(set(screens), key=lambda s : screens.count(s)))


class EmbeddedStand(EmbeddedControl):
    """
    An Embedded Control screen for a stand overview
    """
    def __init__(self, group):
        super(EmbeddedStand, self).__init__(title=group.name)


