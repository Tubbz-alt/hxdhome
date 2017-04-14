"""
The two major displays that are meant to be launched are :class:`.HXRAYStand`
and :class:`.HXRAYHome`. Each inherit from :class:`.HXRAYWindow` that handles
writing EDM files to disk, whether they be temporary or permanent
"""
############
# Standard #
############
import os.path
import logging
import tempfile

###############
# Third Party #
###############
import pedl
from pedl.choices          import AlignmentChoice
from pedl.widgets          import MenuButton, EmbeddedWindow, MessageButton
from pedl.widgets.embedded import Display
##########
# Module #
##########
from .buttons  import StandIndicator, StandButton
from .embedded import EmbeddedStand, EmbeddedGroup
logger = logging.getLogger(__name__)

class HXRAYWindow(pedl.HBoxLayout):
    """
    Generic Window

    Many of the created EDM files have complex interactions between
    EmbeddedWindows and file paths that need to handled as ``pedl`` layouts are
    rendered. The methods in this class handle saving these in sensible
    locations in the file system to either temporarily view the files or saved
    to disk.

    Parameters
    ----------
    group : :class:`HXDGroup`
        Group of subgroups and devices to render 

    kwargs :
        Passed on to Layout configuration
    """

    def __init__(self, group, **kwargs):
        self.group  =  group
        self.app    =  pedl.Designer()
        #Initialize layout
        super(HXRAYWindow, self).__init__(alignment=AlignmentChoice.Center,
                                          **kwargs)


    @property
    def subdisplays(self):
        """
        List of tuples (layout, display) to be rendered into screens.
        Reimplemented by subclasses
        """
        raise NotImplementedError


    def show(self, block=False):
        """
        Show the EDM display

        Parameters
        ----------
        block : bool
            Block the thread while the screen is open

        Returns
        -------
        proc : subprocess.Popen
            Process launched by show
        """
        #Create temporary subdisplays
        tmp = self._show_displays()
        #Add main layout
        self.app.window.setLayout(self, resize=True)
        return self.app.exec_(wait=block)


    def save(self, name=None, build_dir=''):
        """
        Save the window to file

        The full path is specified by :attr:`.build_dir` as EDM is sensitive to
        directory structure

        Parameters
        ----------
        name : str, optional
            Name of file, otherwise the group :attr:`HXDGroup.alias` is used.
        """
        #Use default name
        prefix = name or self.group.alias
        #Add .edl suffix
        if not prefix.endswith('.edl'):
            prefix += '.edl'
        #Create saved subdisplays
        self._save_displays(build_dir=build_dir)
        #Set main layout
        self.app.window.setLayout(self, resize=True)
        #Save to disk
        with open(os.path.join(build_dir, prefix), 'w+') as handle:
            self.app.dump(handle)


    def _save_displays(self, build_dir=''):
        """
        Save displays to edl files
        """
        #Iterate through displays
        for lay, display in self.subdisplays:
            #Set window as main Designer layout
            self.app.window.setLayout(lay, resize=True)

            #Create filename
            fname = os.path.join(build_dir,
                                 self.group.alias+display.name)

            #Write to disk
            with open(fname, 'w+') as handle:
                self.app.dump(handle)
                #Adjust path name
                display.path = fname


    def _show_displays(self):
        """
        Create temporary display names
        """
        context = []

        #Iterate through displays
        for lay, display in self.subdisplays:
            #Set window as main Designer layout
            self.app.window.setLayout(lay, resize=True)
            #Create temporary file
            tmp = tempfile.NamedTemporaryFile(mode='w+', suffix='.edl')
            #Save name and add to context to be destroyed later
            display.path = tmp.name
            context.append(tmp)
            #Create a new file handle so we don't delete before we close
            with open(tmp.name, 'w') as handle:
                self.app.dump(handle)

        return context


class HXRAYHome(HXRAYWindow):
    """
    Main Home Screen

    The home screen can be divided into three main sections, the center of the
    screen which consists of indicators for various devices along the beamline.
    These allow for quick navigation between different sections of the
    instrument through a combination of hidden MenuButtons and MessageButtons.
    Secondly, on the right side of the screen is a large EmbeddedWindow with a
    display for each of the stands. Finally at the bottom is a tabbed display
    with links to executable and other screens not embedded in the home window.

    Parameters
    ----------
    hutch : :class:`.HXDGroup`
        Large group of all devices to render. This should usually have two
        layers of grouping, with the first subgroups being stands and those
        below being device groupings

    Attributes
    ----------
    vert_spacing : int
        Distance between indicator rows

    horiz_spacing : int
        Distance between indicator columns
    
    window_size : tuple
        Size of embedded window (w,h)
    """
    #Geometry settings
    vert_spacing  = 75
    horiz_spacing = 10
    window_size   = (600, 900)

    def __init__(self, hutch):
        #Initialize layout
        super(HXRAYHome, self).__init__(hutch, spacing=self.horiz_spacing)

        #Set Embedded window size
        HXRAYStand.window_size = self.window_size

        #All displays not including embedded controls
        left_panels = pedl.VBoxLayout(spacing=self.vert_spacing,
                                      alignment=AlignmentChoice.Center)

        indicators = pedl.HBoxLayout(spacing=self.horiz_spacing,
                                     alignment=AlignmentChoice.Center)
        #Add all stand indicators and buttons
        for stand in self.group.subgroups:
            indicators.addLayout(self.create_stand_buttons(stand))

        #Create left panel layout
        left_panels.addLayout(indicators)
        #left_panels.addLayout(ControlTab)
        self.addLayout(left_panels)

        #Create EmbeddedControls
        self.stands = self.create_stands()
        self.window = self.create_window()
        self.addWidget(self.window)


    def create_stand_buttons(self, group):
        """
        Create indicator column for stands

        This consists of a StandButton and StandIndicator in a vertical column.
        Each of these is buttonized so that it can control the main embedded
        windows.

        Parameters
        ----------
        group : :class:`.HXDGroup`
            This should be a subgroup of the main hutch with only one layer of
            :attr:`.subgroups` below

        Returns
        -------
        stand : :class:`pedl.VBoxLayout`
            Vertical layout with indicator lights and buttons
        """
        stand = pedl.VBoxLayout(spacing=self.vert_spacing,
                                alignment=AlignmentChoice.Center)

        #Create main frame
        stand.addLayout(StandIndicator(group))
        stand.addLayout(StandButton(group))

        #Buttonize
        for widget in stand.widgets:
            MessageButton.buttonize(widget, value=group.alias,
                                    controlPv=self.group.pv)

        return stand


    @property
    def subdisplays(self):
        """
        Subdisplays to be rendered simultaneously, tuples of
        :class:`.HXRAYStand` and their embedded display descriptions
        """
        return zip(self.stands, self.window.displays)


    def create_stands(self):
        """
        Create every :class:`.EmbeddedStand` screen for the hutch
        """
        return [HXRAYStand(group) for group in self.group.subgroups]


    def create_window(self):
        """
        Create :class:`.EmbeddedWindow` containing each stand display
        """
        emb = EmbeddedWindow(autoscale=False, controlPv=self.group.pv)

        for stand in self.stands:
            #Information is set later upon rendering
            emb.addDisplay(Display(stand.group.alias+'.edl', None, None))

        #Manual resize, to avoid doing it for each addition
        emb.w, emb.h  = self.window_size

        return emb


    def _save_displays(self, build_dir=''):
        """
        Reimplemented to save all child displays
        """
        #Create all subdisplays for stands
        list(map(lambda x : x._save_displays(build_dir=build_dir),
                 self.stands))
        #Create stand displays
        super(HXRAYHome, self)._save_displays(build_dir=build_dir)


    def _show_displays(self):
        """
        Reimplemented to keep track of all child displays
        """
        #Create all subdisplays for stands
        context = list(map(lambda x : x._show_displays(),
                       self.stands))
        #Create home displays
        context.append(super(HXRAYHome, self)._show_displays())

        #Return flattened list of tempfiles
        return [tmp for display in context for tmp in display]


class HXRAYStand(HXRAYWindow):
    """
    EmbeddedWindow set for Stands

    A single embedded window containing a summary of the stand devices, as well
    as a display for each subgroup.

    Parameters
    ----------
    stand : :class:`.HXDGroup`
        Group with one layer of subgroups for devices 
    """
    window_size = (600, 1100)

    def __init__(self, stand):
        super(HXRAYStand, self).__init__(stand)
        self.window = self.create_window()
        #Add main embedded window
        self.addWidget(self.window)


    @property
    def subdisplays(self):
        """
        Subdisplays to be rendered simultaneously, tuples of
        :class:`.EmbeddedControl` and their embedded display descriptions
        """
        return zip(self.embedded, self.window.displays)


    @property
    def embedded_overview(self):
        """
        Overall display for stand
        """
        emb = EmbeddedStand(self.group, target_width=self.window_size[0])
        MenuButton.buttonize(emb.widgets[0], controlPv=self.group.pv)
        return emb


    @property
    def embedded_groups(self):
        """
        Every subgroup display in the Widget
        """
        emb = [EmbeddedGroup(group, target_width=self.window_size[0])
               for group in self.group.subgroups]

        #Buttonize title
        for display in emb:
            MenuButton.buttonize(display.widgets[0], controlPv=self.group.pv)

        return emb

    @property
    def embedded(self):
        """
        All displays contained within stand
        """
        return self.embedded_groups + [self.embedded_overview] 


    def create_window(self):
        """
        Create an :class:`.pedlEmbeddedWindow` containing all stand groups
        """
        #Instantiate EmbeddedWindow
        emb = EmbeddedWindow(autoscale=False, controlPv=self.group.pv)

        for display in self.embedded:
            #Information is set later upon rendering
            emb.addDisplay(Display(display.filename, None, None))

        #Manual resize, to avoid doing it for each addition
        emb.w, emb.h  = self.window_size

        return emb
