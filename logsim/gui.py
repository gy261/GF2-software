
    """Implement the graphical user interface for the Logic Simulator.


Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
Gui - configures the main window and all the widgets.
"""
import wx
import wx.glcanvas as wxcanvas
from OpenGL import GL, GLUT

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser


class MyGLCanvas(wxcanvas.GLCanvas):
    """Handle all drawing operations.

    This class contains functions for drawing onto the canvas. It
    also contains handlers for events relating to the canvas.

    Parameters
    ----------
    parent: parent window.
    devices: instance of the devices.Devices() class.
    monitors: instance of the monitors.Monitors() class.

    Public methods
    --------------
    init_gl(self): Configures the OpenGL context.

    render(self, text): Handles all drawing operations.

    on_paint(self, event): Handles the paint event.

    on_size(self, event): Handles the canvas resize event.

    on_mouse(self, event): Handles mouse events.

    render_text(self, text, x_pos, y_pos): Handles text drawing
                                           operations.
    """

    def __init__(self, parent, devices, monitors):
        """Initialise canvas properties and useful variables."""
        super().__init__(parent, -1,
                         attribList=[wxcanvas.WX_GL_RGBA,
                                     wxcanvas.WX_GL_DOUBLEBUFFER,
                                     wxcanvas.WX_GL_DEPTH_SIZE, 16, 0])
        GLUT.glutInit()
        self.init = False
        self.context = wxcanvas.GLContext(self)

        # Initialise variables for panning
        self.pan_x = 0
        self.pan_y = 0
        self.last_mouse_x = 0  # previous mouse x position
        self.last_mouse_y = 0  # previous mouse y position

        # Initialise variables for zooming
        self.zoom = 1

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)

    def init_gl(self):
        """Configure and initialise the OpenGL context."""
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glViewport(0, 0, size.width, size.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, size.width, 0, size.height, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslated(self.pan_x, self.pan_y, 0.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)

    def render(self, text):
        """Handle all drawing operations."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Draw specified text at position (10, 10)
        self.render_text(text, 10, 10)

        # Draw a sample signal trace
        GL.glColor3f(0.0, 0.0, 1.0)  # signal trace is blue
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range(10):
            x = (i * 20) + 10
            x_next = (i * 20) + 30
            if i % 2 == 0:
                y = 75
            else:
                y = 100
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
        GL.glEnd()

        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def on_paint(self, event):
        """Handle the paint event."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        size = self.GetClientSize()
        text = "".join(["Canvas redrawn on paint event, size is ",
                        str(size.width), ", ", str(size.height)])
        self.render(text)

    def on_size(self, event):
        """Handle the canvas resize event."""
        # Forces reconfiguration of the viewport, modelview and projection
        # matrices on the next paint event
        self.init = False

    def on_mouse(self, event):
        """Handle mouse events."""
        text = ""
        # Calculate object coordinates of the mouse position
        size = self.GetClientSize()
        ox = (event.GetX() - self.pan_x) / self.zoom
        oy = (size.height - event.GetY() - self.pan_y) / self.zoom
        old_zoom = self.zoom
        if event.ButtonDown():
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            text = "".join(["Mouse button pressed at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.ButtonUp():
            text = "".join(["Mouse button released at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.Leaving():
            text = "".join(["Mouse left canvas at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False
            text = "".join(["Mouse dragged to: ", str(event.GetX()),
                            ", ", str(event.GetY()), ". Pan is now: ",
                            str(self.pan_x), ", ", str(self.pan_y)])
        if event.GetWheelRotation() < 0:
            self.zoom *= (1.0 + (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(["Negative mouse wheel rotation. Zoom is now: ",
                            str(self.zoom)])
        if event.GetWheelRotation() > 0:
            self.zoom /= (1.0 - (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(["Positive mouse wheel rotation. Zoom is now: ",
                            str(self.zoom)])
        if text:
            self.render(text)
        else:
            self.Refresh()  # triggers the paint event

    def render_text(self, text, x_pos, y_pos):
        """Handle text drawing operations."""
        GL.glColor3f(0.0, 0.0, 0.0)  # text is black
        GL.glRasterPos2f(x_pos, y_pos)
        font = GLUT.GLUT_BITMAP_HELVETICA_12

        for character in text:
            if character == '\n':
                y_pos = y_pos - 20
                GL.glRasterPos2f(x_pos, y_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))


class Gui(wx.Frame):
    """Configure the main window and all the widgets.

    This class provides a graphical user interface for the Logic Simulator and
    enables the user to change the circuit properties and run simulations.

    Parameters
    ----------
    title: title of the window.

    Public methods
    --------------
    on_menu(self, event): Event handler for the file menu.

    on_spin(self, event): Event handler for when the user changes the spin
                           control value.

    on_run_button(self, event): Event handler for when the user clicks the run
                                button.

    on_text_box(self, event): Event handler for when the user enters text.
    """

    def __init__(self, title, path, names, devices, network, monitors):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(800, 600))
        self.quit_id = 999
        self.open_id = 998
        self.help_id = 997
        self.home_id = 996
        self.cnf_id = 995
        self.logic_id = 994
        self.save_id = 993

        # Configure the file menu
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_ABOUT, "&About")
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors)
    
        # Store for monitored signals from network
        self.values = None
        self.trace_names = None
        self.time_steps = 8

        # Store inputs from logsim.py
        self.title = title
        self.path = path
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        #self.graph = Graph(self.names, self.devices, self.network,self.monitors)

        #self.switch_ids = self.devices.find_devices(self.devices.SWITCH)
        #self.switch_names = [self.names.get_name_string(i) for i in self.switch_ids]
        #self.switch_values = [self.devices.get_switch_value(i) for i in self.switch_ids]
        #self.sig_mons, self.sig_n_mons = self.monitors.get_signal_names()


        # Toolbar setup
        toolbar = self.CreateToolBar()
        myimage = wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, wx.ART_TOOLBAR)
        toolbar.AddTool(self.home_id, "Home", myimage)
        #myimage = wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_TOOLBAR)
        #toolbar.AddTool(self.logic_id, "Logic Description", myimage)
        #myimage = wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR)
        #toolbar.AddTool(self.cnf_id, _("CNF"), myimage)
        myimage = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR)
        toolbar.AddTool(self.open_id, "Open file", myimage)
        myimage = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR)
        toolbar.AddTool(self.save_id, "Save file", myimage)
        myimage = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR)
        toolbar.AddTool(self.help_id, "Help", myimage)
        toolbar.Bind(wx.EVT_TOOL, self.on_run_button) #should be tool-bar handler 
        toolbar.Realize()
        self.ToolBar = toolbar

        # Configure the widgets
        self.text = wx.StaticText(self, wx.ID_ANY, "Cycles to Run")
        self.spin = wx.SpinCtrl(self, wx.ID_ANY, "10")
        self.run_button = wx.Button(self, wx.ID_ANY, "Run")
        self.continue_button = wx.Button(self, wx.ID_ANY, "Continue")
        self.text_switch_control = wx.StaticText(self, wx.ID_ANY,"Switch Input")
        self.switch_choice = wx.ComboBox(self, wx.ID_ANY, "SWITCH", choices=[]) #should be choices = self.switch_names 
        self.switch_choice.SetValue("First switch name")#should be SetValue(self.switch_names[0])
        self.switch_choice_value = wx.RadioBox(self,wx.ID_ANY,choices=["0","1"])
        self.unmonitored_choice = wx.ComboBox(self, wx.ID_ANY, "UNMONITORED", choices=[]) #should be choices = self.sig_n_mons
        self.monitored_choice = wx.ComboBox(self, wx.ID_ANY, "MONITORED", choices=[]) #should be choices = self.sig_mons
        self.unmonitored_choice.SetValue("First unmonitored name")#should be SetValue(self.sig_n_mons[0])
        self.monitored_choice.SetValue("First monitored name")#should be SetValue(self.sig_mons[0])
        self.text_add_monitor = wx.StaticText(self, wx.ID_ANY,"Signal Monitors")
        self.add_monitor_button = wx.Button(self, wx.ID_ANY, "Add")
        self.remove_monitor_button = wx.Button(self, wx.ID_ANY, "Remove")
        self.exit_button = wx.Button(self, wx.ID_ANY, "Exit")
        #self.text_box = wx.TextCtrl(self, wx.ID_ANY, "",style=wx.TE_PROCESS_ENTER)

        # Bind events to widgets 
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.continue_button.Bind(wx.EVT_BUTTON, self.on_run_button) #需要增加on run event 
        self.switch_choice.Bind(wx.EVT_COMBOBOX, self.on_run_button) #需要增加on switch event
        self.switch_choice_value.Bind(wx.EVT_RADIOBOX, self.on_run_button) #需要增加on switch event 
        self.unmonitored_choice.Bind(wx.EVT_COMBOBOX, self.on_run_button) #需要增加on switch event 
        self.monitored_choice.Bind(wx.EVT_COMBOBOX, self.on_run_button) #需要增加on switch event 
        self.add_monitor_button.Bind(wx.EVT_BUTTON, self.on_run_button) #需要增加add monitor event 
        self.remove_monitor_button.Bind(wx.EVT_BUTTON, self.on_run_button) #需要增加continue button event 
        self.exit_button.Bind(wx.EVT_BUTTON, self.on_exit_box)
        #self.text_box.Bind(wx.EVT_TEXT_ENTER, self.on_text_box)

        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)
        side_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer5 = wx.BoxSizer(wx.HORIZONTAL)

        main_sizer.Add(self.canvas, 5, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(side_sizer, 1, wx.ALL, 5)

        side_sizer.Add(self.text, 1, wx.ALL, 10)
        side_sizer.Add(self.spin, 0, wx.EXPAND | wx.LEFT, 10)
        side_sizer.Add(side_sizer3, 0, wx.ALL, 5)
        side_sizer3.Add(self.run_button, 0, wx.EXPAND | wx.LEFT, 25)
        side_sizer3.Add(self.continue_button, 0, wx.EXPAND | wx.LEFT, 75) 
        #side_sizer.Add(self.text_box, 1, wx.ALL, 5)

        side_sizer.Add(self.text_switch_control, 0, wx.EXPAND | wx.LEFT, 10)
        side_sizer.Add(side_sizer4, 0, wx.ALL, 0)
        #side_sizer4.Add(self.switch_choice, 1, wx.ALL, 5)
        side_sizer4.Add(self.switch_choice, 0, wx.ALL, 5)
        side_sizer4.Add(self.switch_choice_value,0, wx.EXPAND | wx.LEFT, 30)

        side_sizer.Add(self.text_add_monitor, 1, wx.ALL, 10)
        side_sizer.Add(side_sizer1, 1, wx.ALL, 5)

        side_sizer5.Add(self.unmonitored_choice, 0, wx.EXPAND | wx.LEFT, 5)
        side_sizer5.Add(self.monitored_choice, 0, wx.EXPAND | wx.LEFT, 5)
        side_sizer.Add(side_sizer5,0, wx.ALL, 5)
        side_sizer1.Add(self.add_monitor_button, 0, wx.EXPAND | wx.LEFT, 25)
        side_sizer1.Add(self.remove_monitor_button, 0,  wx.EXPAND | wx.LEFT, 75)
        side_sizer.Add(self.exit_button,0,wx.ALIGN_CENTER | wx.TOP,270)
        #side_sizer.Add(self.text_connection_monitor, 1, wx.ALL, 10)
        #side_sizer.Add(side_sizer5, 1, wx.ALL, 5)
        #side_sizer.Add(side_sizer6, 1, wx.ALL, 5)
        #side_sizer.Add(side_sizer7, 1, wx.ALL, 5)


        self.SetSizeHints(600, 600)
        self.SetSizer(main_sizer)

    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)
        if Id == wx.ID_ABOUT:
            wx.MessageBox("Logic Simulator\nCreated by Mojisola Agboola\n2017",
                          "About Logsim", wx.ICON_INFORMATION | wx.OK)

    def on_spin(self, event):
        """Handle the event when the user changes the spin control value."""
        spin_value = self.spin.GetValue()
        text = "".join(["New spin control value: ", str(spin_value)])
        self.canvas.render(text)

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""
        text = "Run button pressed."
        self.canvas.render(text)

    def on_text_box(self, event):
        """Handle the event when the user enters text."""
        text_box_value = self.text_box.GetValue()
        text = "".join(["New text box value: ", text_box_value])
        self.canvas.render(text)

    def on_exit_box(self, event):
        """Handle the event when the user enters text."""
        wx.Exit()
