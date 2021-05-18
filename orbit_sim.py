#   2D N-BODY ORBIT SIMULATOR

version = "0.4.1"

from dearpygui.core import *
from dearpygui.simple import *
import math
import pandas as pd
import time as t
import scipy.constants as scp_const
import numpy as npy

#set initial window configuration (purely cosmetic)
set_main_window_size(1300, 700)
set_main_window_title("N-body Orbit Sim 2D | MRS")
set_theme("Dark")

calc_run_number = 0

grav_const = scp_const.G

set_value(name="progress", value=0)

#save latest simulation inputs in global variables - for export if required

last_run_inputs = []

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                 FILE IMPORT/EXPORT
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def importFile():

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

        # import vessel settings
        set_value(name="alt_init_field", value=import_lines[4][18:-3])
        set_value(name="vel_tgn_init_field", value=import_lines[5][29:-5])
        set_value(name="vel_rad_init_field", value=import_lines[6][25:-5])
        set_value(name="long_init_field", value=import_lines[7][19:-4])
        set_value(name="vessel_name", value=import_lines[8][14:-1])
        set_value(name="vessel_color_edit", value=list(import_lines[9][14:-1]))
        set_value(name="init_orbiting_body_field", value=int(import_lines[10][27:-1]))

        # import parent body
        set_value(name="body_mass_field", value=import_lines[13][18:-4])
        set_value(name="body_mass_magnitude_field", value="0")
        set_value(name="body_radius_field", value=import_lines[14][20:-3])
        set_value(name="body_radius_magnitude_field", value="0")
        set_value(name="parent_name", value=import_lines[15][18:-1])
        set_value(name="parent_color_edit", value=list(import_lines[16][19:-1]))

        # import body_b
        if import_lines[18][18:-1] == "True":
            set_value(name="moon1_check", value=True)
            set_value(name="moon1_mass_field", value=import_lines[19][13:-4])
            set_value(name="moon1_mass_magnitude_field", value="0")
            set_value(name="moon1_radius_field", value=import_lines[20][15:-3])
            set_value(name="moon1_radius_magnitude_field", value="0")
            set_value(name="moon1_alt_init_field", value=import_lines[21][23:-3])
            set_value(name="moon1_vel_tgn_init_field", value=import_lines[22][30:-5])
            set_value(name="moon1_vel_rad_init_field", value=import_lines[23][26:-5])
            set_value(name="moon1_long_init_field", value=import_lines[24][20:-5])
            set_value(name="moon1_name", value=import_lines[25][13:-1])
            set_value(name="moon1_color_edit", value=list(import_lines[26][14:-1]))
        else:
            set_value(name="moon1_check", value=False)

        # import body_c
        if import_lines[28][18:-1] == "True":
            set_value(name="moon2_check", value=True)
            set_value(name="moon2_mass_field", value=import_lines[29][13:-4])
            set_value(name="moon2_mass_magnitude_field", value="0")
            set_value(name="moon2_radius_field", value=import_lines[30][15:-3])
            set_value(name="moon2_radius_magnitude_field", value="0")
            set_value(name="moon2_alt_init_field", value=import_lines[31][23:-3])
            set_value(name="moon2_vel_tgn_init_field", value=import_lines[32][30:-5])
            set_value(name="moon2_vel_rad_init_field", value=import_lines[33][26:-5])
            set_value(name="moon2_long_init_field", value=import_lines[34][20:-5])
            set_value(name="moon2_name", value=import_lines[35][13:-1])
            set_value(name="moon2_color_edit", value=list(import_lines[36][14:-1]))
        else:
            set_value(name="moon2_check", value=False)
            
    except:
        log_error("Import failed. Check file formatting.", logger="Logs")
        return

    log_info("Import successful.", logger="Logs")

def exportFile():

    global version
    
    if not calc_run_number > 0:
        log_error("Cannot export. Run the calculations first.", logger="Logs")
        return

    show_item("progress_bar")
    setProgressBarOverlay("Attempting export...")
    saveFilename = get_value("filepath_field")

    # sanitize filename
    if not saveFilename == "" or saveFilename == None:
        log_info("Attempting export...", logger = "Logs")
        if len(saveFilename) > 4 and saveFilename[-4:] == ".txt":
            exportFile = saveFilename
        else:
            exportFile = saveFilename + ".txt"

        setProgressBarOverlay("Saving inputs to TXT...")
        
        # Save given inputs to TXT
        # last_run_inputs = [vessel_a, body_a, body_b, body_c]

        global last_run_inputs
        vessel_data = last_run_inputs[0]
        body_a_data = last_run_inputs[1]
        body_b_data = last_run_inputs[2]
        body_c_data = last_run_inputs[3]
        
        try:
            set_value(name="progress", value=0.50)
            result_file = open(exportFile, "w")
            result_file.write("Save file version " + version + "\n\n")
            result_file.write("INPUTS\n\n")

            # vessel inputs
            result_file.write("Initial altitude: ")
            result_file.write(str(vessel_data[0])+" m\n")
            result_file.write("Initial tangential velocity: ")
            result_file.write(str(vessel_data[1])+" m/s\n")
            result_file.write("Initial radial velocity: ")
            result_file.write(str(vessel_data[2])+" m/s\n")
            result_file.write("Initial longitude: ")
            result_file.write(str(vessel_data[3])+" deg\n")
            result_file.write("Vessel label: ")
            result_file.write(str(vessel_data[4])+"\n")
            result_file.write("Vessel color: ")
            result_file.write(str(vessel_data[5])+"\n")
            result_file.write("Initially orbiting body #: ")
            result_file.write(str(vessel_data[6])+"\n\n")

            # parent body inputs
            result_file.write("Parent body existence: ")
            result_file.write(str(body_a_data[0])+"\n")
            result_file.write("Parent body mass: ")
            result_file.write(str(body_a_data[1])+" kg\n")
            result_file.write("Parent body radius: ")
            result_file.write(str(body_a_data[2])+" m\n")
            result_file.write("Parent body name: ")
            result_file.write(str(body_a_data[3])+"\n")
            result_file.write("Parent body color: ")
            result_file.write(str(body_a_data[4])+"\n\n")

            # body_b inputs
            result_file.write("Body B existence: ")
            result_file.write(str(body_b_data[0])+"\n")
            result_file.write("Body B mass: ")
            result_file.write(str(body_b_data[1])+" kg\n")
            result_file.write("Body B radius: ")
            result_file.write(str(body_b_data[2])+" m\n")
            result_file.write("Body B init. altitude: ")
            result_file.write(str(body_b_data[3])+" m\n")
            result_file.write("Body B init. tangential vel.: ")
            result_file.write(str(body_b_data[4])+" m/s\n")
            result_file.write("Body B init. radial vel.: ")
            result_file.write(str(body_b_data[5])+" m/s\n")
            result_file.write("Body B init. long.: ")
            result_file.write(str(body_b_data[6])+" deg\n")
            result_file.write("Body B name: ")
            result_file.write(str(body_b_data[7])+"\n")
            result_file.write("Body B color: ")
            result_file.write(str(body_b_data[8])+"\n\n")

            # body_c inputs
            result_file.write("Body C existence: ")
            result_file.write(str(body_c_data[0])+"\n")
            result_file.write("Body C mass: ")
            result_file.write(str(body_c_data[1])+" kg\n")
            result_file.write("Body C radius: ")
            result_file.write(str(body_c_data[2])+" m\n")
            result_file.write("Body C init. altitude: ")
            result_file.write(str(body_c_data[3])+" m\n")
            result_file.write("Body C init. tangential vel.: ")
            result_file.write(str(body_c_data[4])+" m/s\n")
            result_file.write("Body C init. radial vel.: ")
            result_file.write(str(body_c_data[5])+" m/s\n")
            result_file.write("Body C init. long.: ")
            result_file.write(str(body_c_data[6])+" deg\n")
            result_file.write("Body C name: ")
            result_file.write(str(body_c_data[7])+"\n")
            result_file.write("Body C color: ")
            result_file.write(str(body_c_data[8])+"\n\n")
            
            result_file.close()
            log_info("Inputs saved in " + exportFile, logger = "Logs")
        except:
            log_error("TXT export failed.", logger = "Logs")  
        
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

def disableEndFlag():
    internal_dpg.configure_item("end_flag", enabled=False)

def enableEndFlag():
    internal_dpg.configure_item("end_flag", enabled=True)

def simulateOrbit():

    class body:

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

        def set_alt (self, altitude):
            self.alt = altitude

        def get_alt (self):
            return self.alt

        def set_long (self, longitude):
            self.long = longitude

        def get_long (self):
            return self.long

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

    class vessel ():

        def __init__(self):
            self.pos_x = 0
            self.pos_y = 0
            self.vel_y = 0
            self.vel_x = 0
            self.orbiting = None
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

        def set_alt (self, altitude):
            self.alt = altitude

        def get_alt (self):
            return self.alt

        def set_long (self, longitude):
            self.long = longitude

        def get_long (self):
            return self.long

        def set_vel_tgn (self, velocity):
            self.vel_tgn = velocity

        def get_vel_tgn (self):
            return self.vel_tgn

        def set_vel_rad (self, velocity):
            self.vel_rad = velocity

        def get_vel_rad (self):
            return self.vel_rad

        def set_orbiting (self, body):
            self.orbiting = body

        def get_orbiting (self):
            return self.orbiting

    global calc_run_number
    calc_run_number += 1
    log_info(message = "Run [" + str(calc_run_number) + "]: Simulating trajectory...", logger = "Logs")

    global last_run_inputs
    last_run_inputs = []

    # set vessel values
    vessel_a = vessel()
    vessel_a.set_alt(float(get_value("alt_init_field")))
    vessel_a.set_vel_tgn(float(get_value("vel_tgn_init_field")))
    vessel_a.set_vel_rad(float(get_value("vel_rad_init_field")))
    vessel_a.set_long(float(get_value("long_init_field")))
    vessel_a.set_label(str(get_value("vessel_name")))
    vessel_a.set_color(get_value("vessel_color_edit"))

    # save simulation inputs for export
    last_run_inputs.append([vessel_a.get_alt(), vessel_a.get_vel_tgn(), vessel_a.get_vel_rad(), vessel_a.get_long(), vessel_a.get_label(), vessel_a.get_color()])
    
    # create bodies
    body_a = body()
    body_b = body()
    body_c = body()

    # create parent body
    body_a.set_exists(True)
    body_a.set_mass(float(get_value("body_mass_field")) * 10**float((get_value("body_mass_magnitude_field"))))
    body_a.set_radius(float(get_value("body_radius_field")) * 10**float((get_value("body_radius_magnitude_field"))))
    body_a.set_pos(0, 0)
    body_a.set_vel(0, 0)
    body_a.set_label(str(get_value("parent_name")))
    body_a.set_color(get_value("parent_color_edit"))

    last_run_inputs.append([body_a.does_exist(), body_a.get_mass(), body_a.get_radius(), body_a.get_label(), body_a.get_color()])

    # moon 1
    body_b.set_exists(get_value("moon1_check"))
    if body_b.does_exist():
        body_b.set_mass(float(get_value("moon1_mass_field")) * 10**float((get_value("moon1_mass_magnitude_field"))))
        body_b.set_radius(float(get_value("moon1_radius_field")) * 10**float((get_value("moon1_radius_magnitude_field"))))
        body_b.set_alt(float(get_value("moon1_alt_init_field")))
        body_b.set_vel_tgn(float(get_value("moon1_vel_tgn_init_field")))
        body_b.set_vel_rad(float(get_value("moon1_vel_rad_init_field")))
        body_b.set_long(float(get_value("moon1_long_init_field")))
        body_b.set_label(str(get_value("moon1_name")))
        body_b.set_color(get_value("moon1_color_edit"))

    last_run_inputs.append([body_b.does_exist(), body_b.get_mass(), body_b.get_radius(), body_b.get_alt(), body_b.get_vel_tgn(), body_b.get_vel_rad(), body_b.get_long(), body_b.get_label(), body_b.get_color()])

    body_c.set_exists(get_value("moon2_check"))
    if body_c.does_exist():
        body_c.set_mass(float(get_value("moon2_mass_field")) * 10**float((get_value("moon2_mass_magnitude_field"))))
        body_c.set_radius(float(get_value("moon2_radius_field")) * 10**float((get_value("moon2_radius_magnitude_field"))))
        body_c.set_alt(float(get_value("moon2_alt_init_field")))
        body_c.set_vel_tgn(float(get_value("moon2_vel_tgn_init_field")))
        body_c.set_vel_rad(float(get_value("moon2_vel_rad_init_field")))
        body_c.set_long(float(get_value("moon2_long_init_field")))
        body_c.set_label(str(get_value("moon2_name")))
        body_c.set_color(get_value("moon2_color_edit"))

    last_run_inputs.append([body_c.does_exist(), body_c.get_mass(), body_c.get_radius(), body_c.get_alt(), body_c.get_vel_tgn(), body_c.get_vel_rad(), body_c.get_long(), body_c.get_label(), body_c.get_color()])

    orbit_init = int(get_value("init_orbiting_body_field"))
    last_run_inputs[0].append(orbit_init)

    if orbit_init == 0:
        vessel_a.set_orbiting(body_a)
    elif orbit_init == 1:
        vessel_a.set_orbiting(body_b)
    else:
        vessel_a.set_orbiting(body_c)

    # global simulation inputs
    time_increment = float(get_value("sim_speed_field")/get_value("sim_precision_field"))

    log_info("Inputs:\n" +          
             "Vessel Init. Alt.: " + str(vessel_a.get_alt()) + " m\n"
             "Vessel Init. Tgn. Vel.: " + str(vessel_a.get_vel_tgn()) + " m/s\n"
             "Vessel Init. Rad. Vel.: " + str(vessel_a.get_vel_rad()) + " m/s\n"
             "Vessel Init. Long.: " + str(vessel_a.get_long()) + " deg\n"
             "Vessel Name: " + str(vessel_a.get_label()) + "\n"
             "Vessel Color: " + str(vessel_a.get_color()) + "\n\n", logger = "Logs")

    # Calculation sub-functions

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
         

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                   RUN SIMULATION
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    #set initial values

    time = 0

    vessels = [vessel_a]
    moons = [body_b, body_c]
    bodies = [body_a, body_b, body_c]
    objects = [vessel_a, body_a, body_b, body_c]

    # initiate moons
    for moon in moons:
        if moon.does_exist(): 
            moon.set_pos(sph2cart(moon.get_alt(), moon.get_long())[0], sph2cart(moon.get_alt(), moon.get_long())[1])
            moon.set_vel(moon.get_vel_rad() * math.cos(math.radians(moon.get_long() + 90)) + moon.get_vel_tgn() * math.cos(math.radians(moon.get_long() + 180)),
                         moon.get_vel_rad() * math.sin(math.radians(moon.get_long() + 90)) + moon.get_vel_tgn() * math.sin(math.radians(moon.get_long() + 180)))

    # initiate vessel
    vessel_a.set_pos(sph2cart(vessel_a.get_alt() + vessel_a.get_orbiting().get_radius(), vessel_a.get_long())[0] + vessel_a.get_orbiting().get_pos()[0],
                   sph2cart(vessel_a.get_alt() + vessel_a.get_orbiting().get_radius(), vessel_a.get_long())[1]+ vessel_a.get_orbiting().get_pos()[1])

    vessel_a.set_vel(vessel_a.get_vel_rad() * math.cos(math.radians(vessel_a.get_long() + 90)) + vessel_a.get_vel_tgn() * math.cos(math.radians(vessel_a.get_long() + 180)) + vessel_a.get_orbiting().get_vel()[0],
                     vessel_a.get_vel_rad() * math.sin(math.radians(vessel_a.get_long() + 90)) + vessel_a.get_vel_tgn() * math.sin(math.radians(vessel_a.get_long() + 180)) + vessel_a.get_orbiting().get_vel()[1])

    # reset trajectory data for new simulation
    for obj in objects:
        obj.clear_traj_history()

    # apply gravity to each object, by all bodies in the simulation
    for obj in objects:
        for body in bodies:
            if obj.does_exist() and body.does_exist() and not obj == body:
                obj.update_vel(body.get_grav_pull(get_dist(obj, body)) * abs(math.cos(math.atan((obj.get_pos()[1] - body.get_pos()[1])/(obj.get_pos()[0] - body.get_pos()[0])))) * sign(body.get_pos()[0] - obj.get_pos()[0]),
                               body.get_grav_pull(get_dist(obj, body)) * abs(math.sin(math.atan((obj.get_pos()[1] - body.get_pos()[1])/(obj.get_pos()[0] - body.get_pos()[0])))) * sign(body.get_pos()[1] - obj.get_pos()[1]),
                               time_increment)
                            
        
    time_list = []
    alt_list = []
    vel_list = []
##    vel_rad_list = []
##    vel_tgn_list = []

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

        # --- update visualizer ---

        vis_scale = float(get_value("vis_scale_field"))
        clear_drawing("vis_canvas")

        if get_value("lock_on_vessel"):
            # draw vessel
            for vessel in vessels:
                if vessel.does_exist():
                    draw_rectangle(drawing="vis_canvas", pmin=space2screen(-3,-3,680,380), pmax=space2screen(3,3,680,380), color=vessel.get_color())
                    if get_value("display_labels"):
                        draw_text(drawing="vis_canvas", pos=space2screen(6, 6, 680, 380), text=vessel.get_label(), size=12, color=vessel.get_color())

            # draw planet
            for body in bodies:
                if body.does_exist():
                    draw_circle(drawing="vis_canvas", center=space2screen((body.get_pos()[0]-vessel_a.get_pos()[0])/vis_scale,(body.get_pos()[1]-vessel_a.get_pos()[1])/vis_scale,680,380), radius=(body.get_radius()/vis_scale), color=body.get_color())
                    if get_value("display_labels"):
                        draw_text(drawing="vis_canvas", pos=space2screen((body.get_pos()[0]-vessel_a.get_pos()[0])/vis_scale+3,(body.get_pos()[1]-vessel_a.get_pos()[1])/vis_scale+3,680,380), text=body.get_label() , size=14, color=body.get_color())
            
        else:
            for body in bodies:
                if body.does_exist():
                    draw_circle(drawing="vis_canvas", center=space2screen(body.get_pos()[0]/vis_scale,body.get_pos()[1]/vis_scale,680,380), radius=(body.get_radius()/vis_scale), color=body.get_color())
                    if get_value("display_labels"):
                        draw_text(drawing="vis_canvas", pos=space2screen(body.get_pos()[0]/vis_scale+3,body.get_pos()[1]/vis_scale+3,680,380), size=14, text=body.get_label(), color=body.get_color())

            for vessel in vessels:
                if vessel.does_exist():
                    draw_rectangle(drawing="vis_canvas", pmin=space2screen(vessel.get_pos()[0]/vis_scale-3,vessel.get_pos()[1]/vis_scale-3,680,380), pmax=space2screen(vessel.get_pos()[0]/vis_scale+3,vessel.get_pos()[1]/vis_scale+3,680,380), color=vessel.get_color())
                    if get_value("display_labels"):
                        draw_text(drawing="vis_canvas", pos=space2screen(vessel.get_pos()[0]/vis_scale+6, vessel.get_pos()[1]/vis_scale+6, 680, 380), size=12, text=vessel.get_label(), color=vessel.get_color())

        # --- --- --- --- --- ---

        if progress_loop < 1.0:
            progress_loop = progress_loop + 0.01
        else:
            progress_loop = 0.0

        set_value(name="progress", value=progress_loop)
        setProgressBarOverlay("Simulation running...")

        # update lists
        time_list.append(time)
        alt_list.append(vessel_a.get_alt())
        vel_list.append((vessel_a.get_vel()[0]**2 + vessel_a.get_vel()[1]**2)**(0.5))

        for obj in objects:
            if obj.does_exist():
                obj.update_traj()

        # - - - - ITERATIVE PHYSICS HAPPEN HERE - - - -
        # increment time step
        time = time + time_increment

        # apply gravity to each object, by all bodies in the simulation
        for obj in objects:
            for body in bodies:
                if obj.does_exist() and body.does_exist() and not obj == body:
                    obj.update_vel(body.get_grav_pull(get_dist(obj, body)) * abs(math.cos(math.atan((obj.get_pos()[1] - body.get_pos()[1])/(obj.get_pos()[0] - body.get_pos()[0])))) * sign(body.get_pos()[0] - obj.get_pos()[0]),
                                   body.get_grav_pull(get_dist(obj, body)) * abs(math.sin(math.atan((obj.get_pos()[1] - body.get_pos()[1])/(obj.get_pos()[0] - body.get_pos()[0])))) * sign(body.get_pos()[1] - obj.get_pos()[1]),
                                   time_increment)
                    
                # set sphere of influence to the body that applies most gravity on the vessel
                if type(obj).__name__ == "vessel":
                    if body.get_grav_pull(get_dist(obj, body)) > obj.get_orbiting().get_grav_pull(get_dist(obj, obj.get_orbiting())):
                        obj.set_orbiting(body)

        # update positions
        for obj in objects:
            if obj.does_exist():
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
        set_value(name="alt", value= (get_dist(vessel_a, vessel_a.get_orbiting())) - vessel_a.get_orbiting().get_radius())
        set_value(name="vel", value= (((vessel_a.get_vel()[0] - vessel_a.get_orbiting().get_vel()[0])**2 + (vessel_a.get_vel()[1] - vessel_a.get_orbiting().get_vel()[1])**2)**(0.5)))
        set_value(name="time", value=time)
        set_value(name="soi", value=vessel_a.get_orbiting().get_label())

        if get_value("realtime_graph"):
            add_line_series(name="Altitude", plot="alt_plot",x=time_list, y=alt_list)
            add_line_series(name="Velocity", plot="vel_plot",x=time_list, y=vel_list)

            for obj in objects:
                if obj.does_exist():
                    add_line_series(name=str(obj.get_label() + " Traj"), plot="traj_plot", x=obj.get_traj()[0], y=obj.get_traj()[1], color=obj.get_color())

        if get_value("end_flag"):
            disableEndFlag()
            set_value("end_flag", value=False)
            break

    # post-simulation
    setProgressBarOverlay("Updating graphs...")
    add_line_series(name="Altitude", plot="alt_plot",x=time_list, y=alt_list)
    add_line_series(name="Velocity", plot="vel_plot",x=time_list, y=vel_list)

    for obj in objects:
        if obj.does_exist():
            add_line_series(name=str(obj.get_label() + " Traj"), plot="traj_plot", x=obj.get_traj()[0], y=obj.get_traj()[1], color=obj.get_color())

    set_value(name="progress", value=0)
    hide_item("progress_bar")
    setProgressBarOverlay("")
    log_info("Simulation completed.", logger="Logs")

##    global last_results
##    last_results = [time_list, alt_list, vel_list, pos_x_list, pos_y_list]

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

#FILE OPERATIONS BAR
with window("File I/O", width=1260, height=60, no_close=True, no_move=True):
    set_window_pos("File I/O", 10, 10)
    add_input_text(name="filepath_field", label="Filepath", tip = "If the file is in the same directory with the script, you don't need\nto write the full path.")
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

    add_tab(name="vessel_input_tab", label="Vessel", parent="input_tab_bar")
    end("vessel_input_tab")
    add_tab(name="main_body_input_tab", label="Parent Body", parent="input_tab_bar")
    end("main_body_input_tab")
    add_tab(name="moon1_input_tab", label="Moon 1", parent="input_tab_bar")
    end("moon1_input_tab")
    add_tab(name="moon2_input_tab", label="Moon 2", parent="input_tab_bar")
    end("moon2_input_tab")

    # VESSEL INPUTS
    add_spacing(count=6, parent="vessel_input_tab")
    add_text("Initially orbiting:", parent="vessel_input_tab")
    add_radio_button(name = "init_orbiting_body_field", items=["Parent Body", "Moon 1", "Moon 2"], parent="vessel_input_tab")
    add_spacing(count=6, parent="vessel_input_tab")
    add_input_text(name = "alt_init_field", label = "Initial Altitude (m)", width=175, parent="vessel_input_tab")
    add_input_text(name = "vel_tgn_init_field", label = "Init. Tangential Vel. (m/s)", width=175, parent="vessel_input_tab")
    add_input_text(name = "vel_rad_init_field", label = "Init. Radial Vel. (m/s)", width=175, parent="vessel_input_tab")
    add_spacing(count=6, parent="vessel_input_tab")
    add_input_text(name = "long_init_field", label = "Init. Longitude (degrees)", width=175, parent="vessel_input_tab", tip="Zero at 12 o'clock of orbited body, increases counterclockwise.")
    add_spacing(count=6, parent="vessel_input_tab")
    add_separator(parent="vessel_input_tab")
    add_spacing(count=6, parent="vessel_input_tab")
    add_input_text(name="vessel_name", label="Vessel Name", width=150, parent="vessel_input_tab")
    add_color_edit4(name="vessel_color_edit", label="Vessel Visualizer Color", default_value=[200,0,0,255], parent="vessel_input_tab")

    # PARENT BODY INPUTS
    add_spacing(count=6, parent="main_body_input_tab")
    add_input_text(name = "body_mass_field", label = "", width=175, parent="main_body_input_tab")
    add_same_line(parent="main_body_input_tab")
    add_text("x 10^", parent="main_body_input_tab")
    add_same_line(parent="main_body_input_tab")
    add_input_text(name = "body_mass_magnitude_field", label = "Body Mass (kg)", width=100, parent="main_body_input_tab")
    add_input_text(name = "body_radius_field", label = "", width=175, parent="main_body_input_tab")
    add_same_line(parent="main_body_input_tab")
    add_text("x 10^",parent="main_body_input_tab")
    add_same_line(parent="main_body_input_tab")
    add_input_text(name = "body_radius_magnitude_field", label = "Body Radius (m)", width=100, parent="main_body_input_tab")
    add_spacing(count=6, parent="main_body_input_tab")
    add_separator(parent="main_body_input_tab")
    add_spacing(count=6, parent="main_body_input_tab")
    add_input_text(name="parent_name", label="Body Name", width=150, parent="main_body_input_tab")
    add_color_edit4(name="parent_color_edit", label="Body Visualizer Color", default_value=[255,255,255,255], parent="main_body_input_tab")

    # MOON 1 INPUTS
    add_spacing(count=6, parent="moon1_input_tab")
    add_checkbox(name="moon1_check", label="Enable Moon 1", parent="moon1_input_tab")
    add_spacing(count=6, parent="moon1_input_tab")
    add_input_text(name = "moon1_mass_field", label = "", width=175, parent="moon1_input_tab")
    add_same_line(parent="moon1_input_tab")
    add_text("x 10^", parent="moon1_input_tab")
    add_same_line(parent="moon1_input_tab")
    add_input_text(name = "moon1_mass_magnitude_field", label = "Body Mass (kg)", width=100, parent="moon1_input_tab")
    add_input_text(name = "moon1_radius_field", label = "", width=175, parent="moon1_input_tab")
    add_same_line(parent="moon1_input_tab")
    add_text("x 10^",parent="moon1_input_tab")
    add_same_line(parent="moon1_input_tab")
    add_input_text(name = "moon1_radius_magnitude_field", label = "Body Radius (m)", width=100, parent="moon1_input_tab")
    add_spacing(count=6,parent="moon1_input_tab")
    add_input_text(name = "moon1_alt_init_field", label = "Initial Distance to Parent (m)", width=100, parent="moon1_input_tab", tip="Between body centers.")
    add_input_text(name = "moon1_vel_tgn_init_field", label = "Init. Tangential Vel. (m/s)", width=100, parent="moon1_input_tab", tip="Rel. to parent body.")
    add_input_text(name = "moon1_vel_rad_init_field", label = "Init. Radial Vel. (m/s)", width=100, parent="moon1_input_tab", tip="Rel. to parent body.")
    add_spacing(count=6,parent="moon1_input_tab")
    add_input_text(name = "moon1_long_init_field", label = "Init. Longitude (degrees)", width=100, parent="moon1_input_tab", tip="Zero at 12 o'clock of parent body, increases counterclockwise.")
    add_spacing(count=6, parent="moon1_input_tab")
    add_separator(parent="moon1_input_tab")
    add_spacing(count=6, parent="moon1_input_tab")
    add_input_text(name="moon1_name", label="Body Name", width=150, parent="moon1_input_tab")
    add_color_edit4(name="moon1_color_edit", label="Body Visualizer Color", default_value=[255,255,255,255], parent="moon1_input_tab")

    # MOON 2 INPUTS
    add_spacing(count=6, parent="moon2_input_tab")
    add_checkbox(name="moon2_check", label="Enable Moon 2", parent="moon2_input_tab")
    add_spacing(count=6, parent="moon2_input_tab")
    add_input_text(name = "moon2_mass_field", label = "", width=175, parent="moon2_input_tab")
    add_same_line(parent="moon2_input_tab")
    add_text("x 10^", parent="moon2_input_tab")
    add_same_line(parent="moon2_input_tab")
    add_input_text(name = "moon2_mass_magnitude_field", label = "Body Mass (kg)", width=100, parent="moon2_input_tab")
    add_input_text(name = "moon2_radius_field", label = "", width=175, parent="moon2_input_tab")
    add_same_line(parent="moon2_input_tab")
    add_text("x 10^", parent="moon2_input_tab")
    add_same_line(parent="moon2_input_tab")
    add_input_text(name = "moon2_radius_magnitude_field", label = "Body Radius (m)", width=100, parent="moon2_input_tab")
    add_spacing(count=6,parent="moon2_input_tab")
    add_input_text(name = "moon2_alt_init_field", label = "Initial Distance to Parent (m)", width=100, parent="moon2_input_tab", tip="Between body centers.")
    add_input_text(name = "moon2_vel_tgn_init_field", label = "Init. Tangential Vel. (m/s)", width=100, parent="moon2_input_tab", tip="Rel. to parent body.")
    add_input_text(name = "moon2_vel_rad_init_field", label = "Init. Radial Vel. (m/s)", width=100, parent="moon2_input_tab", tip="Rel. to parent body.")
    add_spacing(count=6,parent="moon2_input_tab")
    add_input_text(name = "moon2_long_init_field", label = "Init. Longitude (degrees)", width=100, parent="moon2_input_tab", tip="Zero at 12 o'clock of parent body, increases counterclockwise.")
    add_spacing(count=6, parent="moon2_input_tab")
    add_separator(parent="moon2_input_tab")
    add_spacing(count=6, parent="moon2_input_tab")
    add_input_text(name="moon2_name", label="Body Name", width=150, parent="moon2_input_tab")
    add_color_edit4(name="moon2_color_edit", label="Body Visualizer Color", default_value=[255,255,255,255], parent="moon2_input_tab")

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
    add_checkbox(name = "realtime_graph", label = "Update graphs every cycle", tip="Looks really cool but significantly reduces performance.")
    add_spacing(count=6)
    add_button("Simulate Orbit", callback = simulateOrbit)
    add_same_line()
    add_checkbox(name="end_flag", label="End Simulation", tip="Raising this flag breaks out of the simulation loop in the next cycle.", enabled=False)

#OUTPUTS WINDOW
with window("Output", width=700, height=560, no_close=True):
    set_window_pos("Output", 570, 80)

    add_tab_bar(name="graph_switch")
    end("graph_switch")
    add_tab(name="graphs_tab", label="Graphs", parent="graph_switch")
    end("graphs_tab")
    add_tab(name="vis_tab", label="Visualization", parent="graph_switch")
    end("vis_tab")

    # VISUALIZER

    add_input_text(name="soi_output", label="SoI", source="soi", readonly=True, enabled=False, parent="vis_tab", width=300)
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
    add_checkbox(name="display_labels", label="Show Labels", parent="vis_tab")
    
    add_slider_float(name="vis_scale_field", label="Scale (m/pixel)",
                     min_value=float(get_value("scale_min_field")), max_value=float(get_value("scale_max_field")), default_value=50000.0,
                     clamped=True, parent="vis_tab", width=300)

    add_same_line(parent="vis_tab")
    add_checkbox(name="lock_on_vessel", label="Lock View on Vessel", parent="vis_tab")

    add_drawing("vis_canvas", parent="vis_tab", width=680, height=380)
    clear_drawing("vis_canvas")

    # GRAPHS
    add_tab_bar(name="output_tabs", parent="graphs_tab")
    end("output_tabs")

    add_tab(name="traj_tab", label="Trajectory", parent="output_tabs")
    end("traj_tab")
    add_tab(name="alt_tab", label="Altitude", parent="output_tabs")
    end("alt_tab")
    add_tab(name="vel_tab", label="Velocity", parent="output_tabs")
    end("vel_tab")
##    add_tab(name="vertical_rate_tab", label="Vert. Rate", parent="output_tabs")
##    end("vertical_rate_tab")
##    add_tab(name="tangential_rate_tab", label="Tgnt. Vel.", parent="output_tabs")
##    end("tangential_rate_tab")
    add_tab(name="params_tab", label="Params.", parent="output_tabs")
    end("params_tab")

    add_plot(name="traj_plot", label="Trajectory",
             x_axis_name="X (m)", y_axis_name = "Y (m)", anti_aliased=True, parent="traj_tab", equal_aspects=True)
    add_input_text(name = "apoapsis_output_field", label = "Apoapsis (m)",
                   source="apoapsis", readonly=True, enabled=False, parent ="alt_tab")
    add_input_text(name = "periapsis_output_field", label = "Periapsis (m)",
                   source="periapsis", readonly=True, enabled=False, parent ="alt_tab")
    add_plot(name="alt_plot", label="Altitude vs Time",
             x_axis_name="Time (s)", y_axis_name = "Altitude (m)", anti_aliased=True, parent="alt_tab")

    add_input_text(name = "vel_max_output_field", label = "Max. Velocity (m/s)",
                   source="vel_max", readonly=True, enabled=False, parent ="vel_tab")
    add_input_text(name = "vel_min_output_field", label = "Min. Velocity (m/s)",
                   source="vel_min", readonly=True, enabled=False, parent ="vel_tab")
    add_plot(name="vel_plot", label="Velocity vs Time",
             x_axis_name="Time (s)", y_axis_name = "Velocity (m/s)", anti_aliased=True, parent="vel_tab")

##    add_plot(name="vert_rate_plot", label="Vertical Rate vs Time",
##             x_axis_name="Time (s)", y_axis_name = "Vertical Rate (m/s)", anti_aliased=True, parent="vertical_rate_tab")
##
##    add_plot(name="vel_tan_plot", label="Tangential Velocity vs Time",
##             x_axis_name="Time (s)", y_axis_name = "Tangential Velocity (m/s)", anti_aliased=True, parent="tangential_rate_tab")

    add_input_text(name = "p_apoapsis_output_field", label = "Apoapsis (m)",
                   source="apoapsis", readonly=True, enabled=False, parent="params_tab")
    add_input_text(name = "p_periapsis_output_field", label = "Periapsis (m)",
                   source="periapsis", readonly=True, enabled=False, parent="params_tab")
    add_input_text(name = "p_vel_max_output_field", label = "Max. Velocity (m/s)",
                   source="vel_max", readonly=True, enabled=False, parent="params_tab")
    add_input_text(name = "p_vel_min_output_field", label = "Min. Velocity (m/s)",
                   source="vel_min", readonly=True, enabled=False, parent="params_tab")
    add_input_text(name = "p_vel_avg_output_field", label = "Average Velocity (m/s)",
                   source="vel_avg", readonly=True, enabled=False, parent="params_tab")
    add_input_text(name = "p_period_output_field", label = "Orbital Period (s)",
                   source="period", readonly=True, enabled=False, parent="params_tab")

#LOG WINDOW
with window("Log", width=550, height=190, no_close=True):
    set_window_pos("Log", 10, 450)
    add_logger("Logs", log_level=0, autosize_x = True, autosize_y = True)

start_dearpygui()
