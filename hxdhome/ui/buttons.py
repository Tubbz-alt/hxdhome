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

##########
# Module #
##########

logger = logging.getLogger(__name__)


class StandIndicator(pedl.StackedLayout):
    """
    Indicator Widget for each stand along the beamline
    
    Parameters
    ----------
    args : 
        List of motors to include in the Indicator

    kwargs : 
        Extra arguments passed to ``pedl.StackedLayout``

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

    movement_pv : str
        Suffix to add to each motor prefix to color surrounding motion
        indicator
    """
    indicator_size    = 5
    indicator_spacing = 2
    max_col_height    = 6
    frame_margin      = 4
    indicator_pv      = '.MSTA'
    movement_pv       = '.DMOV'

    def __init__(self, *args, **kwargs):
        super(StandIndicator, self).__init__(**kwargs)

        #Split motors into columns
        columns = np.array_split(args, self.max_col_height)
        
        #Create overall layout
        lights = pedl.HBoxLayout(spacing=self.indicator_spacing)

        for column in columns:
            #Create column layout
            l = pedl.VBoxLayout(spacing=self.indicator_spacing)
            #Add each motor
            for mtr in column:
                l.addWidget(self.create_indicator(mtr)
            #Add to overall layout
            lights.addLayout(l)

        #Find proper frame dimension
        w, h = [d + self.frame_margin for d in (lights.w, lights.h)]

        #Add each frame
        for mtr in args:
            self.addWidget(self.create_movement_indicator(mtr, w, h))

        #Add indicators
        self.addLayout(lights)
    
        
    def create_indicator(self, prefix):
        """
        Create indicator light for a given motor
        """
        #Create buttons
        return pedl.Circle(w = self.indicator_size,
                           h = self.indicator_size,
                           fill = ColorChoice.Green,
                           alarmPV = prefix + self.indicator_pv,
                           alarm   = True)
        

    def create_motion_indicator(self, prefix, w, h):
        """
        Create indicator frame to notify when any motor in group is moving
        """
        return pedl.Rectangle(fill=False,
                               lineColor=ColorChoice.Yellow,
                               w = w,
                               h = h,
                               vis_pv  = prefix + self.movement_pv,
                               vis_min = 1)
