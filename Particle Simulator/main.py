from particle_simulator import *

sim = Simulation(width=650, height=600, title="Simulation", gridres=(50, 50),
                 temperature=0, g=0, air_res=0.05, ground_friction=0)

# Random particle-positions
for i in range(50):
    s = 4
    Particle(sim, random.normalvariate(sim.gui.width / 2, sim.gui.width / 5),
             random.normalvariate(sim.gui.height / 2, sim.gui.height / 5), radius=s,
             color=np.random.randint(0, 255, 3).tolist(),
             mass=1, bounciness=0.7, velocity=np.zeros(2), collisions=False,
             attract_r=-1, repel_r=10, attraction_strength=0.25, repulsion_strength=1)

# Code for code-win

# Rope
# for i in range(1, len(self.particles)):
#     self.link([self.particles[i], self.particles[i-1]])

# Cloth
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

# 'Building'
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

sim.simulate()
