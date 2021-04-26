# Particle Simulator 

This particle simulator is written using Python. 
Using the GUI, you can easily create and edit scenes and play with them in real-time.
For more info, you can watch this video: _https://youtu.be/iLcBNWgSt7I_. <br>
Most of the things I mentioned in that video you can also find in this file too, 
as well as a detailed explanation about things I didn't have time for to explain in the video.
If you have questions, suggestions or if you encounter a bug, be sure to let me know 
(eg. by creating an 'issue' on GitHub).

Example simulation can be found in the 'example_simulations'-folder. (see 'Saving and Loading Simulations')

## Table of Contents
1. [Required modules](#Required_modules)
2. [Shortcuts, mouse-modes and toolbar](#Shortcuts_and_toolbar)
    1. [Mouse-modes](#Mouse-modes)
    2. [Buttons](#Buttons)
    3. [Shortcuts](#Shortcuts)
3. [Simulation-settings](#Simulation-settings) + [Extra Options Window](#Extra_Options_Window)
4. [Linking, fit-linking and particle-groups](#Linking,_fit-linking_and_particle-groups)
5. [Particle-settings](#Particle-settings)
6. [Saving and Loading Simulations](#Saving_and_Loading_Simulations)
7. [Code-window](#Code-window)

## Required modules <a name="Required_modules"></a>
- pynput
- numpy
- cv2 (OpenCV) 
- PIL

The rest of the modules should be built-ins, 
but definitely let me know if you have problems with
the installation.

## Shortcuts and toolbar <a name="Shortcuts_and_toolbar"></a>
At the top of the screen, you can see the toolbar with the different mouse modes and some buttons.

### Mouse-modes <a name="Mouse-modes"></a>
In the toolbar, you can see 3 different mouse-modes, being to select, move and add particles.
By default, move will be selected. <br> Scrolling up or down will change the cursor-size,
which gets represented by a circle around your cursor.
- **Move:** When you’re in the ‘move’ mouse-mode, you can move particles by dragging them around.
            The amount of particles that get moved depends on your cursor-size.
            When multiple particles are select and you move one of the particles from your selection,
            all the particles in the selection will be moved.
- **Select:** When you’re in the ‘select’ mouse-mode, you can select particles by clicking or dragging. 
              To deselect them, you can simply click outside of your selection.
              The amount of particles that get selected depends on your cursor-size.
- **Add:** When you’re in the ‘add’ mouse-mode, you can add particles by clicking, 
           dragging or holding the left-mouse button.
           By default, the size of the particles is set to the cursor-size, 
           but you can simply change this setting in the particle-settings tab (see 'particle-settings').
 
 ### Buttons <a name="Buttons"></a>
- **Pause button:** Starts and stops the simulation
- **Link button:** Links the selected particles (does the same as pressing 'L')
- **Unlink button:** 'unlinks' the selected particles (does the same as pressing SHIFT+L)
- **Save button:** Opens dialog window to save the simulation (does the same as pressing CTRL+S)
- **Load button:** Opens dialog window to open a simulation-file (does the same as pressing CTRL+O)
- **Code-window-button:** Opens a window in which you can write and execute code. More info: see 'code-window'-section.
 
### Shortcuts <a name="Shortcuts"></a>
- **RMB:** erase particles
- **DELETE:** delete selected particles
- **SPACE:** pause / unpause simulation
- **CTRL+A:** select all
- **CTRL+C:** copy selected particles
- **CTRL+V:** paste
- **CTRL+X:** cut selected particles
- **CTRL+L:** lock selected particles
- **CTRL+SHIFT+L:** 'unlock' selected particles
- **L:** link selected particles
- **SHIFT+L:** unlink selected particles
- **ALT + L:** fit-link selected particles
- **R (hold) + scroll:** rotate selected particles (rotation amount depends on the cursor-size)
- **CTRL+S:** save simulation
- **CTRL+O:** open/load simulation

Note: Most shortcuts won't work when the canvas isn't 'selected' or 'focused'.
To reset the focus, you can click the canvas with one of the mouse-modes selected.

## Simulation-settings <a name="Simulation-settings"></a>
- **Gravity:** Gravity-strength (float)
- **Air Resistance:** Amount of air resistance, a particle's velocity gets multiplied by "1 - air resistance" 
                      (float, values range from 0 to 1)
- **Ground Friction:** Amount of friction between the edges of the canvas and a particle (float, values range from 0 to 1)
- **Temperature:** Strength of random velocity that gets added to a particle's velocity (float)
- **Simulation Speed:** Speed at which the simulation runs. Does not change the fps! 
                        Setting it too high might result in inaccurate simulations and particles might not be able to go 
                        to a stable position. (float)
- **Display FPS:** When set to True, the current fps will be displayed in the top left corner of the screen (bool)
- **Display # Particles:** When set to True, the amount of particles in the simulation will be displayed in the 
                           top left corner of the screen (bool)
- **Display links:** When set to True, the links between particles that are linked will be displayed as thin lines (bool)
- **Blocking edges:** 'top', 'bottom', 'left' and 'right' checkboxes determine whether that edge of the canvas 
                       acts like a wall (booleans)
- **Use Grid:** When set to True, a grid-optimization (which partitions the canvas into grid-cells 
                and will only check for collisions in the grid-cells that are in a particle’s range) will be used (bool)
- **Grid-Res:** Grid resolution, determines the amount of rows and columns that the optimization will use 
                (x and y: integers)
- **Min-Spawn-Delay:** Affects the rate at which you can spawn particles while dragging, 
                       i.e. value = delay between spawning particles when dragging or holding LMB (float)
- **Better Radii-Calculation:** Essentially, by default, the simulator will assume that two colliding particles have 
                                the same repulsion- and attraction-settings, which is to save time, 
                                but this isn’t always the case. 
                                Activating it will make the forces be calculated in a more realistic way 
                                when the particles have different attraction- or repulsion-radii, 
                                but this is a tiny bit slower and most of the time, you won’t need it. 

### Extra Options Window <a name="Extra_Options_Window"></a>
<sub> To open this window, you have to click on the three dots at the bottom of the simulation settings tab. </sub>

- **Gravity-Angle:** Angle at which gravity pulls on particles (float: °)
- **Wind-Angle:** Angle at which wind pushes particles (only when wind-strength != 0, float: °)
- **Wind-Strength:** Strength at which wind pushes particles (float)
- **Background-Color:** Background color of canvas (change color by pressing 'preview-square' and selecting a color)
- **Void Edges:** By default, particles still get simulated when they're off-screen. 
                  When "Void Edges" is set to True, particles will be deleted when they are off-screen.
- **Fit-link Selected:** Button to fit-link selected particles (same as ALT + L)
- **Stress Visualization:** When set to True, the links of linked particles with breakable links get colored red 
                            based on the forces that that link exerts on the particles. 
                            The final color is the percentage of this force to the maximum force it can support. 
                            If this maximum force is set to a negative number (=unbreakable links), in other words, 
                            if it’s infinite, the links will just display their normal color.
- **Change selected fit-link-length:** When pressing '+' or '-', the length of the links 
                                       between selected particles that are linked will be extended or contracted 
                                       by the amount filled in in the 'spinbox'. When holding '+' or '-', 
                                       the links will continuously be extended or contracted by that amount.

## Linking, fit-linking and particle-groups <a name="Linking,_fit-linking_and_particle-groups"></a>
Each particle belongs to a **particle-group**. By default, a particle will interact with (=attracting and repelling) 
particles that are in its group (this can be changed by turning off 'linked to group-particles', see particle-settings).

**Linking** 2 particles will make it so they interact, even when they don't belong to the same group 
or when 'linked to group-particles' is turned off.

**Fit-linking** works like linking, but instead of using the repulsion-radius as a rest length for the 'springs',
the simulator will use the distance between the particles at the moment of linkage as the rest length.
This means that the particles will try to keep the shape that they were in at the moment of linkage. 
This can for example be used to simulate rigid bodies or more solid structures.

## Particle-settings <a name="Particle-settings"></a>
In the particles-tab, you can see the settings that particles will have when you spawn them. 
You can also change the settings of existing particles using the ‘set selected’ and ‘set all’ buttons. 
To see the properties of a certain particle, you can simply select it and click on ‘copy from selected’. 
This will display all the settings from that particle in the particle-tab. If you do this with 
multiple particles selected, the fields of the settings that they don’t have in common will be left empty.

- **Radius:** Radius of circle drawn on the screen, only affects physics when 'Check Collisions' is set to True 
              (int or 'scroll' to set it to the current cursor-size)
- **Color:** Color of circle drawn on the screen, no effect on physics 
            (change color by pressing 'preview-square' and selecting a color,
             typing it as a list, eg. [255, 0, 0] for red or setting it to 'random' for a random color)
- **Mass:** Mass of particle (float)
- **Bounciness:** Bounciness of particle, particle-velocity gets multiplied by this value when hitting an edge 
                  (float, values range from 0 to 1)
- **Velocity:** Current velocity of particle (x and y components: floats)
- **Locked:** When set to True, the particle won't move, but will still affect other particle (bool)
- **Check Collisions:** Handles particle-collisions, based on radius, does not work when 'Use Grid' is set to True,
                        !not recommended in simulations with many particles: using repel-radius works better (bool)
- **Attraction-radius\*:** Minimum distance between particles before the attraction force gets applied (float)
- **Attr-strength:** Attraction force coefficient (float)
- **Gravity-Mode:** When set to True, attraction force will be calculated with gravity-equation 
                    instead of spring equation (bool)
- **Repulsion-radius:** Minimum distance between particles before the repulsion force gets applied,
                        attraction force won't be applied when repulsion force gets applied (float)
- **Repel-strength:** Repulsion force coefficient (float)
- **Linked to group-particles:** When set to True, makes it so particles will attract and repel the rest of their group 
                                 by default, instead of needing to link them (bool)
- **Link-breaking-force\*:** Maximum attraction- and repulsion-force that a particle's links can support before breaking
                           (attr and repel: float)
- **Particle-group:** Name of group a particle is in. More info: see 'particle-groups' 
                      (use drop-down list to select group, 'group' + int, '+' adds a new group, 
                      select-button automatically selects particles in that group)
- **Separate Group:** When set to True, makes it so the particle isn’t in any particular group, 
                      can for example be used to make a rope collide with itself and not make it intersect itself (bool)

###### *: When setting this to a negative number, this value gets interpreted as infinity
##### Note: You can also write code in the settings-field, eg. 'random.uniform(0, 10)'. <br> Tip: To use the cursor-size as a variable, you can use 'self.mr' (=mouse radius)

## Saving and Loading Simulations <a name="Saving_and_Loading_Simulations"></a>
Saving and loading the simulation can be done using the **save and load** button in the toolbar 
or by pressing **CTRL+S and CTRL+O**.

Saving a simulation **saves the state of each particle** as well as **all current settings**.
The code in the code window is also saved when the code window is closed or when the code is executed.
The text / states of all input fields and check boxes also get saved.

## Code-window <a name="Code-window"></a>
The code-window can be opened using the **'gears'-icon** on the right side of the toolbar. 
In this window, you can **write and execute Python code**. <br>
When an error occurs while running the code, it will be shown as a warning. <br>
The 'Use threading'-checkbox, when set to True, makes the code run in parallel with the simulation. 

**Important!:**
- Implementing a break command (like pausing the simulation) when using loops is recommended!
- Some methods from the simulation-class, such as add_particle(x, y), might not support threading!

These are some examples of code that you can run in the code-window:

**Chaining together particles like a rope more easily:**
```Python
for i in range(1, len(self.particles)):
    self.link([self.particles[i], self.particles[i-1]])
```

**Spawning a 'cloth'** (Set 'Use-threading' to False!):
```Python
cols = 10
rows = 10
spread_x = 40
spread_y = 40
grid = np.empty((rows, cols), dtype=np.object)
for ix, x in enumerate(range(10, 10+spread_x*cols, spread_x)):
	for iy, y in enumerate(range(10, 10+spread_y*rows, spread_y)):
		self.add_particle(x, y)
		grid[iy][ix] = self.particles[-1]
for ix, x in enumerate(range(10, 10+spread_x*cols, spread_x)):
	for iy, y in enumerate(range(10, 10+spread_y*rows, spread_y)):
		if ix > 0:
			self.link([grid[iy][ix], grid[iy][ix-1]], fit_link=True)
		if iy > 0:
			self.link([grid[iy][ix], grid[iy - 1][ix]], fit_link=True)
		if ix > 0 and iy > 0:
			self.link([grid[iy][ix], grid[iy - 1][ix - 1]], fit_link=True)
		if ix < cols-1 and iy > 0:
			self.link([grid[iy][ix], grid[iy - 1][ix + 1]], fit_link=True)
```

**Spawning a 'building'** (Set 'Use-threading' to False!):
```Python
cols = 5
rows = 10
spread_x = 30
spread_y = 30
particles = []
for ix, x in enumerate(range(10, 10+spread_x*cols, spread_x)):
	for iy, y in enumerate(range(10, 10+spread_y*rows, spread_y)):
		self.add_particle(x, y)
		particles.append(self.particles[-1])
self.link(particles, fit_link=True)
```

**Rainbow wave** (Set 'Use-threading' to True!):
```Python
from colorsys import hsv_to_rgb
h = 0
for x in range(50, self.width-49, 6):
	color = [round(i * 255) for i in hsv_to_rgb(h%1, 1, 1)]
	Particle(self, x, 50, radius=4, color=color, mass=1, velocity=np.zeros(2), bounciness=0.9,
           collisions=False, attract_r=0, repel_r=0, attraction_strength=0, repulsion_strength=0,
           linked_group_particles=False)
	h += 0.03
	time.sleep(0.02)
```
