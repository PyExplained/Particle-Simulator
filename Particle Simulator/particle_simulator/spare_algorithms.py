metaballs = []
for particle in self.particles:
    particle.update(self.grid)
    if particle.render_mode == 'SPHERE':
        image = cv2.circle(image, (int(particle.x), int(particle.y)), particle.r, particle.color, -1)
    elif particle.render_mode == 'BLOB':
        metaballs.append(particle)

if len(metaballs) > 0:
    low_width = 40
    factor = low_width / self.width
    low_height = int(self.height * factor)
    metaball_image = np.zeros((low_height, low_width, 3))

    # for m in metaballs:
    #     cv2.circle(metaball_image, (int(np.floor(m.x * factor)), int(np.floor(m.y * factor))),
    #                int(np.floor(m.r * factor)), m.color, -1)

    for y in range(low_height):
        for x in range(low_width):
            # Setup
            r = 0.0
            g = 0.0
            b = 0.0
            sum_ = 0.0

            # Calc power
            for m in metaballs:
                dx = x - m.x * factor
                dy = y - m.y * factor
                dst = 1 / max(dx**2 + dy**2, 0.0001)

                r += dst * m.color[0]
                g += dst * m.color[1]
                b += dst * m.color[2]
                sum_ += dst * m.r * factor

            # Normalize rgb
            length = np.sqrt(r**2 + g**2 + b**2)
            r /= length
            g /= length
            b /= length
            sum_ /= len(metaballs)

            if sum_ >= 0.05:
                r = int(r * 255)
                g = int(g * 255)
                b = int(b * 255)
                metaball_image[y][x] = [r, g, b]

metaball_image = cv2.resize(metaball_image, (self.width, self.height))
image = metaball_image
# cnd = metaball_image > 0
# image[cnd] = metaball_image[cnd]

# Debugging
# for particle in self.particles:
#     image = cv2.circle(image, (int(particle.x), int(particle.y)), particle.r, particle.color, -1)

# Debugging
# low_width = 30
# factor = low_width / self.width
# low_height = int(self.height * factor)
# image = cv2.resize(image.astype('uint8'), (low_width, low_height), interpolation=cv2.INTER_AREA)
# image = cv2.resize(image, (self.width, self.height))