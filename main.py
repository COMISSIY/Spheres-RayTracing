import pygame, math, sys
pygame.init()

w, h = 600, 400
ratio = w/h
sc = pygame.display.set_mode((w, h))
pygame.display.set_caption(str(sys.argv[0].split("/")[-1]))
res = 10
x_a = 0
y_a = 0
c_pos = pygame.Vector3((-10, -10, -10))
n = -10
def rotate_y(p, a):
	x = p[0]*math.cos(a)+p[2]*math.sin(a)
	y = p[1]
	z = -p[0]*math.sin(a)+p[2]*math.cos(a)
	return pygame.Vector3((x, y, z))

def rotate_x(p, a):
	x = p[0]
	y = p[1]*math.cos(a)+p[2]*math.sin(a)
	z = -p[1]*math.sin(a)+p[2]*math.cos(a)
	return pygame.Vector3((x, y, z))

def sphereIN(ro, rd, ce, ra):
	oc = ro - ce
	b = oc.dot(rd)
	c = oc.dot(oc) - ra ** 2
	h = b ** 2 - c
	
	if h < 0:
		return pygame.Vector2(-1)
	h = math.sqrt(h)
	return pygame.Vector2(-b - h, -b+h)

def plateIN(ro, rd, p):
	a = rd.dot(p.xyz)
	if a == 0:
		a = 0.001
	return -(ro.dot(p.xyz) + 1) / a

def raycast(vec, pos, color, level=200, is_ref = False):
	ray = vec
	if not is_ref:
		ray = rotate_x(ray, x_a)
		ray = rotate_y(ray, y_a)
	rd = (pos + ray).normalize()
	z_buff = {}
	for i in objects:
		if i[0] == "sphere":
			dist = sphereIN(pos, rd, i[1], i[3])
			if dist.x > 0:
				ray_point = pos + rd * dist.x
				ref_v = (ray_point - i[1])
				
				if level > 0:
					color = raycast(rd.reflect(ref_v)*10000, ray_point, (i[2]+color)/2*0.8, level-1, True)
					z_buff[dist.x] = color
		if i[0] == "plate":
			dist = plateIN(pos, rd, i[1])
			if dist > 0:
				ray_point = pos + rd * dist
				dop = i[1].xyz
				dop.xz = ray_point.xz
				ref_v = (ray_point - dop)*10000
				
				if level > 0:
					color = raycast(rd.reflect(ref_v)*10000, ray_point, (i[2]+color)/2*0.8, level-1, True)
					z_buff[dist] = color
	if len(z_buff) != 0:
		return z_buff[min(list(z_buff))] * 0.8

	return color *0.8

objects = [["sphere", pygame.Vector3((0, -10, 100)), pygame.Vector3((255, 0, 0)), 10], ["sphere", pygame.Vector3((30, -100, 100)), pygame.Vector3((255, 255, 0)), 2], ["plate", pygame.Vector3((0, 1, 0)), pygame.Vector3((255, 255, 255))], ["sphere", pygame.Vector3((30, -5, 100)), pygame.Vector3((255, 0, 255)), 5]]

while True:
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			exit()

	for nx, x in enumerate(range(-w//2, w//2, res)):
		for ny, y in enumerate(range(-h//2, h//2, res)):
			color = raycast(pygame.Vector3((x, y, 1000))*ratio, c_pos, pygame.Vector3((255, 255, 255)))
			pygame.draw.rect(sc, color, (nx*res, ny*res, res, res))
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:
		y_a -= 0.1
	if keys[pygame.K_RIGHT]:
		y_a += 0.1
	if keys[pygame.K_UP]:
		x_a -= 0.1
	if keys[pygame.K_DOWN]:
		x_a += 0.1
	if keys[pygame.K_a]:
		c_pos.z -= math.cos(y_a+90)
		c_pos.x -= math.sin(y_a+90)
	if keys[pygame.K_d]:
		c_pos.z -= math.cos(y_a-90)
		c_pos.x -= math.sin(y_a-90)
	if keys[pygame.K_w]:
		c_pos.z += math.cos(y_a)
		c_pos.x += math.sin(y_a)
	if keys[pygame.K_s]:
		c_pos.z -= math.cos(y_a)
		c_pos.x -= math.sin(y_a)
	if keys[pygame.K_LSHIFT]:
		c_pos.y -= 1
	if keys[pygame.K_LCTRL]:
		c_pos.y += 1
	if keys[pygame.K_1]:
		res= 1
	if keys[pygame.K_2]:
		res = 10

	
	objects[1][1].xyz = c_pos.xyz
	pygame.display.update()
