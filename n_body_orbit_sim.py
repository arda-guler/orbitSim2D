#   2D N-BODY ORBIT SIMULATOR

version = "0.6.0"

from dearpygui.core import *
from dearpygui.simple import *
import math
import pandas as pd
import time as t
import scipy.constants as scp_const

#set initial window configuration (purely cosmetic)
set_main_window_size(1300, 700)
set_main_window_title("N-body Simulator 2D")
set_theme("Dark")

calc_run_number = 0

grav_const = scp_const.G

set_value(name="progress", value=0)

vessels = []
bodies = []
objects = []
target = None
target_id = 0

set_value(name="vessels", value=[])
set_value(name="bodies", value=[])
set_value(name="objects", value=[])

class body ():

    def __init__(self):
        self.mass = 0
        self.radius = 0
        self.pos_x = 0
        self.pos_y = 0
        self.vel_x = 0
        self.vel_y = 0
        self.alt = 0
        self.vel_tgn = 0
        self.vel_rad = 0
        self.long = 0
        self.exists = False
        self.label = "Body"
        self.color = [255, 255, 255, 255]
        self.x_list = []
        self.y_list = []
        self.orbiting = None
        self.orbiting_init = None

    def set_label (self, new_label):
        self.label = new_label

    def get_label (self):
        return self.label

    def set_color(self, new_color):
        self.color = new_color

    def get_color(self):
        return self.color

    def clear_traj_history(self):
        self.x_list = []
        self.y_list = []

    def update_traj(self):
        self.x_list.append(self.pos_x)
        self.y_list.append(self.pos_y)

    def get_traj(self):
        return [self.x_list, self.y_list]

    def set_pos (self, x, y):
        self.pos_x = x
        self.pos_y = y

    def get_pos (self):
        return self.pos_x, self.pos_y

    def set_vel (self, x, y):
        self.vel_x = x
        self.vel_y = y

    def get_vel (self):
        return self.vel_x, self.vel_y

    def update_pos (self, vel_x, vel_y, timescale):
        self.pos_x = self.pos_x + vel_x * timescale
        self.pos_y = self.pos_y + vel_y * timescale

    def update_vel (self,accel_x, accel_y, timescale):
        self.vel_x = self.vel_x + accel_x * timescale
        self.vel_y = self.vel_y + accel_y * timescale

    def set_radius (self,r):
        self.radius = r

    def set_mass (self, m):
        self.mass = m

    def set_exists (self, existence):
        self.exists = existence

    def set_alt_init (self, altitude):
        self.alt_init = altitude

    def get_alt_init (self):
        return self.alt_init

    def set_alt (self, altitude):
        self.alt = altitude

    def get_alt (self):
        return self.alt

    def set_long_init(self, longitude):
        self.long_init = longitude

    def get_long_init(self):
        return self.long_init

    def set_long (self, longitude):
        self.long = longitude

    def get_long (self):
        return self.long

    def set_vel_tgn_init (self, velocity):
        self.vel_tgn_init = velocity

    def get_vel_tgn_init (self):
        return self.vel_tgn_init

    def set_vel_rad_init (self, velocity):
        self.vel_rad_init = velocity

    def get_vel_rad_init (self):
        return self.vel_rad_init

    def set_vel_tgn (self, velocity):
        self.vel_tgn = velocity

    def get_vel_tgn (self):
        return self.vel_tgn

    def set_vel_rad (self, velocity):
        self.vel_rad = velocity

    def get_vel_rad (self):
        return self.vel_rad

    def does_exist (self):
        return self.exists

    def get_radius (self):
        return self.radius

    def get_mass (self):
        return self.mass

    def get_grav_pull (self, dist):
        return (grav_const * self.mass) / (dist**2)

    def set_orbiting_init (self, body):
        self.orbiting_init = body

    def get_orbiting_init (self):
        return self.orbiting_init

class vessel ():

    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.vel_y = 0
        self.vel_x = 0
        self.orbiting = None
        self.orbiting_init = None
        self.label = "Vessel"
        self.color = [200,0,0,255]
        self.x_list = []
        self.y_list = []

    def set_label (self, new_label):
        self.label = new_label

    def get_label (self):
        return self.label

    def does_exist (self):
        return True

    def set_color(self, new_color):
        self.color = new_color

    def get_color(self):
        return self.color

    def clear_traj_history(self):
        self.x_list = []
        self.y_list = []

    def update_traj(self):
        self.x_list.append(self.pos_x)
        self.y_list.append(self.pos_y)

    def get_traj(self):
        return [self.x_list, self.y_list]

    def set_pos (self, x, y):
        self.pos_x = x
        self.pos_y = y

    def get_pos (self):
        return self.pos_x, self.pos_y

    def set_vel (self, x, y):
        self.vel_x = x
        self.vel_y = y

    def get_vel (self):
        return self.vel_x, self.vel_y

    def update_pos (self, vel_x, vel_y, timescale):
        self.pos_x = self.pos_x + vel_x * timescale
        self.pos_y = self.pos_y + vel_y * timescale

    def update_vel (self, accel_x, accel_y, timescale):
        self.vel_x = self.vel_x + accel_x * timescale
        self.vel_y = self.vel_y + accel_y * timescale

    def set_alt_init (self, altitude):
        self.alt_init = altitude

    def get_alt_init (self):
        return self.alt_init

    def set_alt (self, altitude):
        self.alt = altitude

    def get_alt (self):
        return self.alt

    def set_long_init(self, longitude):
        self.long_init = longitude

    def get_long_init(self):
        return self.long_init

    def set_long (self, longitude):
        self.long = longitude

    def get_long (self):
        return self.long

    def set_vel_tgn_init (self, velocity):
        self.vel_tgn_init = velocity

    def get_vel_tgn_init (self):
        return self.vel_tgn_init

    def set_vel_rad_init (self, velocity):
        self.vel_rad_init = velocity

    def get_vel_rad_init (self):
        return self.vel_rad_init

    def set_vel_tgn (self, velocity):
        self.vel_tgn = velocity

    def get_vel_tgn (self):
        return self.vel_tgn

    def set_vel_rad (self, velocity):
        self.vel_rad = velocity

    def get_vel_rad (self):
        return self.vel_rad

    def set_orbiting_init (self, body):
        self.orbiting_init = body

    def get_orbiting_init (self):
        return self.orbiting_init

    def set_orbiting (self, body):
        self.orbiting = body

    def get_orbiting (self):
        return self.orbiting

# Vessel E-S-D
def examineVesselSetup():
    
    global vessels
    vessel_found = False
    
    for vessel in vessels:
        if vessel.get_label() == get_value("vessel_name"):
            vessel_found = True
            set_value(name="alt_init_field", value=vessel.get_alt_init())
            set_value(name="vel_tgn_init_field", value=vessel.get_vel_tgn_init())
            set_value(name="vel_rad_init_field", value=vessel.get_vel_rad_init())
            set_value(name="long_init_field", value=vessel.get_long_init())
            set_value(name="vessel_color_edit", value=vessel.get_color())
            set_value(name="init_orbiting_body_field", value=vessel.get_orbiting_init().get_label())

    if not vessel_found:
        set_value(name="alt_init_field", value="VESSEL NOT FOUND.")
        set_value(name="vel_tgn_init_field", value="VESSEL NOT FOUND.")
        set_value(name="vel_rad_init_field", value="VESSEL NOT FOUND.")
        set_value(name="long_init_field", value="VESSEL NOT FOUND.")
        set_value(name="init_orbiting_body_field", value="VESSEL NOT FOUND.")

def saveVesselSetup():

    global vessels, objects, bodies

    already_exists = False
    for ves in vessels:     
        if str(get_value("vessel_name")) == ves.get_label():
            new_vessel = ves
            already_exists= True

    if not already_exists:
        new_vessel = vessel()

    orbit_init = (get_value("init_orbiting_body_field"))
    reference_found = False

    for body in bodies:
        if body.get_label() == orbit_init:
            new_vessel.set_orbiting_init(body)
            reference_found = True

    if not orbit_init or orbit_init == "":
        reference_found = True

    if not reference_found:
        set_value(name="init_orbiting_body_field", value="REFERENCE NOT FOUND - SAVE ABORTED!")
        return
    
    new_vessel.set_alt_init(float(get_value("alt_init_field")))
    new_vessel.set_vel_tgn_init(float(get_value("vel_tgn_init_field")))
    new_vessel.set_vel_rad_init(float(get_value("vel_rad_init_field")))
    new_vessel.set_long_init(float(get_value("long_init_field")))
    new_vessel.set_label(str(get_value("vessel_name")))
    new_vessel.set_color(get_value("vessel_color_edit"))

    if not already_exists:
        vessels.append(new_vessel)
        objects.append(new_vessel)
        set_value(name="vessels", value=vessels)
        set_value(name="objects", value=objects)
        add_menu_item(name=new_vessel.get_label(), parent="vessel_menu", callback=lockView)

    initVessels()
    updateVisualizer()

def deleteVessel():
    
    global vessels, objects

    vessel_found = False
    
    for vessel in vessels:
        if get_value("vessel_name") == vessel.get_label():
            vessel_found = True
            set_value(name="alt_init_field", value="VESSEL DELETED.")
            set_value(name="vel_tgn_init_field", value="VESSEL DELETED.")
            set_value(name="vel_rad_init_field", value="VESSEL DELETED.")
            set_value(name="long_init_field", value="VESSEL DELETED.")
            set_value(name="init_orbiting_body_field", value="VESSEL DELETED.")
            hide_item(vessel.get_label())
            vessel.clear_traj_history()
            vessels.remove(vessel)
            del vessel

    for obj in objects:
        if get_value("vessel_name") == obj.get_label():
            del obj
            updateVisualizer()

    if not vessel_found:
        set_value(name="alt_init_field", value="VESSEL NOT FOUND.")
        set_value(name="vel_tgn_init_field", value="VESSEL NOT FOUND.")
        set_value(name="vel_rad_init_field", value="VESSEL NOT FOUND.")
        set_value(name="long_init_field", value="VESSEL NOT FOUND.")
        set_value(name="init_orbiting_body_field", value="VESSEL NOT FOUND.")

# Body E-S-D
def examineBodySetup():
    
    global bodies, objects
    body_found = False

    for body in bodies:
        if body.get_label() == get_value("moon_name"):
            body_found = True
            set_value(name="moon_mass_field", value=body.get_mass())
            set_value(name="moon_mass_magnitude_field", value="0")
            set_value(name="moon_radius_field", value=body.get_radius())
            set_value(name="moon_radius_magnitude_field", value="0")
            set_value(name="moon_alt_init_field", value=body.get_alt_init())
            set_value(name="moon_vel_tgn_init_field", value=body.get_vel_tgn_init())
            set_value(name="moon_vel_rad_init_field", value=body.get_vel_rad_init())
            set_value(name="moon_long_init_field", value=body.get_long_init())
            set_value(name="moon_color_edit", value=body.get_color())
            set_value(name="moon_init_orbiting_field", value=body.get_orbiting_init().get_label())
            
    if not body_found:
        set_value(name="moon_mass_field", value="BODY NOT FOUND.")
        set_value(name="moon_mass_magnitude_field", value="BODY NOT FOUND.")
        set_value(name="moon_radius_field", value="BODY NOT FOUND.")
        set_value(name="moon_radius_magnitude_field", value="BODY NOT FOUND.")
        set_value(name="moon_alt_init_field", value="BODY NOT FOUND.")
        set_value(name="moon_vel_tgn_init_field", value="BODY NOT FOUND.")
        set_value(name="moon_vel_rad_init_field", value="BODY NOT FOUND.")
        set_value(name="moon_long_init_field", value="BODY NOT FOUND.")
        set_value(name="moon_init_orbiting_field", value="BODY NOT FOUND.")    

def saveBodySetup():

    global bodies, objects

    already_exists = False
    for obj in bodies:     
        if str(get_value("moon_name")) == obj.get_label():
            new_body = obj
            already_exists = True
            
    if not already_exists:
        new_body = body()

    orbit_init = str(get_value("moon_init_orbiting_body_field"))
    reference_found = False
    
    for obj in bodies:
        if obj.get_label() == orbit_init:
            new_body.set_orbiting_init(obj)
            reference_found = True

    if not orbit_init or orbit_init == "":
        reference_found = True

    if not reference_found:
        set_value(name="moon_init_orbiting_body_field", value="REFERENCE NOT FOUND - SAVE ABORTED!")
        return
    
    new_body.set_mass(float(get_value("moon_mass_field")) * 10**float((get_value("moon_mass_magnitude_field"))))
    new_body.set_radius(float(get_value("moon_radius_field")) * 10**float((get_value("moon_radius_magnitude_field"))))
    new_body.set_alt_init(float(get_value("moon_alt_init_field")))
    new_body.set_vel_tgn_init(float(get_value("moon_vel_tgn_init_field")))
    new_body.set_vel_rad_init(float(get_value("moon_vel_rad_init_field")))
    new_body.set_long_init(float(get_value("moon_long_init_field")))
    new_body.set_label(str(get_value("moon_name")))
    new_body.set_color(get_value("moon_color_edit"))

    if not already_exists:
        bodies.append(new_body)
        objects.append(new_body)
        set_value(name="bodies", value=bodies)
        set_value(name="objects", value=objects)
        add_menu_item(name=new_body.get_label(), parent="moon_menu", callback=lockView)

    initBodies()
    updateVisualizer()

def deleteBody():
    
    global bodies, objects

    body_found = False
    
    for body in bodies:
        if get_value("moon_name") == body.get_label():
            body_found = True
            set_value(name="moon_mass_field", value="BODY DELETED.")
            set_value(name="moon_mass_magnitude_field", value="BODY DELETED.")
            set_value(name="moon_radius_field", value="BODY DELETED.")
            set_value(name="moon_radius_magnitude_field", value="BODY DELETED.")
            set_value(name="moon_alt_init_field", value="BODY DELETED.")
            set_value(name="moon_vel_tgn_init_field", value="BODY DELETED.")
            set_value(name="moon_vel_rad_init_field", value="BODY DELETED.")
            set_value(name="moon_long_init_field", value="BODY DELETED.")
            hide_item(body.get_label())
            body.clear_traj_history()
            bodies.remove(body)
            del body

    for obj in objects:
        if get_value("moon_name") == obj.get_label():
            del obj
            updateVisualizer()

    if not body_found:
        set_value(name="moon_mass_field", value="BODY NOT FOUND.")
        set_value(name="moon_mass_magnitude_field", value="BODY NOT FOUND.")
        set_value(name="moon_radius_field", value="BODY NOT FOUND.")
        set_value(name="moon_radius_magnitude_field", value="BODY NOT FOUND.")
        set_value(name="moon_alt_init_field", value="BODY NOT FOUND.")
        set_value(name="moon_vel_tgn_init_field", value="BODY NOT FOUND.")
        set_value(name="moon_vel_rad_init_field", value="BODY NOT FOUND.")
        set_value(name="moon_long_init_field", value="BODY NOT FOUND.")

def resetSimulation():
    initBodies()
    initVessels()
    updateVisualizer()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                 FILE IMPORT/EXPORT
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def browseSaves():  
    open_file_dialog(extensions=".txt", callback=selectSave)

def selectSave(dialog, save_path):
    set_value("filepath_field", save_path[0] + "\\" + save_path[1])

def importFile():
    global bodies, vessels, objects

    try:
        import_filepath = get_value("filepath_field")
        
        if not import_filepath[-4:] == ".txt":
            import_filepath = import_filepath + ".txt"
            
        log_info("Importing inputs from " + import_filepath, logger="Logs")
        import_file = open(import_filepath, "r")
    except:
        log_error("Import failed. Check filepath.", logger="Logs")
        return

    try:
        import_lines = import_file.readlines()
        if not import_lines[0][18:-1] == version:
            log_warning("Save file version does not match software version. Import might fail.", logger="Logs")

        for obj in objects:
            del obj

        for b in bodies:
            del b

        for v in vessels:
            del v
            
        objects, bodies, vessels = [], [], []

        for line in import_lines:
            
            if line[0] == "B":
                line = line.split("|")
                new_body = body()
                new_body.set_mass(float(line[3]))
                new_body.set_radius(float(line[4]))
                new_body.set_alt_init(float(line[5]))
                new_body.set_vel_tgn_init(float(line[6]))
                new_body.set_vel_rad_init(float(line[7]))
                new_body.set_long_init(float(line[8]))
                new_body.set_label(str(line[1]))
                new_body.set_color(list(line[2]))
                orbit_init = str(line[9].strip("\n"))
                objects.append(new_body)
                bodies.append(new_body)

                reference_found = False

                for obj in bodies:
                    if obj.get_label() == orbit_init:
                        new_body.set_orbiting_init(obj)
                        reference_found = True

                if not orbit_init or orbit_init == "" or orbit_init == "None":
                    reference_found = True

                if not reference_found:
                    return

            if line[0] == "V":
                line = line.split("|")
                new_vessel = vessel()
                new_vessel.set_alt_init(float(line[3]))
                new_vessel.set_vel_tgn_init(float(line[4]))
                new_vessel.set_vel_rad_init(float(line[5]))
                new_vessel.set_long_init(float(line[6]))
                new_vessel.set_label(str(line[1]))
                new_vessel.set_color(list(line[2]))
                orbit_init = str(line[7].strip("\n"))
                objects.append(new_vessel)
                vessels.append(new_vessel)

                reference_found = False

                for obj in bodies:
                    if obj.get_label() == orbit_init:
                        new_vessel.set_orbiting_init(obj)
                        reference_found = True

                if not orbit_init or orbit_init == "":
                    reference_found = True

                if not reference_found:
                    return
            
    except:
        log_error("Import failed. Check file formatting.", logger="Logs")
        for obj in objects:
            del obj

        for b in bodies:
            del b

        for v in vessels:
            del v
            
        objects, bodies, vessels = [], [], []
        return

    initBodies()
    initVessels()
    updateVisualizer()

    log_info("Import successful.", logger="Logs")

def exportFile():

    global version
    
    if not calc_run_number > 0:
        log_error("Cannot export. Run the calculations first.", logger="Logs")
        return

    show_item("progress_bar")
    setProgressBarOverlay("Attempting export...")
    saveFilename = get_value("filepath_field")

    global vessels, bodies

    # sanitize filename
    if not saveFilename == "" or saveFilename == None:
        log_info("Attempting export...", logger = "Logs")
        if len(saveFilename) > 4 and saveFilename[-4:] == ".txt":
            exportFile = saveFilename
        else:
            exportFile = saveFilename + ".txt"

        setProgressBarOverlay("Saving inputs to TXT...")
        
        #try:
        set_value(name="progress", value=0.50)
        result_file = open(exportFile, "w")
        result_file.write("Save file version " + version + "\n\n")

        for body in bodies:
            save_line = "B|" + str(body.get_label()) + "|" + str(body.get_color()) + "|" + str(body.get_mass()) + "|"
            save_line += str(body.get_radius()) + "|" + str(body.get_alt_init()) + "|"
            save_line += str(body.get_vel_tgn_init()) + "|" + str(body.get_vel_rad_init()) + "|"
            save_line += str(body.get_long_init()) + "|"
            if body.get_orbiting_init():
                save_line += str(body.get_orbiting_init().get_label())
            else:
                save_line += "None"
            save_line += "\n"
            result_file.write(save_line)

        for vessel in vessels:
            save_line = "V|" + str(vessel.get_label()) + "|" + str(vessel.get_color()) + "|" + str(vessel.get_alt_init()) + "|"
            save_line += str(vessel.get_vel_tgn_init()) + "|" + str(vessel.get_vel_rad_init()) + "|"
            save_line += str(vessel.get_long_init()) + "|"
            if vessel.get_orbiting_init():
                save_line += str(vessel.get_orbiting_init().get_label())
            else:
                save_line += "None"
            save_line += "\n"
            result_file.write(save_line)
            
        result_file.close()
        log_info("Inputs saved in " + exportFile, logger = "Logs")
        #except:
           # log_error("TXT export failed.", logger = "Logs")  
        
    else:
        log_warning("No filename provided. Export aborted.", logger = "Logs")
    set_value(name="progress", value=1)
    hide_item("progress_bar")
    log_info("Done.", logger = "Logs")
    set_value(name="progress", value=0)
    setProgressBarOverlay("")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                SIMULATION SETUP
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def lockView(sender, data):
    set_value(name="view_target", value=str(data))

def prevTarget():
    
    global objects, target, target_id
    
    if len(objects) < 1:
        set_value(name="target_name", value="")
        return
    
    else:
        if target_id > 0:
            target_id = target_id - 1
        else:
            target_id = len(objects) - 1
            
        target = objects[target_id]
        set_value(name="target_name", value=target.get_label())

    updateVisualizer()


def nextTarget():
    
    global objects, target, target_id

    if len(objects) < 1:
        set_value(name="target_name", value="")
        return
    
    else:
        if target_id < len(objects) - 1:
            target_id = target_id + 1
        else:
            target_id = 0
            
        target = objects[target_id]
        set_value(name="target_name", value=target.get_label())

    updateVisualizer()

def updateVisualizer():

    global bodies, vessels, objects, target
    
    vis_scale = float(get_value("vis_scale_field"))
    clear_drawing("vis_canvas")

    if get_value("lock_on_target") and not target == None and len(objects) > 1:    
        for vessel in vessels:
            draw_rectangle(drawing="vis_canvas", pmin=space2screen((vessel.get_pos()[0]-target.get_pos()[0])/vis_scale-3,(vessel.get_pos()[1]-target.get_pos()[1])/vis_scale-3,680,380), pmax=space2screen((vessel.get_pos()[0]-target.get_pos()[0])/vis_scale+3,(vessel.get_pos()[1]-target.get_pos()[1])/vis_scale+3,680,380), color=vessel.get_color())
            if get_value("display_labels"):
                draw_text(drawing="vis_canvas", pos=space2screen((vessel.get_pos()[0]-target.get_pos()[0])/vis_scale+6, (vessel.get_pos()[1]-target.get_pos()[1])/vis_scale+6, 680, 380), text=vessel.get_label(), size=12, color=vessel.get_color())

        for body in bodies:
            draw_circle(drawing="vis_canvas", center=space2screen((body.get_pos()[0]-target.get_pos()[0])/vis_scale,(body.get_pos()[1]-target.get_pos()[1])/vis_scale,680,380), radius=(body.get_radius()/vis_scale), color=body.get_color())
            if get_value("display_labels"):
                draw_text(drawing="vis_canvas", pos=space2screen((body.get_pos()[0]-target.get_pos()[0])/vis_scale+3,(body.get_pos()[1]-target.get_pos()[1])/vis_scale+3,680,380), text=body.get_label() , size=14, color=body.get_color())
        
    else:
        for body in bodies:
            draw_circle(drawing="vis_canvas", center=space2screen(body.get_pos()[0]/vis_scale,body.get_pos()[1]/vis_scale,680,380), radius=(body.get_radius()/vis_scale), color=body.get_color())
            if get_value("display_labels"):
                draw_text(drawing="vis_canvas", pos=space2screen(body.get_pos()[0]/vis_scale+3,body.get_pos()[1]/vis_scale+3,680,380), size=14, text=body.get_label(), color=body.get_color())

        for vessel in vessels:
            draw_rectangle(drawing="vis_canvas", pmin=space2screen(vessel.get_pos()[0]/vis_scale-3,vessel.get_pos()[1]/vis_scale-3,680,380), pmax=space2screen(vessel.get_pos()[0]/vis_scale+3,vessel.get_pos()[1]/vis_scale+3,680,380), color=vessel.get_color())
            if get_value("display_labels"):
                draw_text(drawing="vis_canvas", pos=space2screen(vessel.get_pos()[0]/vis_scale+6, vessel.get_pos()[1]/vis_scale+6, 680, 380), size=12, text=vessel.get_label(), color=vessel.get_color())

        # --- --- --- --- --- ---


def disableEndFlag():
    internal_dpg.configure_item("end_flag", enabled=False)

def enableEndFlag():
    internal_dpg.configure_item("end_flag", enabled=True)

def initBodies():
    
    global bodies
    
    for body in bodies:

        # set values to sim setup inputs
        body.set_alt(body.get_alt_init())
        body.set_long(body.get_long_init())
        body.set_vel_tgn(body.get_vel_tgn_init())
        body.set_vel_rad_init(body.get_vel_rad_init())
        
        # body is placed with respect to a reference body
        if not body.get_orbiting_init() == None:
            body.set_pos(sph2cart(body.get_alt(), body.get_long())[0] + body.get_orbiting_init().get_pos()[0],
                         sph2cart(body.get_alt(), body.get_long())[1] + body.get_orbiting_init().get_pos()[1])

            body.set_vel(body.get_vel_rad() * math.cos(math.radians(body.get_long() + 90)) + body.get_vel_tgn() * math.cos(math.radians(body.get_long() + 180)) + body.get_orbiting_init().get_vel()[0],
                         body.get_vel_rad() * math.sin(math.radians(body.get_long() + 90)) + body.get_vel_tgn() * math.sin(math.radians(body.get_long() + 180)) + body.get_orbiting_init().get_vel()[1])
        else:
            # no reference body, place with respect to global coordinates
            body.set_pos(sph2cart(body.get_alt(), body.get_long())[0], sph2cart(body.get_alt(), body.get_long())[1])
            body.set_vel(body.get_vel_rad() * math.cos(math.radians(body.get_long() + 90)) + body.get_vel_tgn() * math.cos(math.radians(body.get_long() + 180)),
                         body.get_vel_rad() * math.sin(math.radians(body.get_long() + 90)) + body.get_vel_tgn() * math.sin(math.radians(body.get_long() + 180)))

def initVessels():
    
    global vessels
    
    for vessel in vessels:

        # set values to sim setup inputs
        vessel.set_orbiting(vessel.get_orbiting_init())
        vessel.set_alt(vessel.get_alt_init())
        vessel.set_long(vessel.get_long_init())
        vessel.set_vel_tgn(vessel.get_vel_tgn_init())
        vessel.set_vel_rad(vessel.get_vel_rad_init())
        
        # vessel is placed with respect to a reference body
        if not vessel.get_orbiting_init() == None:
            vessel.set_pos(sph2cart(vessel.get_alt() + vessel.get_orbiting().get_radius(), vessel.get_long())[0] + vessel.get_orbiting().get_pos()[0],
                           sph2cart(vessel.get_alt() + vessel.get_orbiting().get_radius(), vessel.get_long())[1]+ vessel.get_orbiting().get_pos()[1])

            vessel.set_vel(vessel.get_vel_rad() * math.cos(math.radians(vessel.get_long() + 90)) + vessel.get_vel_tgn() * math.cos(math.radians(vessel.get_long() + 180)) + vessel.get_orbiting().get_vel()[0],
                           vessel.get_vel_rad() * math.sin(math.radians(vessel.get_long() + 90)) + vessel.get_vel_tgn() * math.sin(math.radians(vessel.get_long() + 180)) + vessel.get_orbiting().get_vel()[1])
        else:
            # no reference body, place with respect to global coordinates
            vessel.set_pos(sph2cart(vessel.get_alt(), vessel.get_long())[0],
                           sph2cart(vessel.get_alt(), vessel.get_long())[1])

            vessel.set_vel(vessel.get_vel_rad() * math.cos(math.radians(vessel.get_long() + 90)) + vessel.get_vel_tgn() * math.cos(math.radians(vessel.get_long() + 180)),
                           vessel.get_vel_rad() * math.sin(math.radians(vessel.get_long() + 90)) + vessel.get_vel_tgn() * math.sin(math.radians(vessel.get_long() + 180)))

# Mathematical sub-functions

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

def sign(x): return 1 if x >= 0 else -1

# takes longitude (in degrees) and radial distance, gives relative x and y position
def sph2cart(r, long_theta):
    phi = long_theta + 90
    phi = math.radians(phi)
    
    x = r * math.cos(phi)
    y = r * math.sin(phi)

    return [x, y]

def get_dist(obj1, obj2):
    dist = ((obj1.get_pos()[0] - obj2.get_pos()[0])**2 + (obj1.get_pos()[1] - obj2.get_pos()[1])**2)**(0.5)
    return float(dist)

def simulateOrbit():

    global calc_run_number
    calc_run_number += 1
    log_info(message = "Run [" + str(calc_run_number) + "]: Simulating trajectory...", logger = "Logs")

    global last_run_inputs
    last_run_inputs = []

    global vessels, bodies, objects

    # global simulation inputs
    time_increment = float(get_value("sim_speed_field")/get_value("sim_precision_field"))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                   RUN SIMULATION
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    time = 0

    # reset trajectory data for new simulation
    for obj in objects:
        obj.clear_traj_history()

    # apply gravity to each object, by all bodies in the simulation
    for obj in objects:
        for body in bodies:
            if not obj == body:
                if not obj.get_pos()[0] == body.get_pos()[0] and not obj.get_pos()[1] == body.get_pos()[1]:
                    obj.update_vel(body.get_grav_pull(get_dist(obj, body)) * abs(math.cos(math.atan((obj.get_pos()[1] - body.get_pos()[1])/(obj.get_pos()[0] - body.get_pos()[0])))) * sign(body.get_pos()[0] - obj.get_pos()[0]),
                                   body.get_grav_pull(get_dist(obj, body)) * abs(math.sin(math.atan((obj.get_pos()[1] - body.get_pos()[1])/(obj.get_pos()[0] - body.get_pos()[0])))) * sign(body.get_pos()[1] - obj.get_pos()[1]),
                                   time_increment)
                    
                # x coords same
                elif obj.get_pos()[0] == body.get_pos()[0] and not obj.get_pos()[1] == body.get_pos()[1]:
                    obj.update_vel(0,
                                   body.get_grav_pull(get_dist(obj, body)) * sign(body.get_pos()[1] - obj.get_pos()[1]),
                                   time_increment)

                # y coords same
                elif obj.get_pos()[1] == body.get_pos()[1] and not obj.get_pos()[0] == body.get_pos()[0]:
                    obj.update_vel(body.get_grav_pull(get_dist(obj, body)) * sign(body.get_pos()[0] - obj.get_pos()[0]),
                                   0,
                                   time_increment)
                    
                # both coords same, no need to update velocity for this cycle
                else:
                    pass

    show_item("progress_bar")
    progress_loop = 0
    enableEndFlag()

    clear_plot("traj_plot")

    # --- BEGIN TIMESTEPS ---

    cycle_num = 0
    while (True):
        cycle_num = cycle_num + 1
        cycle_start = t.perf_counter()

        time_increment = float(get_value("sim_speed_field")/get_value("sim_precision_field"))
            
        setSimSpeedLimits()
        setScaleLimits()

        updateVisualizer()

        if progress_loop < 1.0:
            progress_loop = progress_loop + 0.01
        else:
            progress_loop = 0.0

        set_value(name="progress", value=progress_loop)
        setProgressBarOverlay("Simulation running...")

        for obj in objects:
            obj.update_traj()

        # - - - - ITERATIVE PHYSICS HAPPEN HERE - - - -
        # increment time step
        time = time + time_increment

        # apply gravity to each object, by all bodies in the simulation
        for obj in objects:
            for body in bodies:
                if not obj == body:
                    if not obj.get_pos()[0] == body.get_pos()[0] and not obj.get_pos()[1] == body.get_pos()[1]:
                        obj.update_vel(body.get_grav_pull(get_dist(obj, body)) * abs(math.cos(math.atan((obj.get_pos()[1] - body.get_pos()[1])/(obj.get_pos()[0] - body.get_pos()[0])))) * sign(body.get_pos()[0] - obj.get_pos()[0]),
                                       body.get_grav_pull(get_dist(obj, body)) * abs(math.sin(math.atan((obj.get_pos()[1] - body.get_pos()[1])/(obj.get_pos()[0] - body.get_pos()[0])))) * sign(body.get_pos()[1] - obj.get_pos()[1]),
                                       time_increment)
                    
                # x coords same
                elif obj.get_pos()[0] == body.get_pos()[0] and not obj.get_pos()[1] == body.get_pos()[1]:
                    obj.update_vel(0,
                                   body.get_grav_pull(get_dist(obj, body)) * sign(body.get_pos()[1] - obj.get_pos()[1]),
                                   time_increment)

                # y coords same
                elif obj.get_pos()[1] == body.get_pos()[1] and not obj.get_pos()[0] == body.get_pos()[0]:
                    obj.update_vel(body.get_grav_pull(get_dist(obj, body)) * sign(body.get_pos()[0] - obj.get_pos()[0]),
                                   0,
                                   time_increment)
                    
                # both coords same, no need to update velocity for this cycle
                else:
                    pass
                    
                # set sphere of influence to the body that applies most gravity on the vessel
                if type(obj).__name__ == "vessel":
                    if body.get_orbiting_init() and body.get_grav_pull(get_dist(obj, body)) > obj.get_orbiting().get_grav_pull(get_dist(obj, obj.get_orbiting())):
                        obj.set_orbiting(body)

        # update positions
        for obj in objects:
            obj.update_pos(obj.get_vel()[0], obj.get_vel()[1], time_increment)
        # - - - -   - - - -   - - - -   - - - -   - - - -

        # adjust simulation speed
        speed_scale = get_value("sim_speed_field")
        cycle_dt = t.perf_counter() - cycle_start
        try:
            t.sleep((time_increment-cycle_dt)*(1/speed_scale))
        except:
            pass
        
        # update displays
        set_value(name="time", value=time)
        if type(target).__name__ == "vessel" and target.get_orbiting():
            set_value(name="alt", value= (get_dist(target, target.get_orbiting())) - target.get_orbiting().get_radius())
            set_value(name="vel", value= (((target.get_vel()[0] - target.get_orbiting().get_vel()[0])**2 + (target.get_vel()[1] - target.get_orbiting().get_vel()[1])**2)**(0.5)))
            set_value(name="soi", value=target.get_orbiting().get_label())
        elif type(target).__name__ == "body" and target.get_orbiting_init():
            set_value(name="alt", value= (get_dist(target, target.get_orbiting_init())) - target.get_orbiting_init().get_radius())
            set_value(name="vel", value= (((target.get_vel()[0] - target.get_orbiting_init().get_vel()[0])**2 + (target.get_vel()[1] - target.get_orbiting_init().get_vel()[1])**2)**(0.5)))
            set_value(name="soi", value=target.get_orbiting_init().get_label())

        if get_value("realtime_graph"):

            for obj in objects:
                add_line_series(name=str(obj.get_label() + " Traj"), plot="traj_plot", x=obj.get_traj()[0], y=obj.get_traj()[1], color=obj.get_color())

        if get_value("end_flag"):
            disableEndFlag()
            set_value("end_flag", value=False)
            break

    # post-simulation
    setProgressBarOverlay("Updating graphs...")

    for obj in objects:
        add_line_series(name=str(obj.get_label() + " Traj"), plot="traj_plot", x=obj.get_traj()[0], y=obj.get_traj()[1], color=obj.get_color())

    set_value(name="progress", value=0)
    hide_item("progress_bar")
    setProgressBarOverlay("")
    log_info("Simulation completed.", logger="Logs")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                    USER INTERFACE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def space2screen(space_x, space_y, screen_width, screen_height):
    
    screen_x = space_x + screen_width/2
    screen_y = -space_y + screen_height/2

    return [screen_x, screen_y]

# hacky function to update progress bar overlay text
# because dearpygui.simple doesn't have such a solution
def setProgressBarOverlay(overlay_str):
    internal_dpg.configure_item("progress_bar", overlay=overlay_str)

def setSimSpeedLimits():
    internal_dpg.configure_item("sim_speed_field", min_value=float(get_value("sim_speed_min_field")), max_value=float(get_value("sim_speed_max_field")))

def setScaleLimits():
    internal_dpg.configure_item("vis_scale_field", min_value=float(get_value("scale_min_field")), max_value=float(get_value("scale_max_field")))
    updateVisualizer()

#FILE OPERATIONS BAR
with window("File I/O", width=1260, height=60, no_close=True, no_move=True):
    set_window_pos("File I/O", 10, 10)
    add_button("Browse", callback = browseSaves)
    add_same_line()
    add_input_text(name="filepath_field", label="Filepath", tip = "If the file is in the same directory with the script, you don't need\nto write the full path.", width=600)
    add_same_line()
    add_button("Import", callback=importFile)
    add_same_line()
    add_button("Export", callback=exportFile)
    add_same_line()
    add_progress_bar(name="progress_bar", source="progress", width=200, overlay="progress_overlay")
    hide_item("progress_bar")

#INPUTS WINDOW
with window("Input", width=550, height=360, no_close=True):

    set_window_pos("Input", 10, 80)
    
    add_tab_bar(name="input_tab_bar")
    end("input_tab_bar")

    add_tab(name="moon_input_tab", label="Body", parent="input_tab_bar")
    end("moon_input_tab")
    add_tab(name="vessel_input_tab", label="Vessel", parent="input_tab_bar")
    end("vessel_input_tab")

    add_menu_bar("input_menu_bar")
    end("moon_menu_bar")
    add_menu("moon_menu", label="Bodies", parent="input_menu_bar")
    end("moon_menu")
    add_menu("vessel_menu", label="Vessels", parent="input_menu_bar")
    end("vessel_menu")

    # VESSEL INPUTS     
    add_spacing(count=6, parent="vessel_input_tab")
    add_input_text(name="vessel_name", label="Vessel Name", width=175, parent="vessel_input_tab")
    add_color_edit4(name="vessel_color_edit", label="Vessel Visualizer Color", default_value=[200,0,0,255], parent="vessel_input_tab")
    add_spacing(count=6, parent="vessel_input_tab")
    add_input_text("init_orbiting_body_field", label="Initial Frame of Reference", width=175, parent="vessel_input_tab", tip="Leave blank to place relative to global frame.")
    add_input_text(name = "alt_init_field", label = "Initial Altitude (m)", width=175, parent="vessel_input_tab")
    add_input_text(name = "vel_tgn_init_field", label = "Initial Tangential Velocity (m/s)", width=175, parent="vessel_input_tab")
    add_input_text(name = "vel_rad_init_field", label = "Initial Radial Velocity (m/s)", width=175, parent="vessel_input_tab")
    add_input_text(name = "long_init_field", label = "Initial Longitude (degrees)", width=175, parent="vessel_input_tab", tip="Zero at 12 o'clock of orbited body, increases counterclockwise.")
    add_spacing(count=6, parent="vessel_input_tab")
    add_button("examine_vessel_button", label="Examine Setup", callback=examineVesselSetup, parent="vessel_input_tab")
    add_same_line(parent="vessel_input_tab")
    add_button("create_vessel_button", label="Save Setup", callback=saveVesselSetup, parent="vessel_input_tab")
    add_same_line(parent="vessel_input_tab")
    add_button("delete_vessel_button", label="Delete Vessel", callback=deleteVessel, parent="vessel_input_tab")

    # BODY INPUTS  
    add_spacing(count=6, parent="moon_input_tab")
    add_input_text(name="moon_name", label="Body Name", width=150, parent="moon_input_tab")
    add_color_edit4(name="moon_color_edit", label="Body Visualizer Color", default_value=[255,255,255,255], parent="moon_input_tab")
    add_spacing(count=6, parent="moon_input_tab")
    add_input_text(name = "moon_mass_field", label = "", width=175, parent="moon_input_tab")
    add_same_line(parent="moon_input_tab")
    add_text("x 10^", parent="moon_input_tab")
    add_same_line(parent="moon_input_tab")
    add_input_text(name = "moon_mass_magnitude_field", label = "Body Mass (kg)", width=100, parent="moon_input_tab")
    add_input_text(name = "moon_radius_field", label = "", width=175, parent="moon_input_tab")
    add_same_line(parent="moon_input_tab")
    add_text("x 10^",parent="moon_input_tab")
    add_same_line(parent="moon_input_tab")
    add_input_text(name = "moon_radius_magnitude_field", label = "Body Radius (m)", width=100, parent="moon_input_tab")
    add_spacing(count=6,parent="moon_input_tab")
    add_input_text("moon_init_orbiting_body_field", label="Initial Frame of Reference", width=175, parent="moon_input_tab", tip="Leave blank to place relative to global frame.")
    add_input_text(name = "moon_alt_init_field", label = "Initial Distance to Parent (m)", width=100, parent="moon_input_tab", tip="Between body centers.")
    add_input_text(name = "moon_vel_tgn_init_field", label = "Initial Tangential Velocity (m/s)", width=100, parent="moon_input_tab", tip="Rel. to parent body.")
    add_input_text(name = "moon_vel_rad_init_field", label = "Initial Radial Velocity (m/s)", width=100, parent="moon_input_tab", tip="Rel. to parent body.")
    add_input_text(name = "moon_long_init_field", label = "Initial Longitude (degrees)", width=100, parent="moon_input_tab", tip="Zero at 12 o'clock of parent body, increases counterclockwise.")
    add_spacing(count=6, parent="moon_input_tab")
    add_button("examine_moon_button", label="Examine Setup", callback=examineBodySetup, parent="moon_input_tab")
    add_same_line(parent="moon_input_tab")
    add_button("create_moon_button", label="Save Setup", callback=saveBodySetup, parent="moon_input_tab")
    add_same_line(parent="moon_input_tab")
    add_button("delete_moon_button", label="Delete Body", callback=deleteBody, parent="moon_input_tab")

    # spacing
    add_spacing(count=6)
    add_separator()
    add_spacing(count=6)

    # GLOBAL SIMULATION INPUTS
    add_input_text(name="sim_speed_min_field", label= "Min. Sim. Speed", default_value = "0.1", width=100, callback=setSimSpeedLimits)
    add_same_line()
    add_input_text(name="sim_speed_max_field", label= "Max. Sim. Speed", default_value = "100.0", width=100, callback=setSimSpeedLimits)
    add_spacing(count=6)
    add_text("Simulation Speed:")
    add_slider_float(name="sim_speed_field", label="",
                     min_value=float(get_value("sim_speed_min_field")), max_value=float(get_value("sim_speed_max_field")), default_value=1.0,
                     clamped=True, width=500)
    add_spacing(count=6)
    add_text("Simulation Precision:")
    add_slider_float(name="sim_precision_field", label="",
                     min_value=1, max_value=100.0, default_value=10.0,
                     clamped=True, width=500)
    add_button(name="sim_reset_button", label="Reset Simulation", tip="Re-initializes all objects at their starting position and velocities.", callback=resetSimulation)
    add_same_line()
    add_checkbox(name = "realtime_graph", label = "Update graphs every cycle", tip="Looks really cool but significantly reduces performance.")
    add_spacing(count=6)
    add_button("Run Simulation", callback = simulateOrbit)
    add_same_line()
    add_checkbox(name="end_flag", label="Pause Simulation", tip="Raising this flag breaks out of the simulation loop in the next cycle.", enabled=False)

#OUTPUTS WINDOW
with window("Output", width=700, height=560, no_close=True):
    set_window_pos("Output", 570, 80)

    add_tab_bar(name="graph_switch")
    end("graph_switch")
    add_tab(name="vis_tab", label="Visualization", parent="graph_switch")
    end("vis_tab")
    add_tab(name="graphs_tab", label="Graphs", parent="graph_switch")
    end("graphs_tab")

    # VISUALIZER

    add_button(name="prev_target_button", label="<-", parent="vis_tab", callback=prevTarget)
    add_same_line(parent="vis_tab")
    add_input_text(name="selected_target_field", label="", parent="vis_tab", width=500, source="target_name", enabled=False)
    add_same_line(parent="vis_tab")
    add_button(name="next_target_button", label="->", parent="vis_tab", callback=nextTarget)

    add_input_text(name="soi_output", label="Ref. Frame", source="soi", readonly=True, enabled=False, parent="vis_tab", width=300)
    add_same_line(parent="vis_tab")
    add_input_text(name="time_output", label="Time (s)", source="time", readonly=True, enabled=False, parent="vis_tab", width=150)
    add_input_text(name="alt_output", label="Altitude (m)", source="alt", readonly=True, enabled=False, parent="vis_tab", width=200)
    add_same_line(parent="vis_tab")
    add_input_text(name="vel_output", label="Velocity (m/s)", source="vel", readonly=True, enabled=False, parent="vis_tab", width=200)
    #add_input_text(name="dist_output", label="Dist. From Body Center (m)", source="dist", readonly=True, enabled=False, parent="vis_tab")

    add_input_text(name="scale_min_field", label="Scale Min", parent="vis_tab", default_value="1000.0", width=100, callback=setScaleLimits)
    add_same_line(parent="vis_tab")
    add_input_text(name="scale_max_field", label="Scale Max", parent="vis_tab", default_value="10000000.0", width=100, callback=setScaleLimits)
    add_same_line(parent="vis_tab")
    add_checkbox(name="display_labels", label="Show Labels", parent="vis_tab", callback=updateVisualizer)
    
    add_slider_float(name="vis_scale_field", label="Scale (m/pixel)",
                     min_value=float(get_value("scale_min_field")), max_value=float(get_value("scale_max_field")), default_value=50000.0,
                     clamped=True, parent="vis_tab", width=300, callback=updateVisualizer)

    add_same_line(parent="vis_tab")
    add_checkbox(name="lock_on_target", label="Lock View on Selected", parent="vis_tab", enabled=True)

    add_drawing("vis_canvas", parent="vis_tab", width=680, height=380)
    clear_drawing("vis_canvas")

    # GRAPHS
    add_tab_bar(name="output_tabs", parent="graphs_tab")
    end("output_tabs")

    add_tab(name="traj_tab", label="Trajectory", parent="output_tabs")
    end("traj_tab")

    add_plot(name="traj_plot", label="Trajectory",
             x_axis_name="X (m)", y_axis_name = "Y (m)", anti_aliased=True, parent="traj_tab", equal_aspects=True)

#LOG WINDOW
with window("Log", width=550, height=190, no_close=True):
    set_window_pos("Log", 10, 450)
    add_logger("Logs", log_level=0, autosize_x = True, autosize_y = True)

start_dearpygui()
