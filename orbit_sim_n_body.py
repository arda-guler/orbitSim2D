#   N-BODY ORBIT SIMULATOR

version = "0.1.0 Pre-Alpha"

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

#variables to save values of last run
#saving in another variable in case user makes changes to the input fields before clicking Export
last_alt_init = None
last_vel_rad_init = None
last_vel_tgn_init = None
last_body_mass = None
last_body_radius = None
last_time_increment = None

last_results = []

grav_const = scp_const.G

set_value(name="progress", value=0)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                 FILE IMPORT/EXPORT
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

##def importFile():
##
##    try:
##        import_filepath = get_value("filepath_field")
##        
##        if not import_filepath[-4:] == ".txt":
##            if import_filepath[-5:] == ".xlsx":
##                log_warning("Exported .xlsx files don't contain input info. Trying " + import_filepath[:-5] + ".txt instead...", logger="Logs")
##                import_filepath = import_filepath[:-5] + ".txt"
##            else:
##                import_filepath = import_filepath + ".txt"
##            
##        log_info("Importing inputs from " + import_filepath, logger="Logs")
##        import_file = open(import_filepath, "r")
##    except:
##        log_error("Import failed. Check filepath.", logger="Logs")
##        return
##
##    try:
##        import_lines = import_file.readlines()
##        if not import_lines[0][18:-1] == version:
##            log_warning("Save file version does not match software version. Import might fail.", logger="Logs")
##
##        set_value(name="alt_init_field", value=import_lines[4][18:-3])
##        set_value(name="vel_tgn_init_field", value=import_lines[5][29:-5])
##        set_value(name="vel_rad_init_field", value=import_lines[6][25:-5])
##        set_value(name="body_mass_field", value=import_lines[7][11:-4])
##        set_value(name="body_mass_magnitude_field", value="0")
##        set_value(name="body_radius_field", value=import_lines[8][13:-3])
##        set_value(name="body_radius_magnitude_field", value="0")
##        set_value(name="time_increment_field", value=import_lines[9][16:-3])
##            
##    except:
##        log_error("Import failed. Check file formatting.", logger="Logs")
##        return
##
##    log_info("Import successful.", logger="Logs")
##
##def exportFile():
##
##    global version
##    
##    if not calc_run_number > 0:
##        log_error("Cannot export. Run the calculations first.", logger="Logs")
##        return
##
##    show_item("progress_bar")
##    setProgressBarOverlay("Attempting export...")
##    excelFilename = get_value("filepath_field")
##
##    # sanitize filename
##    if not excelFilename == "" or excelFilename == None:
##        log_info("Attempting export (this might take a while)...", logger = "Logs")
##        if len(excelFilename) > 5 and excelFilename[-5:] == ".xlsx":
##            exportFile = excelFilename
##        elif len(excelFilename) > 4 and excelFilename[-4:] == ".txt":
##            exportFile = excelFilename[:-4] + ".xlsx"
##        else:
##            exportFile = excelFilename + ".xlsx"
##
##        # Actual writing to Excel happens here
##        try:
##            
##            # map of last_results:
##            # [time_list, alt_list, vel_list, gravity_list, pos_x_list, pos_y_list]
##            # [0]: time_list
##            # [1]: alt_list
##            # [2]: vel_list
##            # [3]: gravity_list
##            # [4]: pos_x_list
##            # [5]: pos_y_list
##
##            setProgressBarOverlay("Preparing data for export...")
##
##            export_alt = {'Time (s)': last_results[0], 'Altitude (m)': last_results[1]}
##            export_vel = {'Time (s)': last_results[0], 'Velocity (m/s)': last_results[2]}
##            export_grav = {'Time (s)': last_results[0], 'Gravity (m/s^2)': last_results[3]}
##            export_traj = {'Pos_X (m)': last_results[4], 'Pos_Y (m)': last_results[5]}
##
##            df_alt = pd.DataFrame(export_alt)
##            df_vel = pd.DataFrame(export_vel)
##            df_grav = pd.DataFrame(export_grav)
##            df_traj = pd.DataFrame(export_traj)
##
##            with pd.ExcelWriter(exportFile) as writer:
##                set_value(name="progress", value=0.25)
##                setProgressBarOverlay("Writing trajectory...")
##                df_traj.to_excel(writer, sheet_name = 'Trajectory')
##                set_value(name="progress", value=0.50)
##                setProgressBarOverlay("Writing altitude...")
##                df_alt.to_excel(writer, sheet_name = 'Altitude')
##                set_value(name="progress", value=0.75)
##                setProgressBarOverlay("Writing velocity...")
##                df_vel.to_excel(writer, sheet_name = 'Velocity')
##                set_value(name="progress", value=0.95)
##                setProgressBarOverlay("Writing gravity...")
##                df_grav.to_excel(writer, sheet_name = 'Gravity')
##            
##            setProgressBarOverlay("Finishing xlsx export...")
##  
##            log_info("Successfully saved data to " + exportFile, logger = "Logs")
##            
##        except:
##            log_error("Excel export failed.", logger = "Logs")
##
##        setProgressBarOverlay("Saving inputs to TXT...")
##        
##        # Save given inputs to TXT
##        try:
##            set_value(name="progress", value=0.96)
##            inputSaveFile = exportFile[0:-5] + ".txt"
##            result_file = open(inputSaveFile, "w")
##            result_file.write("Save file version " + version + "\n\n")
##            result_file.write("INPUTS\n\n")
##            result_file.write("Initial altitude: ")
##            result_file.write(str(last_alt_init)+" m\n")
##            result_file.write("Initial tangential velocity: ")
##            result_file.write(str(last_vel_tgn_init)+" m/s\n")
##            result_file.write("Initial radial velocity: ")
##            result_file.write(str(last_vel_rad_init)+" m/s\n")
##            result_file.write("Body mass: ")
##            result_file.write(str(last_body_mass)+" kg\n")
##            result_file.write("Body radius: ")
##            result_file.write(str(last_body_radius)+" m\n")
##            result_file.write("Time increment: ")
##            result_file.write(str(last_time_increment)+" s\n")
##            result_file.close()
##            log_info("Inputs saved in " + inputSaveFile, logger = "Logs")
##        except:
##            log_error("TXT export failed.", logger = "Logs")  
##        
##    else:
##        log_warning("No filename provided. Export aborted.", logger = "Logs")
##    set_value(name="progress", value=1)
##    hide_item("progress_bar")
##    log_info("Done.", logger = "Logs")
##    set_value(name="progress", value=0)
##    setProgressBarOverlay("")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                SIMULATION SETUP
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def disableEndFlag():
    internal_dpg.configure_item("end_flag", enabled=False)

def enableEndFlag():
    internal_dpg.configure_item("end_flag", enabled=True)

def simulateOrbit():

    global calc_run_number
    calc_run_number += 1
    log_info(message = "Run [" + str(calc_run_number) + "]: Simulating trajectory...", logger = "Logs")

    # get input values from entry fields

    drag_enabled = get_value("drag_model_checkbox")
    
 ##   try:
    # parent body
    parent_body_mass = float(get_value("body_mass_field")) * 10**float((get_value("body_mass_magnitude_field")))
    parent_body_radius = float(get_value("body_radius_field")) * 10**float((get_value("body_radius_magnitude_field")))

    # vessel
    init_orbiting_body = int(get_value("init_orbiting_body_field"))
    alt_init = float(get_value("alt_init_field"))
    vel_tgn_init = float(get_value("vel_tgn_init_field"))
    vel_rad_init = float(get_value("vel_rad_init_field"))
    long_init = float(get_value("long_init_field"))

    # moon 1
    moon1_exists = get_value("moon1_check")
    if moon1_exists:
        moon1_mass = float(get_value("moon1_mass_field")) * 10**float((get_value("moon1_mass_magnitude_field")))
        moon1_radius = float(get_value("moon1_radius_field")) * 10**float((get_value("moon1_radius_magnitude_field")))
        moon1_alt_init = float(get_value("moon1_alt_init_field"))
        moon1_vel_tgn_init = float(get_value("moon1_vel_tgn_init_field"))
        moon1_vel_rad_init = float(get_value("moon1_vel_rad_init_field"))
        moon1_long_init = float(get_value("moon1_long_init_field"))
    else:
        moon1_mass = 0
        moon1_radius = 0
        moon1_alt_init = 0
        moon1_vel_tgn_init = 0
        moon1_vel_rad_init = 0
        moon1_long_init = 0

    # moon 2
    moon2_exists = get_value("moon2_check")
    if moon2_exists:
        moon2_mass = float(get_value("moon2_mass_field")) * 10**float((get_value("moon2_mass_magnitude_field")))
        moon2_radius = float(get_value("moon2_radius_field")) * 10**float((get_value("moon2_radius_magnitude_field")))
        moon2_alt_init = float(get_value("moon2_alt_init_field"))
        moon2_vel_tgn_init = float(get_value("moon2_vel_tgn_init_field"))
        moon2_vel_rad_init = float(get_value("moon2_vel_rad_init_field"))
        moon2_long_init = float(get_value("moon2_long_init_field"))
    else:
        moon2_mass = 0
        moon2_radius = 0
        moon2_alt_init = 0
        moon2_vel_tgn_init = 0
        moon2_vel_rad_init = 0
        moon2_long_init = 0

    # global simulation inputs
    time_increment = float(get_value("time_increment_field"))
##            
##    except:
##        log_error("Input error. Make sure all design parameters are float values.", logger = "Logs")
##        return

##    # save these values in global scope, in case we want to export
##    global last_alt_init, last_vel_tgn_init, last_vel_rad_init, last_time_increment, last_body_radius, last_body_mass
##    last_alt_init = alt_init
##    last_vel_tgn_init = vel_tgn_init
##    last_vel_rad_init = vel_rad_init
##    last_body_mass = body_mass
##    last_body_radius = body_radius
##    last_time_increment = time_increment

##    log_info("Inputs:\n" +
##             "Initial Alt.: " + str(alt_init) + " m\n"
##             "Init. Tgn. Vel.:" + str(vel_tgn_init) + " m/s\n"
##             "Init. Rad. Vel.:" + str(vel_rad_init) + " m/s\n"
##             "Body Mass:" + str(body_mass) + " kg\n"
##             "Time Increment: " + str(time_increment) + " s\n", logger = "Logs")

    # Calculation sub-functions

    def clamp(num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def sign(x): return 1 if x >= 0 else -1

    def calc_grav(body_mass, dist):
        global grav_const
        gravity = (grav_const * body_mass) / (dist**2)
        return gravity

    def calc_grav_force(mass1, mass2, dist):
        global grav_const
        gravity_force = (grav_const * mass1 * mass2) / (dist**2)
        return gravity_force

    # takes longitude (in degrees) and altitude, gives relative x and y position
    def sph2cart(r, long_theta):
        phi = long_theta + 90
        phi = math.radians(phi)
        
        x = r * math.cos(phi)
        y = r * math.sin(phi)

        return [x, y]
         

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                   RUN SIMULATION
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    #set initial values

    time = 0
    
    parent_pos_x = 0
    parent_pos_y = 0
    parent_vel_x = 0
    parent_vel_y = 0

    if moon1_exists:
        moon1_alt = moon1_alt_init
        moon1_pos_x = sph2cart(moon1_alt_init, moon1_long_init)[0]
        moon1_pos_y = sph2cart(moon1_alt_init, moon1_long_init)[1]
        moon1_vel_x = moon1_vel_rad_init * math.cos(math.radians(moon1_long_init + 90)) + moon1_vel_tgn_init * math.cos(math.radians(moon1_long_init + 180))
        moon1_vel_y = moon1_vel_rad_init * math.sin(math.radians(moon1_long_init + 90)) + moon1_vel_tgn_init * math.sin(math.radians(moon1_long_init + 180))

    if moon2_exists:
        moon2_alt = moon2_alt_init
        moon2_pos_x = sph2cart(moon2_alt_init, moon2_long_init)[0]
        moon2_pos_y = sph2cart(moon2_alt_init, moon2_long_init)[1]
        moon2_vel_x = moon2_vel_rad_init * math.cos(math.radians(moon2_long_init + 90)) + moon1_vel_tgn_init * math.cos(math.radians(moon2_long_init + 180))
        moon2_vel_y = moon2_vel_rad_init * math.sin(math.radians(moon2_long_init + 90)) + moon1_vel_tgn_init * math.sin(math.radians(moon2_long_init + 180))

    vessel_alt = alt_init
    if init_orbiting_body == 0:
        vessel_pos_x = sph2cart(alt_init + parent_body_radius, long_init)[0]
        vessel_pos_y = sph2cart(alt_init + parent_body_radius, long_init)[1]
        vessel_vel_x = vel_rad_init * math.cos(math.radians(long_init + 90)) + vel_tgn_init * math.cos(math.radians(long_init + 180))
        vessel_vel_y = vel_rad_init * math.sin(math.radians(long_init + 90)) + vel_tgn_init * math.sin(math.radians(long_init + 180))
        
    elif init_orbiting_body == 1 and moon1_exists:
        vessel_pos_x = moon1_pos_x + sph2cart(alt_init + moon1_radius, long_init)[0]
        vessel_pos_y = moon1_pos_y + sph2cart(alt_init + moon1_radius, long_init)[1]
        vessel_vel_x = vel_rad_init * math.cos(math.radians(long_init + 90)) + vel_tgn_init * math.cos(math.radians(long_init + 180)) + moon1_vel_x
        vessel_vel_y = vel_rad_init * math.sin(math.radians(long_init + 90)) + vel_tgn_init * math.sin(math.radians(long_init + 180)) + moon1_vel_y

    elif init_orbiting_body == 2 and moon2_exists:
        vessel_pos_x = moon2_pos_x + sph2cart(alt_init + moon2_radius, long_init)[0]
        vessel_pos_y = moon2_pos_y + sph2cart(alt_init + moon2_radius, long_init)[1]
        vessel_vel_x = vel_rad_init * math.cos(math.radians(long_init + 90)) + vel_tgn_init * math.cos(math.radians(long_init + 180)) + moon2_vel_x
        vessel_vel_y = vel_rad_init * math.sin(math.radians(long_init + 90)) + vel_tgn_init * math.sin(math.radians(long_init + 180)) + moon2_vel_y

    else:
        log_error("No.", logger="Logs")
        return

    vessel_gravity_parent = calc_grav(parent_body_mass, ((parent_pos_x-vessel_pos_x)**2 + (parent_pos_y-vessel_pos_y) **2)**(0.5))
    
    if moon1_exists:
        parent_gravity_moon1 = calc_grav_force(parent_body_mass, moon1_mass, ((parent_pos_x-moon1_pos_x)**2 + (parent_pos_y-moon1_pos_y)**2)**(0.5)) / (parent_body_mass)
        vessel_gravity_moon1 = calc_grav(moon1_mass, ((moon1_pos_x-vessel_pos_x)**2 + (moon1_pos_y-vessel_pos_y)**2)**(0.5))
        if moon2_exists:
            moon2_gravity_moon1 = calc_grav_force(moon1_mass, moon2_mass, ((moon2_pos_x-moon1_pos_x)**2 + (moon2-moon1_pos_y)**2)**(0.5)) / (moon2_mass)
        else:
            moon2_gravity_moon1 = 0
    else:
        parent_gravity_moon1 = 0
        vessel_gravity_moon1 = 0
    
    if moon2_exists:
        parent_gravity_moon2 = calc_grav_force(parent_body_mass, moon2_mass, ((parent_pos_x-moon2_pos_x)**2 + (parent_pos_y-moon2_pos_y)**2)**(0.5)) / (parent_body_mass)
        vessel_gravity_moon2 = calc_grav(moon2_mass, ((moon2_pos_x-vessel_pos_x)**2 + (moon2_pos_y-vessel_pos_y)**2)**(0.5))
        if moon1_exists:
            moon1_gravity_moon2 = calc_grav_force(moon1_mass, moon2_mass, ((moon2_pos_x-moon1_pos_x)**2 + (moon2-moon1_pos_y)**2)**(0.5)) / (moon1_mass)
        else:
            moon1_gravity_moon2 = 0
    else:
        parent_gravity_moon2 = 0
        vessel_gravity_moon2 = 0
        
##    time_list = []
##    alt_list = []
##    vel_list = []
##    vel_rad_list = []
##    vel_tgn_list = []
##    gravity_list = []
    vessel_pos_x_list = []
    vessel_pos_y_list = []

    show_item("progress_bar")
    progress_loop = 0
    enableEndFlag()

    # BEGIN TIMESTEPS
    
    while (True):

        cycle_start = t.perf_counter()

        # update visualizer ---

        vis_scale = float(get_value("vis_scale_field"))
        clear_drawing("vis_canvas")

        if get_value("lock_on_vessel"):
            #vessel
            draw_rectangle(drawing="vis_canvas", pmin=space2screen(-3,-3,680,380), pmax=space2screen(3,3,680,380), color=[200,0,0,255])

            #planet
            draw_circle(drawing="vis_canvas", center=space2screen((parent_pos_x-vessel_pos_x)/vis_scale,(parent_pos_y-vessel_pos_y)/vis_scale,680,380), radius=(parent_body_radius/vis_scale), color=[255,255,255,255])

            #moon1
            if moon1_exists:
                draw_circle(drawing="vis_canvas", center=space2screen((moon1_pos_x-vessel_pos_x)/vis_scale,(moon1_pos_y-vessel_pos_y)/vis_scale,680,380), radius=(moon1_radius/vis_scale), color=[255,255,255,255])

            if moon2_exists:
                draw_circle(drawing="vis_canvas", center=space2screen((moon2_pos_x-vessel_pos_x)/vis_scale,(moon2_pos_y-vessel_pos_y)/vis_scale,680,380), radius=(moon2_radius/vis_scale), color=[255,255,255,255])
            
        else:
            # parent
            draw_circle(drawing="vis_canvas", center=space2screen(parent_pos_x/vis_scale,parent_pos_y/vis_scale,680,380), radius=(parent_body_radius/vis_scale), color=[255,255,255,255])

            # vessel
            draw_rectangle(drawing="vis_canvas", pmin=space2screen(vessel_pos_x/vis_scale-3,vessel_pos_y/vis_scale-3,680,380), pmax=space2screen(vessel_pos_x/vis_scale+3,vessel_pos_y/vis_scale+3,680,380), color=[200,0,0,255])

            #moon1
            if moon1_exists:
                draw_circle(drawing="vis_canvas", center=space2screen(moon1_pos_x/vis_scale,moon1_pos_y/vis_scale,680,380), radius=(moon1_radius/vis_scale), color=[255,255,255,255])

            if moon2_exists:
               draw_circle(drawing="vis_canvas", center=space2screen(moon2_pos_x/vis_scale,moon2_pos_y/vis_scale,680,380), radius=(moon2_radius/vis_scale), color=[255,255,255,255]) 
        # --- --- --- --- --- ---

        if progress_loop < 1.0:
            progress_loop = progress_loop + 0.01
        else:
            progress_loop = 0.0

        set_value(name="progress", value=progress_loop)
        setProgressBarOverlay("Simulation running...")

##        time_list.append(time)
##        alt_list.append(alt)
##        vel_list.append(vel)
##        gravity_list.append(gravity)
        vessel_pos_x_list.append(vessel_pos_x)
        vessel_pos_y_list.append(vessel_pos_y)

        # - - - -
        # increment time step
        time = time + time_increment

        # update gravitational acceleration magnitudes
        vessel_gravity_parent = calc_grav(parent_body_mass, ((parent_pos_x-vessel_pos_x)**2 + (parent_pos_y-vessel_pos_y)**2)**(0.5))
    
        if moon1_exists:
            parent_gravity_moon1 = calc_grav_force(parent_body_mass, moon1_mass, ((parent_pos_x-moon1_pos_x)**2 + (parent_pos_y-moon1_pos_y)**2)**(0.5)) / (parent_body_mass)
            moon1_gravity_parent = calc_grav_force(parent_body_mass, moon1_mass, ((parent_pos_x-moon1_pos_x)**2 + (parent_pos_y-moon1_pos_y)**2)**(0.5)) / (moon1_mass)
            vessel_gravity_moon1 = calc_grav(moon1_mass, ((moon1_pos_x-vessel_pos_x)**2 + (moon1_pos_y-vessel_pos_y)**2)**(0.5))
            if moon2_exists:
                moon2_gravity_moon1 = calc_grav_force(moon1_mass, moon2_mass, ((moon2_pos_x-moon1_pos_x)**2 + (moon2-moon1_pos_y)**2)**(0.5)) / (moon2_mass)
            else:
                moon2_gravity_moon1 = 0
        else:
            parent_gravity_moon1 = 0
            vessel_gravity_moon1 = 0
        
        if moon2_exists:
            parent_gravity_moon2 = calc_grav_force(parent_body_mass, moon2_mass, ((parent_pos_x-moon2_pos_x)**2 + (parent_pos_y-moon2_pos_y)**2)**(0.5)) / (parent_body_mass)
            moon2_gravity_parent = calc_grav_force(parent_body_mass, moon2_mass, ((parent_pos_x-moon2_pos_x)**2 + (parent_pos_y-moon2_pos_y)**2)**(0.5)) / (moon2_mass)
            vessel_gravity_moon2 = calc_grav(moon2_mass, ((moon2_pos_x-vessel_pos_x)**2 + (moon2_pos_y-vessel_pos_y)**2)**(0.5))
            if moon1_exists:
                moon1_gravity_moon2 = calc_grav_force(moon1_mass, moon2_mass, ((moon2_pos_x-moon1_pos_x)**2 + (moon2-moon1_pos_y)**2)**(0.5)) / (moon1_mass)
            else:
                moon1_gravity_moon2 = 0
        else:
            parent_gravity_moon2 = 0
            vessel_gravity_moon2 = 0

        # update velocities
        vessel_vel_x = vessel_vel_x + vessel_gravity_parent * abs(math.cos(math.atan((vessel_pos_y - parent_pos_y)/(vessel_pos_x - parent_pos_x)))) * sign(parent_pos_x - vessel_pos_x) * time_increment
        vessel_vel_y = vessel_vel_y + vessel_gravity_parent * abs(math.sin(math.atan((vessel_pos_y - parent_pos_y)/(vessel_pos_x - parent_pos_x)))) * sign(parent_pos_y - vessel_pos_y) * time_increment

        if moon1_exists:
            moon1_vel_x = moon1_vel_x + moon1_gravity_parent * abs(math.cos(math.atan((moon1_pos_y - parent_pos_y)/(moon1_pos_x - parent_pos_x)))) * sign(parent_pos_x - moon1_pos_x) * time_increment
            moon1_vel_y = moon1_vel_y + moon1_gravity_parent * abs(math.sin(math.atan((moon1_pos_y - parent_pos_y)/(moon1_pos_x - parent_pos_x)))) * sign(parent_pos_y - moon1_pos_y) * time_increment

            parent_vel_x = parent_vel_x + parent_gravity_moon1 * abs(math.cos(math.atan((parent_pos_y - moon1_pos_y)/(parent_pos_x - moon1_pos_x)))) * sign(moon1_pos_x - parent_pos_x) * time_increment
            parent_vel_y = parent_vel_y + parent_gravity_moon1 * abs(math.sin(math.atan((parent_pos_y - moon1_pos_y)/(parent_pos_x - moon1_pos_x)))) * sign(moon1_pos_y - parent_pos_y) * time_increment

            vessel_vel_x = vessel_vel_x + vessel_gravity_moon1 * abs(math.cos(math.atan((vessel_pos_y - moon1_pos_y)/(vessel_pos_x - moon1_pos_x)))) * sign(moon1_pos_x - vessel_pos_x) * time_increment
            vessel_vel_y = vessel_vel_y + vessel_gravity_moon1 * abs(math.sin(math.atan((vessel_pos_y - moon1_pos_y)/(vessel_pos_x - moon1_pos_x)))) * sign(moon1_pos_y - vessel_pos_y) * time_increment

            if moon2_exists:
                moon1_vel_x = moon1_vel_x + moon1_gravity_moon2 * abs(math.cos(math.atan((moon1_pos_y - moon2_pos_y)/(moon1_pos_x - moon2_pos_x)))) * sign(moon2_pos_x - moon1_pos_x) * time_increment
                moon1_vel_y = moon1_vel_y + moon1_gravity_moon2 * abs(math.sin(math.atan((moon1_pos_y - moon2_pos_y)/(moon1_pos_x - moon2_pos_x)))) * sign(moon2_pos_y - moon1_pos_y) * time_increment

                moon2_vel_x = moon2_vel_x + moon1_gravity_moon2 * abs(math.cos(math.atan((moon1_pos_y - moon2_pos_y)/(moon1_pos_x - moon2_pos_x)))) * sign(moon1_pos_x - moon2_pos_x) * time_increment
                moon2_vel_y = moon2_vel_y + moon1_gravity_moon2 * abs(math.sin(math.atan((moon1_pos_y - moon2_pos_y)/(moon1_pos_x - moon2_pos_x)))) * sign(moon1_pos_y - moon2_pos_y) * time_increment

                parent_vel_x = parent_vel_x + parent_gravity_moon2 * abs(math.cos(math.atan((parent_pos_y - moon2_pos_y)/(parent_pos_x - moon2_pos_x)))) * sign(moon2_pos_x - parent_pos_x) * time_increment
                parent_vel_y = parent_vel_y + parent_gravity_moon2 * abs(math.sin(math.atan((parent_pos_y - moon2_pos_y)/(parent_pos_x - moon2_pos_x)))) * sign(moon2_pos_y - parent_pos_y) * time_increment

                vessel_vel_x = vessel_vel_x + vessel_gravity_moon2 * abs(math.cos(math.atan((vessel_pos_y - moon2_pos_y)/(vessel_pos_x - moon2_pos_x)))) * sign(moon2_pos_x - vessel_pos_x) * time_increment
                vessel_vel_y = vessel_vel_y + vessel_gravity_moon2 * abs(math.sin(math.atan((vessel_pos_y - moon2_pos_y)/(vessel_pos_x - moon2_pos_x)))) * sign(moon2_pos_y - vessel_pos_y) * time_increment

        # update positions
        vessel_pos_x = vessel_pos_x + vessel_vel_x * time_increment
        vessel_pos_y = vessel_pos_y + vessel_vel_y * time_increment

        parent_pos_x = parent_pos_x + parent_vel_x * time_increment
        parent_pos_y = parent_pos_y + parent_vel_y * time_increment

        if moon1_exists:
            moon1_pos_x = moon1_pos_x + moon1_vel_x * time_increment
            moon1_pos_y = moon1_pos_y + moon1_vel_y * time_increment

        if moon2_exists:
            moon2_pos_x = moon2_pos_x + moon2_vel_x * time_increment
            moon2_pos_y = moon2_pos_y + moon2_vel_y * time_increment
        
        # - - - -

        # adjust simulation speed
        speed_scale = get_value("sim_speed_field")
        cycle_dt = t.perf_counter() - cycle_start
        t.sleep((time_increment-cycle_dt)*(1/speed_scale))
        
        set_value(name="alt", value= ((parent_pos_x - vessel_pos_x)**2 + (parent_pos_y - vessel_pos_y)**2)**(0.5))
        set_value(name="vel", value= ((vessel_vel_x - parent_vel_x)**2 + (vessel_vel_y - parent_vel_y)**2)**(0.5))
        set_value(name="time", value=time)
##        set_value(name="dist", value=dist)

        if get_value("realtime_graph"):
##            add_line_series(name="Altitude", plot="alt_plot",x=time_list, y=alt_list)
##            add_line_series(name="Velocity", plot="vel_plot",x=time_list, y=vel_list)
##            add_line_series(name="Gravity", plot="grav_plot",x=time_list, y=gravity_list)
            add_line_series(name="Trajectory", plot="traj_plot", x=vessel_pos_x_list, y=vessel_pos_y_list)

        if get_value("end_flag"):
            end_flag = False
            disableEndFlag()
            set_value("end_flag", value=False)
            break

    setProgressBarOverlay("Updating graphs...")
##    add_line_series(name="Altitude", plot="alt_plot",x=time_list, y=alt_list)
##    add_line_series(name="Velocity", plot="vel_plot",x=time_list, y=vel_list)
##    add_line_series(name="Gravity", plot="grav_plot",x=time_list, y=gravity_list)
    add_line_series(name="Trajectory", plot="traj_plot", x=vessel_pos_x_list, y=vessel_pos_y_list)

    set_value(name="progress", value=0)
    hide_item("progress_bar")
    setProgressBarOverlay("")
    log_info("Simulation completed.", logger="Logs")

##    global last_results
##    last_results = [time_list, alt_list, vel_list, gravity_list, pos_x_list, pos_y_list]

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

#FILE OPERATIONS BAR
with window("File I/O", width=1260, height=60, no_close=True, no_move=True):
    set_window_pos("File I/O", 10, 10)
    add_input_text(name="filepath_field", label="Filepath", tip = "If the file is in the same directory with the script, you don't need\nto write the full path.")
##    add_same_line()
##    add_button("Import", callback=importFile)
##    add_same_line()
##    add_button("Export", callback=exportFile)
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
    add_text("x 10^",parent="moon2_input_tab")
    add_same_line(parent="moon2_input_tab")
    add_input_text(name = "moon2_radius_magnitude_field", label = "Body Radius (m)", width=100, parent="moon2_input_tab")
    add_spacing(count=6,parent="moon2_input_tab")
    add_input_text(name = "moon2_alt_init_field", label = "Initial Distance to Parent (m)", width=100, parent="moon2_input_tab", tip="Between body centers.")
    add_input_text(name = "moon2_vel_tgn_init_field", label = "Init. Tangential Vel. (m/s)", width=100, parent="moon2_input_tab", tip="Rel. to parent body.")
    add_input_text(name = "moon2_vel_rad_init_field", label = "Init. Radial Vel. (m/s)", width=100, parent="moon2_input_tab", tip="Rel. to parent body.")
    add_spacing(count=6,parent="moon2_input_tab")
    add_input_text(name = "moon2_long_init_field", label = "Init. Longitude (degrees)", width=100, parent="moon2_input_tab", tip="Zero at 12 o'clock of parent body, increases counterclockwise.")

    # spacing
    add_spacing(count=6)
    add_separator()
    add_spacing(count=6)

    # GLOBAL SIMULATION INPUTS
    add_input_text(name = "time_increment_field", label = "Time Increments (s)", tip="Enter lower values for higher precision.", default_value="1")
    add_spacing(count=6)
    add_text("Simulation Speed:")
    add_slider_float(name="sim_speed_field", label="",
                     min_value=0.1, max_value=5000.0, default_value=1.0,
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

    add_input_text(name="alt_output", label="Dist from Earth center (m)", source="alt", readonly=True, enabled=False, parent="vis_tab")
    #add_input_text(name="dist_output", label="Dist. From Body Center (m)", source="dist", readonly=True, enabled=False, parent="vis_tab")
    add_input_text(name="vel_output", label="Velocity (m/s)", source="vel", readonly=True, enabled=False, parent="vis_tab")
    add_input_text(name="time_output", label="Time (s)", source="time", readonly=True, enabled=False, parent="vis_tab")

    add_slider_float(name="vis_scale_field", label="Scale (m/pixel)",
                     min_value=1000.0, max_value=10000000.0, default_value=50000.0,
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
    add_tab(name="grav_tab", label="Gravity", parent="output_tabs")
    end("grav_tab")
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

    add_plot(name="grav_plot", label="Gravity vs Time",
             x_axis_name="Time (s)", y_axis_name = "Gravity (m/s^2)", anti_aliased=True, parent="grav_tab")

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
