#   RANDOM THREE BODY SYSTEM GENERATOR + SIMULATOR

from dearpygui.core import *
from dearpygui.simple import *
import math
import pandas as pd
import time as t
import scipy.constants as scp_const
import random

#set initial window configuration (purely cosmetic)
set_main_window_size(1300, 700)
set_main_window_title("Three Body System Generator")
set_theme("Dark")

grav_const = scp_const.G

set_value(name="progress", value=0)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                SIMULATION SETUP
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def disableEndFlag():
    internal_dpg.configure_item("end_flag", enabled=False)

def enableEndFlag():
    internal_dpg.configure_item("end_flag", enabled=True)

def generateRandom(min_val, max_val):
    return random.uniform(min_val, max_val)

def generateRandomXY(max_val):
    x = random.uniform(-max_val, max_val)
    y = random.uniform(-max_val, max_val)

    return [x, y]

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
            self.x_list = []
            self.y_list = []
            self.color = [255, 255, 255, 255]
            self.label = "Body"

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

        def get_radius (self):
            return self.radius

        def get_mass (self):
            return self.mass

        def get_grav_pull (self, dist):
            return (grav_const * self.mass) / (dist**2)

        def set_color (self, new_color):
            self.color = new_color

        def get_color (self):
            return self.color

        def set_label (self, label):
            self.label = label

        def get_label (self):
            return self.label

    max_pos = float(get_value("max_pos_input")) * 9460730000000000 # light years ---> meters
    max_vel = float(get_value("max_vel_input")) * 1000             # km/s        ---> m/s
    min_mass = float(get_value("min_mass_input")) * 1.989 * 10**30 # solar mass  ---> kg
    max_mass = float(get_value("max_mass_input")) * 1.989 * 10**30 # solar mass  ---> kg
    
    # create bodies
    body_a = body()
    body_b = body()
    body_c = body()

    # generate random values for bodies
    body_a.set_pos(generateRandomXY(max_pos)[0], generateRandomXY(max_pos)[1])
    body_a.set_vel(generateRandomXY(max_vel)[0], generateRandomXY(max_vel)[1])
    body_a.set_mass(generateRandom(min_mass, max_mass))
    body_a.set_color([255, 0, 0, 255])
    body_a.set_radius(body_a.get_mass()/10**24)
    body_a.set_label("Body A")

    set_value("a_mass", value=body_a.get_mass()/(1.989 * 10**30))

    body_b.set_pos(generateRandomXY(max_pos)[0], generateRandomXY(max_pos)[1])
    body_b.set_vel(generateRandomXY(max_vel)[0], generateRandomXY(max_vel)[1])
    body_b.set_mass(generateRandom(min_mass, max_mass))
    body_b.set_color([0, 255, 0, 255])
    body_b.set_radius(body_b.get_mass()/10**24)
    body_b.set_label("Body B")

    set_value("b_mass", value=body_b.get_mass()/(1.989 * 10**30))

    body_c.set_pos(generateRandomXY(max_pos)[0], generateRandomXY(max_pos)[1])
    body_c.set_vel(generateRandomXY(max_vel)[0], generateRandomXY(max_vel)[1])
    body_c.set_mass(generateRandom(min_mass, max_mass))
    body_c.set_color([0, 0, 255, 255])
    body_c.set_radius(body_c.get_mass()/10**24)
    body_c.set_label("Body C")

    set_value("c_mass", value=body_c.get_mass()/(1.989 * 10**30))

    # global simulation inputs
    time_increment = float(get_value("sim_speed_field")/get_value("sim_precision_field"))

    # Calculation sub-functions

    def clamp(num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def sign(x): return 1 if x >= 0 else -1

    def get_dist(obj1, obj2):
        dist = ((obj1.get_pos()[0] - obj2.get_pos()[0])**2 + (obj1.get_pos()[1] - obj2.get_pos()[1])**2)**(0.5)
        return float(dist)
         

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                   RUN SIMULATION
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    #set initial values

    time = 0
    bodies = [body_a, body_b, body_c]

    # reset trajectory data for new simulation
    for obj in bodies:
        obj.clear_traj_history()

    # apply gravity to each object, by all bodies in the simulation
    for obj in bodies:
        for body in bodies:
            if not obj == body:
                obj.update_vel(body.get_grav_pull(get_dist(obj, body)) * abs(math.cos(math.atan((obj.get_pos()[1] - body.get_pos()[1])/(obj.get_pos()[0] - body.get_pos()[0])))) * sign(body.get_pos()[0] - obj.get_pos()[0]),
                               body.get_grav_pull(get_dist(obj, body)) * abs(math.sin(math.atan((obj.get_pos()[1] - body.get_pos()[1])/(obj.get_pos()[0] - body.get_pos()[0])))) * sign(body.get_pos()[1] - obj.get_pos()[1]),
                               time_increment)
                            
        
    time_list = []
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

        for body in bodies:
             draw_circle(drawing="vis_canvas", center=space2screen(body.get_pos()[0]/vis_scale,body.get_pos()[1]/vis_scale,680,380), radius=(body.get_radius()/vis_scale), color=body.get_color())
             if get_value("display_labels"):
                draw_text(drawing="vis_canvas", pos=space2screen(body.get_pos()[0]/vis_scale+3,body.get_pos()[1]/vis_scale+3,680,380), size=14, text=body.get_label(), color=body.get_color())

        # --- --- --- --- --- ---

        for obj in bodies:
            obj.update_traj()

        # - - - - ITERATIVE PHYSICS HAPPEN HERE - - - -
        # increment time step
        time = time + time_increment

        # apply gravity to each object, by all bodies in the simulation
        for obj in bodies:
            for body in bodies:
                if not obj == body:
                    obj.update_vel(body.get_grav_pull(get_dist(obj, body)) * abs(math.cos(math.atan((obj.get_pos()[1] - body.get_pos()[1])/(obj.get_pos()[0] - body.get_pos()[0])))) * sign(body.get_pos()[0] - obj.get_pos()[0]),
                                   body.get_grav_pull(get_dist(obj, body)) * abs(math.sin(math.atan((obj.get_pos()[1] - body.get_pos()[1])/(obj.get_pos()[0] - body.get_pos()[0])))) * sign(body.get_pos()[1] - obj.get_pos()[1]),
                                   time_increment)

        # update positions
        for obj in bodies:
            obj.update_pos(obj.get_vel()[0], obj.get_vel()[1], time_increment)
        # - - - -   - - - -   - - - -   - - - -   - - - -

        # adjust simulation speed
        speed_scale = get_value("sim_speed_field")
        cycle_dt = t.perf_counter() - cycle_start
        try:
            t.sleep((time_increment-cycle_dt)*(1/speed_scale))
        except:
            pass

        set_value("a_pos", value=[body_a.get_pos()[0]/9460730000000000, body_a.get_pos()[1]/9460730000000000])
        set_value("b_pos", value=[body_b.get_pos()[0]/9460730000000000, body_b.get_pos()[1]/9460730000000000])
        set_value("c_pos", value=[body_c.get_pos()[0]/9460730000000000, body_c.get_pos()[1]/9460730000000000])

        set_value("a_vel", value=[body_a.get_vel()[0]/1000, body_a.get_vel()[1]/1000])
        set_value("b_vel", value=[body_b.get_vel()[0]/1000, body_b.get_vel()[1]/1000])
        set_value("c_vel", value=[body_c.get_vel()[0]/1000, body_c.get_vel()[1]/1000])

        if get_value("realtime_graph"):
            for obj in bodies:
                add_line_series(name=str(obj.get_label() + " Traj"), plot="traj_plot", x=obj.get_traj()[0], y=obj.get_traj()[1], color=obj.get_color())

        if get_value("end_flag"):
            disableEndFlag()
            set_value("end_flag", value=False)
            break

    # post-simulation
    for obj in bodies:
        add_line_series(name=str(obj.get_label() + " Traj"), plot="traj_plot", x=obj.get_traj()[0], y=obj.get_traj()[1], color=obj.get_color())

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                    USER INTERFACE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def space2screen(space_x, space_y, screen_width, screen_height):
    
    screen_x = space_x + screen_width/2
    screen_y = -space_y + screen_height/2

    return [screen_x, screen_y]

def setSimSpeedLimits():
    internal_dpg.configure_item("sim_speed_field", min_value=float(get_value("sim_speed_min_field")), max_value=float(get_value("sim_speed_max_field")))

def setScaleLimits():
    internal_dpg.configure_item("vis_scale_field", min_value=float(get_value("scale_min_field")), max_value=float(get_value("scale_max_field")))

#INPUTS WINDOW
with window("Input", width=550, height=630, no_close=True):   
    set_window_pos("Input", 10, 10)

    add_input_text(name="max_pos_input", label= "Max. Position (ly)", default_value = "0.05")
    add_input_text(name="max_vel_input", label= "Max. Velocity (km/s)", default_value = "3")
    add_input_text(name="min_mass_input", label= "Min. Mass (solar mass)", default_value = "0.7")
    add_input_text(name="max_mass_input", label= "Max. Mass (solar mass)", default_value = "30")

    add_spacing(count=6)
    add_separator()
    add_spacing(count=6)

    add_input_text(name="sim_speed_min_field", label= "Min. Sim. Speed", default_value = "10e+7", width=100, callback=setSimSpeedLimits)
    add_same_line()
    add_input_text(name="sim_speed_max_field", label= "Max. Sim. Speed", default_value = "10e+10", width=100, callback=setSimSpeedLimits)
    add_spacing(count=6)
    add_text("Simulation Speed:")
    add_slider_float(name="sim_speed_field", label="",
                     min_value=float(get_value("sim_speed_min_field")), max_value=float(get_value("sim_speed_max_field")), default_value=5000000000,
                     clamped=True, width=500)
    add_spacing(count=6)
    add_text("Simulation Precision:")
    add_slider_float(name="sim_precision_field", label="",
                     min_value=1, max_value=100.0, default_value=90.0,
                     clamped=True, width=500)
    add_checkbox(name = "realtime_graph", label = "Update graphs every cycle", tip="Looks really cool but significantly reduces performance.")
    add_spacing(count=6)
    add_button("Generate & Simulate", callback = simulateOrbit)
    add_same_line()
    add_checkbox(name="end_flag", label="End Simulation", tip="Raising this flag breaks out of the simulation loop in the next cycle.", enabled=False)

#OUTPUTS WINDOW
with window("Output", width=700, height=630, no_close=True):
    set_window_pos("Output", 570, 10)

    add_tab_bar(name="graph_switch")
    end("graph_switch")
    add_tab(name="vis_tab", label="Visualization", parent="graph_switch")
    end("vis_tab")
    add_tab(name="graphs_tab", label="Graphs", parent="graph_switch")
    end("graphs_tab")

    # VISUALIZER
    
    add_input_text(name="scale_min_field", label="Scale Min", parent="vis_tab", default_value="10e+11", width=100, callback=setScaleLimits)
    add_same_line(parent="vis_tab")
    add_input_text(name="scale_max_field", label="Scale Max", parent="vis_tab", default_value="10e+13", width=100, callback=setScaleLimits)
    add_same_line(parent="vis_tab")
    add_checkbox(name="display_labels", label="Show Labels", parent="vis_tab")
    
    add_slider_float(name="vis_scale_field", label="Scale (m/pixel)",
                     min_value=float(get_value("scale_min_field")), max_value=float(get_value("scale_max_field")), default_value=5000000000000.0,
                     clamped=True, parent="vis_tab", width=300)

    add_drawing("vis_canvas", parent="vis_tab", width=680, height=380)
    clear_drawing("vis_canvas")

    add_input_float(name="body_a_mass", label="Body A Mass", source="a_mass", enabled=False, width=100, parent="vis_tab")
    add_same_line(parent="vis_tab")
    add_input_float2(name="body_a_pos", label="Body A Pos.", source="a_pos", enabled=False, width=100, parent="vis_tab")
    add_same_line(parent="vis_tab")
    add_input_float2(name="body_a_vel", label="Body A Vel.", source="a_vel", enabled=False, width=100, parent="vis_tab")

    add_input_float(name="body_b_mass", label="Body B Mass", source="b_mass", enabled=False, width=100, parent="vis_tab")
    add_same_line(parent="vis_tab")
    add_input_float2(name="body_b_pos", label="Body B Pos.", source="b_pos", enabled=False, width=100, parent="vis_tab")
    add_same_line(parent="vis_tab")
    add_input_float2(name="body_b_vel", label="Body B Vel.", source="b_vel", enabled=False, width=100, parent="vis_tab")

    add_input_float(name="body_c_mass", label="Body C Mass", source="c_mass", enabled=False, width=100, parent="vis_tab")
    add_same_line(parent="vis_tab")
    add_input_float2(name="body_c_pos", label="Body C Pos.", source="c_pos", enabled=False, width=100, parent="vis_tab")
    add_same_line(parent="vis_tab")
    add_input_float2(name="body_c_vel", label="Body C Vel.", source="c_vel", enabled=False, width=100, parent="vis_tab")

    # GRAPHS
    add_plot(name="traj_plot", label="Trajectory",
             x_axis_name="X (m)", y_axis_name = "Y (m)", anti_aliased=True, parent="graphs_tab", equal_aspects=True)

start_dearpygui()
