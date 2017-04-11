"""
Represent a group of motors as a single pressbutton
"""
############
# Standard #
############
import logging

###############
# Third Party #
###############
import pedl
import numpy as np
from pedl.choices import ColorChoice, AlignmentChoice
from pedl.widgets import StaticText, Circle, Rectangle, MenuButton
##########
# Module #
##########

logger = logging.getLogger(__name__)


class StandIndicator(pedl.StackedLayout):
    """
    Indicator Widget for each stand along the beamline

    Parameters
    ----------
    group : :class:`.HXDGroup`
        List of motors to include in the Indicator

    Attributes
    ----------
    indicator_size : int
        Width and Height of small indicator lights

    indicator_spacing : int
        Spacing between each indicator light

    max_col_height : int
        Maximum  number of lights to stack in a column

    frame_margin : int
        Distance between lights and surrounding motion indicator

    indicator_pv : str
        Suffix to add to each motor prefix to color indicator light

    motion_pv : str
        Suffix to add to each motor prefix to color surrounding motion
        indicator
    """
    indicator_size    = 5
    indicator_spacing = 2
    max_col_height    = 6
    frame_margin      = 4
    indicator_pv      = '.MSTA'
    motion_pv         = '.DMOV'

    def __init__(self, group):
        #Save groups
        self.group = group

        super(StandIndicator, self).__init__()

        #Grab motors
        motors = [d for d in self.group.devices if 'MMS' in d.prefix]

        #Split motors into columns
        columns = [motors[i:i+self.max_col_height]
                   for i in range(0, len(motors), self.max_col_height)]

        #Create overall layout
        lights = pedl.HBoxLayout(spacing=self.indicator_spacing)

        for column in columns:
            #Create column layout
            l = pedl.VBoxLayout(spacing=self.indicator_spacing)
            #Add each motor
            for mtr in column:
                l.addWidget(self.create_indicator(mtr))
            #Add to overall layout
            lights.addLayout(l)

        #Find proper frame dimension
        w, h = [d + self.frame_margin for d in (lights.w, lights.h)]

        #Add each frame
        for mtr in motors:
            self.addWidget(self.create_motion_indicator(mtr, w, h))

        #Add indicators
        self.addLayout(lights)

        #Add Group Selection
        self.add_menu()


    def add_menu(self):
        """
        Add a :class:`.MenuButton`
        """
        MenuButton.buttonize(self, blend=ColorChoice.Grey,
                             controlPv=self.group.pv)


    def create_indicator(self, mtr):
        """
        Create indicator light for a given motor
        """
        #Create buttons
        return Circle(w = self.indicator_size,
                      h = self.indicator_size,
                      fill = ColorChoice.Green,
                      alarmPV = mtr.prefix + self.indicator_pv,
                      alarm   = True)


    def create_motion_indicator(self, mtr, w, h):
        """
        Create indicator frame to notify when any motor in group is moving
        """
        #Visibility Rules
        vis = pedl.Visibility(pv= mtr.prefix + self.motion_pv, min=0)
        return Rectangle(fill=False, w=w, h=h,
                         lineColor=ColorChoice.Yellow,
                         visibility=vis)


class StandButton(pedl.StackedLayout):
    """
    Generic Block diagram of Stand

    Composed of a single rectangle, the StandButton is buttonized  to show the
    stand overview screen

    Parameters
    ----------
    group : :class:`.HXDGroup`
        Group of devices with name of stand

    Attributes
    ----------
    stand_size : tuple
        Width and Height of the rectangle

    frame_width : int
        Thickness of border surrounding rectangle
    """
    stand_size  = (50, 20)
    frame_width =  2

    def __init__(self, group):
        self.group = group
        super(StandButton, self).__init__()
        #Add Rectangle
        self.addWidget(self.stand_symbol)


    @property
    def stand_symbol(self):
        """
        Rectange Drawing of Stand
        """
        return StaticText(w=self.stand_size[0],
                          h=self.stand_size[1],
                          fill=ColorChoice.Grey,
                          font=pedl.Font(bold=True),
                          text=self.group.name,
                          lineWidth=self.frame_width,
                          alignment=AlignmentChoice.Center)
