from particle_simulator import *


class SaveManager:
    def __init__(self, sim):
        self.sim = sim
        self.filename = 'simulation'

    def save(self):
        filename = asksaveasfilename(initialdir=".",
                                     initialfile=self.filename,
                                     defaultextension=".sim",
                                     filetypes=[("Simulation files", '*.sim'), ("All Files", "*.*")])

        if filename != '':
            try:
                sim_settings = {'gravity_entry': [self.sim.gui.gravity_entry.get(), 'entry'],
                                'air_res_entry': [self.sim.gui.air_res_entry.get(), 'entry'],
                                'friction_entry': [self.sim.gui.friction_entry.get(), 'entry'],
                                'temp_sc': [self.sim.gui.temp_sc.get(), 'set'],
                                'speed_sc': [self.sim.gui.speed_sc.get(), 'set'],
                                'show_fps': [self.sim.gui.show_fps.get(), 'set'],
                                'show_num': [self.sim.gui.show_num.get(), 'set'],
                                'show_links': [self.sim.gui.show_links.get(), 'set'],
                                'top_bool': [self.sim.gui.top_bool.get(), 'set'],
                                'bottom_bool': [self.sim.gui.bottom_bool.get(), 'set'],
                                'left_bool': [self.sim.gui.left_bool.get(), 'set'],
                                'right_bool': [self.sim.gui.right_bool.get(), 'set'],
                                'grid_bool': [self.sim.gui.grid_bool.get(), 'set'],
                                'grid_res_x_value': [self.sim.gui.grid_res_x_value.get(), 'set'],
                                'grid_res_y_value': [self.sim.gui.grid_res_y_value.get(), 'set'],
                                'delay_entry': [self.sim.gui.delay_entry.get(), 'entry'],
                                'calculate_radii_diff_bool': [self.sim.gui.calculate_radii_diff_bool.get(), 'set'],
                                'g_dir': [self.sim.g_dir, 'var'],
                                'wind_force': [self.sim.wind_force, 'var'],
                                'stress_visualization': [self.sim.stress_visualization, 'var'],
                                'bg_color': [self.sim.bg_color, 'var'],
                                'void_edges': [self.sim.void_edges, 'var'],
                                'code': [self.sim.code, 'var']
                                }

                particle_settings = {'radius_entry': [self.sim.gui.radius_entry.get(), 'entry'],
                                     'color_entry': [self.sim.gui.color_entry.get(), 'entry'],
                                     'mass_entry': [self.sim.gui.mass_entry.get(), 'entry'],
                                     'velocity_x_entry': [self.sim.gui.velocity_x_entry.get(), 'entry'],
                                     'velocity_y_entry': [self.sim.gui.velocity_y_entry.get(), 'entry'],
                                     'bounciness_entry': [self.sim.gui.bounciness_entry.get(), 'entry'],
                                     'do_collision_bool': [self.sim.gui.do_collision_bool.get(), 'set'],
                                     'locked_bool': [self.sim.gui.locked_bool.get(), 'set'],
                                     'linked_group_bool': [self.sim.gui.linked_group_bool.get(), 'set'],
                                     'attr_r_entry': [self.sim.gui.attr_r_entry.get(), 'entry'],
                                     'repel_r_entry': [self.sim.gui.repel_r_entry.get(), 'entry'],
                                     'attr_strength_entry': [self.sim.gui.attr_strength_entry.get(), 'entry'],
                                     'gravity_mode_bool': [self.sim.gui.gravity_mode_bool.get(), 'set'],
                                     'repel_strength_entry': [self.sim.gui.repel_strength_entry.get(), 'entry'],
                                     'link_attr_break_entry': [self.sim.gui.link_attr_break_entry.get(), 'entry'],
                                     'link_repel_break_entry': [self.sim.gui.link_repel_break_entry.get(), 'entry'],
                                     'groups_entry': [self.sim.gui.groups_entry.get(), 'entry'],
                                     'separate_group_bool': [self.sim.gui.separate_group_bool.get(), 'set']
                                     }

                data = {'particles': [particle.return_dict() for particle in self.sim.particles],
                        'particle-settings': particle_settings,
                        'sim-settings': sim_settings}

                pickle.dump(data, open(filename, "wb"))

                self.filename = os.path.basename(filename)
            except Exception as error:
                self.sim.error = ('Saving-Error', error)

    def load(self):
        if not self.sim.paused:
            self.sim.toggle_paused()

        filename = askopenfilename(initialdir=".",
                                   initialfile=self.filename,
                                   defaultextension=".sim",
                                   filetypes=[("Simulation files", '*.sim'), ("All Files", "*.*")])

        if filename != '':
            try:
                data = pickle.load(open(filename, "rb"))

                for key, value in list(data['particle-settings'].items()) + list(data['sim-settings'].items()):
                    if value[1] == 'set':
                        vars(self.sim.gui)[key].set(value[0])
                    elif value[1] == 'var':
                        vars(self.sim)[key] = value[0]
                    else:
                        vars(self.sim.gui)[key].delete(0, END)
                        vars(self.sim.gui)[key].insert(0, value[0])

                temp = self.sim.particles.copy()
                for p in temp:
                    p.delete()

                self.sim.groups = {}
                self.sim.gui.group_indices = []
                self.sim.gui.groups_entry['values'] = []
                for i in range(len(data['particles'])):
                    Particle(self.sim, 0, 0, group=data['particles'][i]['group'])

                for i, d in enumerate(data['particles']):
                    particle = self.sim.particles[i]

                    for key, value in d.items():
                        vars(particle)[key] = value
                    particle.sim = self.sim
                    particle.init_constants()

                    particle.linked = [self.sim.particles[index] for index in particle.linked]
                    particle.link_lengths = {self.sim.particles[index]: value for index, value in
                                             particle.link_lengths.items()}

                self.filename = os.path.basename(filename)
            except Exception as error:
                self.sim.error = ('Loading-Error', error)
