from particle_simulator import *


class Simulation:
    def __init__(self, width=650, height=600, title="Simulation", gridres=(50, 50),
                 temperature=0, g=0.1, air_res=0.05, ground_friction=0, fps_update_delay=0.5):
        self.width = width
        self.height = height
        
        self.temperature = temperature
        self.g = g  # gravity
        self.g_dir = np.array([0, 1])
        self.g_vector = np.array([0, -g])
        self.wind_force = np.array([0, 0])
        self.air_res = air_res
        self.air_res_calc = 1 - self.air_res
        self.ground_friction = ground_friction
        self.speed = 1

        self.fps = 0
        self.fps_update_delay = fps_update_delay
        self.mx, self.my = 0, 0
        self.prev_mx, self.prev_my = 0, 0
        self.mouse_mode = 'MOVE'  # 'SELECT', 'MOVE', 'ADD'
        self.rotate_mode = False
        self.min_spawn_delay = 0.05
        self.min_hold_delay = 1
        self.last_mouse_time = 0
        self.mr = 5
        self.mouse_down = False
        self.mouse_down_start = None
        self.shift = False
        self.start_save = False
        self.start_load = False
        self.paused = True
        self.toggle_pause = False
        self.running = True
        self.focus = True
        self.error = None
        self.use_grid = True
        self.calculate_radii_diff = False

        self.top = True
        self.bottom = True
        self.left = True
        self.right = True
        self.void_edges = False

        self.bg_color = [[255, 255, 255], "#ffffff"]
        self.stress_visualization = False
        self.link_colors = []

        self.code = 'print("Hello World")'

        self.gui = GUI(self, title, gridres)
        self.grid = Grid(self, *gridres)
        self.save_manager = SaveManager(self)

        # Keyboard- and mouse-controls
        self.gui.canvas.bind('<B1-Motion>', self.mouse_m)
        self.gui.canvas.bind('<Button-1>', self.mouse_p)
        self.gui.canvas.bind('<ButtonRelease-1>', self.mouse_r)
        self.gui.canvas.bind('<B3-Motion>', self.right_mouse)
        self.gui.canvas.bind('<Button-3>', self.right_mouse)
        self.gui.canvas.bind("<MouseWheel>", self.on_scroll)

        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

        self.start_time = time.time()
        self.prev_time = self.start_time

        self.particles = []
        self.selection = []
        self.clipboard = []
        self.pasting = False
        self.groups = {'group1': []}

    def mouse_p(self, event):
        self.gui.canvas.focus_set()
        self.mouse_down_start = time.time()
        self.mouse_down = True
        if self.mouse_mode == 'SELECT' or self.mouse_mode == 'MOVE':
            selected = False
            for p in self.particles:
                if p.mouse_p(event):
                    selected = True
            if not selected:
                self.selection = []
            elif self.mouse_mode == 'MOVE':
                for particle in self.selection:
                    particle.mouse = True
        elif self.mouse_mode == 'ADD':
            if len(self.selection) > 0:
                self.selection = []

            self.add_particle(event.x, event.y)

    def mouse_m(self, event):
        if self.mouse_mode == 'SELECT':
            for p in self.particles:
                p.mouse_p(event)
        elif self.mouse_mode == 'ADD' and time.time() - self.last_mouse_time >= self.min_spawn_delay:
            self.add_particle(event.x, event.y)

    def mouse_r(self, event):
        self.mouse_down = False
        if self.mouse_mode == 'MOVE' or self.pasting:
            for p in self.particles:
                if p.mouse:
                    p.mouse_r(event)
        self.pasting = False

    def right_mouse(self, event):
        self.gui.canvas.focus_set()
        temp = self.particles.copy()
        for p in temp:
            if np.sqrt((event.x - p.x) ** 2 + (event.y - p.y) ** 2) <= max(int(self.mr), p.r):
                p.delete()

    def rotate_2d(self, x, y, cx, cy, angle):
        angle_rad = -np.radians(angle)
        dist_x = x - cx
        dist_y = y - cy
        current_angle = math.atan2(dist_y, dist_x)
        angle_rad += current_angle
        radius = np.sqrt(dist_x ** 2 + dist_y ** 2)
        x = cx + radius * np.cos(angle_rad)
        y = cy + radius * np.sin(angle_rad)

        return x, y

    def on_scroll(self, event):
        if self.rotate_mode:
            for p in self.selection:
                p.x, p.y = self.rotate_2d(p.x, p.y, event.x, event.y, event.delta / 500 * self.mr)
        else:
            self.mr = max(self.mr * 2 ** (event.delta / 500), 1)

    def on_press(self, key):
        if self.focus:
            # SPACE to pause
            if key == Key.space:
                self.toggle_paused()
            # DELETE to delete
            elif key == Key.delete:
                temp = self.selection.copy()
                for p in temp:
                    p.delete()
            elif key == Key.shift_l or key == Key.shift_r:
                self.shift = True
            # CTRL + A to select all
            elif KeyCode.from_char(key).char == r"'\x01'":
                for p in self.particles:
                    p.select()
            # CTRL + C to copy
            elif KeyCode.from_char(key).char == r"'\x03'":
                self.copy_selected()
            # CTRL + V to copy
            elif KeyCode.from_char(key).char == r"'\x16'":
                self.paste()
            # CTRL + X to cut
            elif KeyCode.from_char(key).char == r"'\x18'":
                self.cut()
            # CTRL + L and CTRL + SHIFT + L to lock and 'unlock'
            elif KeyCode.from_char(key).char == r"'\x0c'" and not self.shift:
                for p in self.selection:
                    p.locked = True
            elif KeyCode.from_char(key).char == r"'\x0c'" and self.shift:
                for p in self.selection:
                    p.locked = False
            # L to link, SHIFT + L to unlink and ALT GR + L to fit-link
            elif KeyCode.from_char(key).char == "'l'":
                self.link_selection()
            elif KeyCode.from_char(key).char == "<76>":
                self.link_selection(fit_link=True)
            elif KeyCode.from_char(key).char == "'L'":
                self.unlink_selection()
            # R to enter rotate-mode
            elif KeyCode.from_char(key).char == "'r'":
                self.rotate_mode = True
            # CTRL + S to save
            elif KeyCode.from_char(key).char == r"'\x13'":
                self.start_save = True  # Threading-issues
            # CTRL + O to load / open
            elif KeyCode.from_char(key).char == r"'\x0f'":
                self.start_load = True

    def on_release(self, key):
        if key == Key.shift_l or key == Key.shift_r:
            self.shift = False
        elif KeyCode.from_char(key).char == "'r'":
            self.rotate_mode = False

    def update_grid(self, *event):
        try:
            self.grid = Grid(self, self.gui.grid_res_x_value.get(), self.gui.grid_res_y_value.get())
        except:
            pass

    def toggle_paused(self):
        self.toggle_pause = True

    def change_mode(self, mode):
        self.mouse_mode = mode
        if mode == 'SELECT':
            self.gui.gui_canvas.itemconfig(self.gui.select_rect, state='normal')
            self.gui.gui_canvas.itemconfig(self.gui.move_rect, state='hidden')
            self.gui.gui_canvas.itemconfig(self.gui.add_rect, state='hidden')
        elif mode == 'MOVE':
            self.gui.gui_canvas.itemconfig(self.gui.select_rect, state='hidden')
            self.gui.gui_canvas.itemconfig(self.gui.move_rect, state='normal')
            self.gui.gui_canvas.itemconfig(self.gui.add_rect, state='hidden')
        elif mode == 'ADD':
            self.gui.gui_canvas.itemconfig(self.gui.select_rect, state='hidden')
            self.gui.gui_canvas.itemconfig(self.gui.move_rect, state='hidden')
            self.gui.gui_canvas.itemconfig(self.gui.add_rect, state='normal')

    def add_group(self):
        for i in range(1, max(self.gui.group_indices) + 2):
            if i not in self.gui.group_indices:
                name = f'group{i}'
                self.gui.group_indices.append(i)
                self.gui.groups_entry['values'] = [f'group{index}' for index in sorted(self.gui.group_indices)]
                self.gui.groups_entry.current(i - 1)
                self.groups[name] = []
                break

    def select_group(self):
        self.selection = []
        for p in self.groups[self.gui.groups_entry.get()]:
            p.select()

    def inputs2dict(self):
        try:
            radius = int(self.mr) if self.gui.radius_entry.get() == 'scroll' else eval(self.gui.radius_entry.get())

            try:
                color = self.gui.color_entry.get().replace('[', '').replace(']', '').split(',')
                color = list(map(lambda x: int(x), color))
            except ValueError:
                color = self.gui.color_entry.get()

            kwargs = {'mass': self.gui.mass_entry.get(),
                      'velocity': [self.gui.velocity_x_entry.get(), self.gui.velocity_y_entry.get()],
                      'bounciness': self.gui.bounciness_entry.get(),
                      'attract_r': self.gui.attr_r_entry.get(),
                      'repel_r': self.gui.repel_r_entry.get(),
                      'attraction_strength': self.gui.attr_strength_entry.get(),
                      'repulsion_strength': self.gui.repel_strength_entry.get(),
                      'link_attr_breaking_force': self.gui.link_attr_break_entry.get(),
                      'link_repel_breaking_force': self.gui.link_repel_break_entry.get(),
                      }

            for key, value in kwargs.items():
                try:
                    kwargs[key] = eval(value)
                except TypeError:
                    for i, element in enumerate(value):
                        kwargs[key][i] = eval(element)

            kwargs['radius'] = radius
            kwargs['color'] = color
            kwargs['collisions'] = self.gui.do_collision_bool.get()
            kwargs['locked'] = self.gui.locked_bool.get()
            kwargs['linked_group_particles'] = self.gui.linked_group_bool.get()
            kwargs['group'] = self.gui.groups_entry.get()
            kwargs['separate_group'] = self.gui.separate_group_bool.get()
            kwargs['gravity_mode'] = self.gui.gravity_mode_bool.get()

            return kwargs
        except Exception as error:
            self.error = ['Input-Error', error]

    def set_selected(self):
        kwargs = self.inputs2dict()
        if kwargs is not None:
            temp = self.selection.copy()
            for p in temp:
                temp_link_lengths = p.link_lengths.copy()
                px, py = p.x, p.y
                p.delete()
                p = Particle(self, px, py, **kwargs)
                self.selection.append(p)
                for link, length in temp_link_lengths.items():
                    self.link([link, p], fit_link=length != 'repel', distance=length)

    def set_all(self):
        temp = self.particles.copy()
        for p in temp:
            kwargs = self.inputs2dict()  # Update for each particle in case of 'random'
            if kwargs is not None:
                temp_link_lengths = p.link_lengths.copy()
                px, py = p.x, p.y
                p.delete()
                p = Particle(self, px, py, **kwargs)
                for link, length in temp_link_lengths.items():
                    self.link([link, p], fit_link=length != 'repel', distance=length)

    def copy_from_selected(self):
        variable_names = {'radius_entry': ['r', 'entry'],
                          'color_entry': ['color', 'entry'],
                          'mass_entry': ['m', 'entry'],
                          'velocity_x_entry': ['v[0]', 'entry'],
                          'velocity_y_entry': ['v[1]', 'entry'],
                          'bounciness_entry': ['bounciness', 'entry'],
                          'do_collision_bool': ['collision_bool', 'set'],
                          'locked_bool': ['locked', 'set'],
                          'linked_group_bool': ['linked_group_particles', 'set'],
                          'attr_r_entry': ['attr_r', 'entry'],
                          'repel_r_entry': ['repel_r', 'entry'],
                          'attr_strength_entry': ['attr', 'entry'],
                          'repel_strength_entry': ['repel', 'entry'],
                          'link_attr_break_entry': ['link_attr_breaking_force', 'entry'],
                          'link_repel_break_entry': ['link_repel_breaking_force', 'entry'],
                          'groups_entry': ['group', 'entry'],
                          'separate_group_bool': ['separate_group', 'set'],
                          'gravity_mode_bool': ['gravity_mode', 'set']
                          }
        particle_settings = variable_names.copy()

        for i, p in enumerate(self.selection):
            for key, value in variable_names.items():
                val = eval('p.' + value[0])

                if i == 0:
                    particle_settings[key] = val

                same = particle_settings[key] == val
                if value[1] == 'set':
                    if same:
                        vars(self.gui)[key].set(val)
                    else:
                        vars(self.gui)[key].set(False)
                else:
                    if same:
                        vars(self.gui)[key].delete(0, END)
                        vars(self.gui)[key].insert(0, str(val))
                    else:
                        vars(self.gui)[key].delete(0, END)

    def add_particle(self, x, y):
        kwargs = self.inputs2dict()
        if kwargs is not None:
            Particle(self, x, y, **kwargs)

            self.last_mouse_time = time.time()

    def copy_selected(self):
        self.clipboard = []
        for p in self.selection:
            dictionary = p.return_dict(index_source=self.selection)
            dictionary['x'] -= self.mx
            dictionary['y'] -= self.my
            self.clipboard.append(dictionary)

    def paste(self):
        self.pasting = True
        temp_particles = []
        for data in self.clipboard:
            temp_particles.append(Particle(self, 0, 0, group=data['group']))

        for i, d in enumerate(self.clipboard):
            particle = temp_particles[i]
            d['x'] += self.mx
            d['y'] += self.my
            for key, value in d.items():
                vars(particle)[key] = value

            particle.init_constants()
            particle.linked = [temp_particles[index] for index in particle.linked]
            particle.link_lengths = {temp_particles[index]: value for index, value in
                                     particle.link_lengths.items()}
            particle.mouse = True
        self.selection = temp_particles

    def cut(self):
        self.copy_selected()
        temp = self.selection.copy()
        for p in temp:
            p.delete()

    def link_selection(self, fit_link=False):
        self.link(self.selection, fit_link=fit_link)
        self.selection = []

    def unlink_selection(self):
        self.unlink(self.selection)
        self.selection = []

    def link(self, particles, fit_link=False, distance=None):
        for p in particles:
            if fit_link:
                position = np.array([p.x, p.y])

            for particle in particles:
                if fit_link:
                    length = np.linalg.norm(
                        position - np.array([particle.x, particle.y])) if distance is None else distance
                p.link_lengths[particle] = length if fit_link else 'repel'

            p.linked = list(set(p.linked + particles.copy()))
            p.linked.remove(p)
            del p.link_lengths[p]

    def unlink(self, particles):
        for p in particles:
            p.linked = [link for link in p.linked if link not in particles]
            p.link_lengths = {link: length for link, length in p.link_lengths.items() if link not in particles}

    def change_link_lengths(self, particles, amount):
        for p in particles:
            for link, value in p.link_lengths.items():
                if value != 'repel':
                    self.link([p, link], fit_link=True, distance=value + amount)

    def execute(self, code):
        try:
            exec(code)
        except Exception as error:
            self.error = ['Code-Error:', error]

    def update_vars(self):
        for var, entry in [('g', 'gravity_entry'), ('air_res', 'air_res_entry'), ('ground_friction', 'friction_entry'),
                           ('use_grid', 'grid_bool'), ('min_spawn_delay', 'delay_entry'),
                           ('calculate_radii_diff', 'calculate_radii_diff_bool')]:
            try:
                vars(self)[var] = float(eval(vars(self.gui)[entry].get()))
            except:
                pass

        self.temperature = self.gui.temp_sc.get()
        self.speed = self.gui.speed_sc.get()

        self.top = self.gui.top_bool.get()
        self.bottom = self.gui.bottom_bool.get()
        self.left = self.gui.left_bool.get()
        self.right = self.gui.right_bool.get()
        self.use_grid = self.gui.grid_bool.get()
        self.calculate_radii_diff = self.gui.calculate_radii_diff_bool.get()

    def simulate(self):
        while self.running:
            self.gui.canvas.delete("all")
            image = np.full((self.height, self.width, 3), self.bg_color[0])
            self.link_colors = []

            self.update_vars()
            self.g_vector = self.g_dir * self.g
            self.air_res_calc = (1 - self.air_res) ** self.speed
            if self.gui.grid_bool.get():
                self.grid.init_grid()
            if self.toggle_pause:
                self.paused = not self.paused
                self.gui.pause_button.config(image=self.gui.play_photo if self.paused else self.gui.pause_photo)

                if not self.paused:
                    self.selection = []
                self.toggle_pause = False

            if self.mouse_down and time.time() - self.mouse_down_start >= self.min_hold_delay:
                event = Event()
                event.x, event.y = self.mx, self.my
                self.mouse_m(event)

            try:
                self.focus = type(self.gui.tk.focus_displayof()) in [Canvas, Tk]
            except KeyError:
                # Combobox
                self.focus = False

            if self.error is not None:
                messagebox.showerror(*self.error)
                self.error = None

            if self.start_save:
                self.save_manager.save()
                self.start_save = False

            if self.start_load:
                self.save_manager.load()
                self.start_load = False

            for particle in self.particles:
                particle.update(self.grid)

            if self.gui.show_links.get():
                if self.stress_visualization and not self.paused:
                    for p1, p2, percentage in self.link_colors:
                        color = [max(255 * percentage, 235)] + [235 * (1 - percentage)] * 2
                        cv2.line(image, (int(p1.x), int(p1.y)), (int(p2.x), int(p2.y)), color, 1)
                else:
                    for p1 in self.particles:
                        for p2 in p1.linked:
                            cv2.line(image, (int(p1.x), int(p1.y)), (int(p2.x), int(p2.y)), [235] * 3, 1)

            for particle in self.particles:
                cv2.circle(image, (int(particle.x), int(particle.y)), particle.r, particle.color, -1)

            for particle in self.selection:
                cv2.circle(image, (int(particle.x), int(particle.y)), particle.r, [0, 0, 255], 2)

            cv2.circle(image, (self.mx, self.my), int(self.mr), [127] * 3)

            if time.time() - self.start_time >= self.fps_update_delay:
                try:
                    self.fps = 1 / (time.time() - self.prev_time)
                except ZeroDivisionError:
                    pass
                self.start_time = time.time()
            self.prev_time = time.time()

            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image.astype(np.uint8)), master=self.gui.tk)
            self.gui.canvas.create_image(0, 0, image=photo, anchor=NW)
            if self.gui.show_fps.get():
                self.gui.canvas.create_text(10, 10, text=f"FPS: {round(self.fps, 2)}", anchor='nw',
                                        font=('Helvetica', 9, 'bold'))
            if self.gui.show_num.get():
                self.gui.canvas.create_text(10, 25, text=f"Particles: {len(self.particles)}", anchor='nw',
                                        font=('Helvetica', 9, 'bold'))

            self.prev_mx, self.prev_my = self.mx, self.my
            self.mx = self.gui.tk.winfo_pointerx() - self.gui.tk.winfo_rootx()
            self.my = self.gui.tk.winfo_pointery() - self.gui.tk.winfo_rooty() - 30

            self.gui.update()
