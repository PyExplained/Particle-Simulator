from particle_simulator import *

sim = Simulation(width=650, height=600, title="Simulation", gridres=(50, 50),
                 temperature=0, g=0, air_res=0.05, ground_friction=0)

# Random particle-positions
for i in range(50):
    s = 4
    Particle(sim, random.normalvariate(sim.width / 2, sim.width / 5),
             random.normalvariate(sim.height / 2, sim.height / 5), radius=s,
             color=np.random.randint(0, 255, 3).tolist(),
             mass=1, bounciness=0.7, velocity=np.zeros(2), collisions=False,
             attract_r=-1, repel_r=10, attraction_strength=0.25, repulsion_strength=1)

# Rope (for code-window)
# for i in range(1, len(self.particles)):
#     self.link([self.particles[i], self.particles[i-1]])

# Cloth (for code-window)
# cols = 10
# rows = 10
# spread_x = 40
# spread_y = 40
# grid = np.empty((rows, cols), dtype=np.object)
#
# for ix, x in enumerate(range(10, 10+spread_x*cols, spread_x)):
# 	for iy, y in enumerate(range(10, 10+spread_y*rows, spread_y)):
# 		self.add_particle(x, y)
# 		grid[iy][ix] = self.particles[-1]
#
# for ix, x in enumerate(range(10, 10+spread_x*cols, spread_x)):
# 	for iy, y in enumerate(range(10, 10+spread_y*rows, spread_y)):
# 		if ix > 0:
# 			self.link([grid[iy][ix], grid[iy][ix-1]], fit_link=True)
# 		if iy > 0:
# 			self.link([grid[iy][ix], grid[iy - 1][ix]], fit_link=True)
# 		if ix > 0 and iy > 0:
# 			self.link([grid[iy][ix], grid[iy - 1][ix - 1]], fit_link=True)
# 		if ix < cols-1 and iy > 0:
# 			self.link([grid[iy][ix], grid[iy - 1][ix + 1]], fit_link=True)

# 'Building' (for code-window)
# cols = 5
# rows = 10
# spread_x = 30
# spread_y = 30
# particles = []
# for ix, x in enumerate(range(10, 10+spread_x*cols, spread_x)):
# 	for iy, y in enumerate(range(10, 10+spread_y*rows, spread_y)):
# 		self.add_particle(x, y)
# 		particles.append(self.particles[-1])
# self.link(particles, fit_link=True)

# Rainbow wave (for code-window)
# from colorsys import hsv_to_rgb
#
# h = 0
# for x in range(50, self.width-49, 6):
# 	color = [round(i * 255) for i in hsv_to_rgb(h%1, 1, 1)]
# 	Particle(self, x, 50, radius=4, color=color, mass=1, velocity=np.zeros(2), bounciness=0.9,
#            collisions=False, attract_r=0, repel_r=0, attraction_strength=0, repulsion_strength=0,
#            linked_group_particles=False)
# 	h += 0.03
# 	time.sleep(0.02)

# Solar/star-system
# sim.gui.air_res_entry.delete(0, END)
# sim.gui.air_res_entry.insert(0, 0)
# attraction_constant = 10**-3
# gravitational_constant = attraction_constant * 20
#
#
# def add_planet(x, y, r=20, color=None, m=100, v=10, center=np.zeros(2)):
#     if v != 0:
#         center_vector = center - np.array([x, y])
#         center_vector = center_vector / np.linalg.norm(center_vector)
#         velocity = v * np.array([center_vector[1], -center_vector[0]])
#     else:
#         velocity = np.zeros(2)
#     Particle(sim, x, y, radius=r,
#              color=color, mass=m, bounciness=0.7, velocity=velocity,
#              collisions=False, attract_r=-1, repel_r=r, attraction_strength=attraction_constant,
#              repulsion_strength=1, gravity_mode=True)
#
#
# # Central planet
# m_central = 10**5
# center_ = np.array([sim.width / 2, sim.height / 2])
# add_planet(*center_, r=10, color=[255, 0, 0],
#            m=m_central, v=0, center=np.array([sim.width / 2, sim.height / 2]))
# # Outer planets
# # outer_planets = [
# #     {'x': 100, 'y': 0, 'r': 5, 'm': 10, 'color': [255, 255, 0], 'center': [0, 0], 'central_m': m_central},
# #     {'x': 200, 'y': 0, 'r': 3, 'm': 10, 'color': [0, 255, 0], 'center': [0, 0], 'central_m': m_central}
# # ]
# outer_planets = [
#     {'x': x, 'y': 0, 'r': 5, 'm': 1, 'color': np.random.randint(0, 255, 3).tolist(), 'center': [0, 0],
#      'central_m': m_central} for x in range(50, 300, 20)
# ]
#
# for planet in outer_planets:
#     x = planet['x']
#     y = planet['y']
#     r = planet['r']
#     m = planet['m']
#     color = planet['color']
#     center = planet['center']
#     central_m = planet['central_m']
#     v = np.sqrt(gravitational_constant * central_m / np.linalg.norm(np.array([x, y])))
#     add_planet(center_[0] + center[0] + x, center_[1] + center[1] + y, r=r, m=m, color=color,
#                v=v, center=np.array(center_ + center))

sim.simulate()
