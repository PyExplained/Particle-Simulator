from particle_simulator import *


class Grid:
    def __init__(self, sim, rows, columns):
        self.sim = sim
        self.grid = None
        self.rows = rows
        self.columns = columns
        self.row_height = sim.gui.height / self.rows
        self.column_width = sim.gui.width / self.columns

    def init_grid(self):
        self.grid = np.empty((self.rows, self.columns), dtype=np.object)
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i, j] = []

        for particle in self.sim.particles:
            row = self.return_row(particle.y)
            column = self.return_column(particle.x)
            if 0 <= row < self.rows and 0 <= column < self.columns:
                self.grid[int(row), int(column)].append(particle)

    def return_row(self, y):
        return min(int(y // self.row_height), self.rows - 1)

    def return_column(self, x):
        return min(int(x // self.column_width), self.rows - 1)

    def return_particles(self, particle):
        if particle.return_none:
            return []
        if particle.return_all:
            return self.sim.particles

        min_row = self.return_row(particle.y - particle.range_)
        max_row = self.return_row(particle.y + particle.range_)
        min_col = self.return_column(particle.x - particle.range_)
        max_col = self.return_column(particle.x + particle.range_)

        if particle.attr == 0 and particle.repel == 0 and not particle.collision_bool:
            return []
        if particle.attr_r < 0 and particle.attr != 0:
            return self.sim.particles

        near_particles = []
        for i in range(min_row, max_row + 1):
            for j in range(min_col, max_col + 1):
                if 0 <= i < self.rows and 0 <= j < self.columns:
                    near_particles += self.grid[i][j]

        return near_particles
