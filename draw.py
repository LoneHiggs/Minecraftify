import pygame
import sys
import math
screen = None
clock = None
backgroundColor = "white"
fillColor = "red"
strokeColor = "black"
angleMode = "degrees"
offset = [0, 0]
initialized = False
fps_limit = 60
show_fps = False
margin = 10

"""-------------------------Init-------------------------"""

class Point2D:
    @classmethod
    def from_list(cls, list):
        return Point2D(list[0], list[1])
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"Point2D at ({self.x}, {self.y})"
    def __iter__(self):
        return iter([self.x, self.y])
    def translate(self, x, y):
        self.x += x
        self.y += y
    def __mul__(self, other):
        if(type(other) == int or type(other) == float):
            return Point2D(self.x*other, self.y*other)
        elif type(other) == Point2D:
            pass
    def __rmul__(self, other):
        if(type(other) == int or type(other) == float):
            return Point2D(self.x*other, self.y*other)
        elif type(other) == Point2D:
            pass
    def __lt__(self, other):
        return self.x < other.x and self.y < other.y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __gt__(self, other):
        return self.x > other.x and self.y > other.y
    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y
    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y
    def __hash__(self):
        return hash(tuple(self))

class thing:
    def __init__(self, surf, rect, info = ""):
        self.surf = surf
        self.rect = rect
        self.info = info
    def __str__(self):
        return f"{self.surf}, {self.rect}: {self.info}"
    @property
    def surf(self):
        return self._surf
    @surf.setter
    def surf(self, surf):
        if type(surf) not in [pygame.surface.Surface, pygame.surface.SurfaceType]:
            raise ValueError("Must be a pygame surface (pygame.surface.Surface)")
        self._surf = surf
    @property
    def rect(self):
        return self._rect
    @rect.setter
    def rect(self, rect):
        if type(rect) not in [pygame.rect.Rect, pygame.rect.RectType]:
            raise ValueError("Must be a pygame rect (pygame.rect.Rect)")
        self._rect = rect

class UninitializedError(Exception):
    def __init__(self):
        super().__init__("Not initialized!")
    def __str__(self):
        return f"Not initialized!"

def init(width=400, height=400, color="white", title = "Unnamed canvas", center = None, margin = 10):
    if not center:
        center = [width/2, height/2]
    pygame.init()
    globals()["screen"] = pygame.display.set_mode((width+2*margin, height+2*margin))
    pygame.display.set_caption(title)
    globals()["clock"] = pygame.time.Clock()
    globals()["backgroundColor"] = color
    globals()["offset"] = (center[0]+margin, center[1]+margin)
    globals()["initialized"] = True

def fill(color):
    globals()["fillColor"] = color

def stroke(color):
    globals()["strokeColor"] = color

def translate(x, y):
    globals()["offset"][0] += x
    globals()["offset"][1] += y

def set_onclick(func):
    onclick = lambda mouseEvent: func(mouseX = pygame.mouse.get_pos()[0], 
                                      mouseY = pygame.mouse.get_pos()[1], 
                                      button = mouseEvent.button)
    globals()["onclick"] = onclick

def set_whileclick(func):
    whileclick = lambda: func(mouseX = pygame.mouse.get_pos()[0], 
                           mouseY = pygame.mouse.get_pos()[1], 
                           left = pygame.mouse.get_pressed()[0],
                           middle = pygame.mouse.get_pressed()[1],
                           right = pygame.mouse.get_pressed()[2])
    globals()["whileclick"] = whileclick

def set_keypressed(func):
    keyPressed = lambda key: func(unicode = key.unicode, key = key.key)
    globals()["keyPressed"] = keyPressed

def set_fps_limit(x):
    globals()["fps_limit"] = round(x)

"""-------------------------Util-------------------------"""

def get_rect(surf, mode, x, y):
    mode = mode.strip().replace(" ", "").lower().replace("_", "")
    rect = surf.get_rect(topleft = (x, y))
    match mode:
        case "center":
            rect = surf.get_rect(center = (x, y))
        case "midtop":
            rect = surf.get_rect(midtop = (x, y))
        case "midleft":
            rect = surf.get_rect(midleft = (x, y))
        case "midright":
            rect = surf.get_rect(midright = (x, y))
        case "midbottom":
            rect = surf.get_rect(midbottom = (x, y))
        case "topleft":
            rect = surf.get_rect(topleft = (x, y))
        case "topright":
            rect = surf.get_rect(topright = (x, y))
        case "bottomleft":
            rect = surf.get_rect(bottomleft = (x, y))
        case "bottomright":
            rect = surf.get_rect(bottomright = (x, y))
        case None:
            pass
        case _:
            raise ValueError
    return rect

def draw(thing, surf):
    if not initialized:
        raise UninitializedError
    if surf == screen:
        thing.rect.topleft = [thing.rect.topleft[0] + offset[0], thing.rect.topleft[1] + offset[1]]
        screen.blit(thing.surf, thing.rect)
        thing.rect.topleft = [thing.rect.topleft[0] - offset[0], thing.rect.topleft[1] - offset[1]]
    else:
        surf.blit(thing.surf, thing.rect)

def mouseIsPressed():
    return True in pygame.mouse.get_pressed()

def get_fps():
    if not initialized:
        raise UninitializedError
    return clock.get_fps()

"""-------------------------Make shapes-------------------------"""

"""def rect(x, y, width, height, color = fillColor, mode = "topleft", borderWidth=None,borderHeight=None,borderColor=strokeColor):
    if not borderHeight:
        borderHeight = borderWidth
    surf = pygame.surface.Surface((width, height))
    rect = get_rect(surf, mode, x, y)
    if borderWidth:
        surf.fill(borderColor)
        realsurf = pygame.surface.Surface((width-2*borderWidth,height-2*borderHeight))
        realsurf.fill(color)
        surf.blit(realsurf,(borderWidth, borderHeight))
    else:
        surf.fill(color)
    output = thing(surf, rect, f"{width}x{height} rectangle at ({x}, {y})")
    return output"""

def rect(x, y, width, height, color = fillColor, mode = "topleft", borderWidth=None, borderColor = strokeColor, radius = -1):
    surf = pygame.surface.Surface((width, height)).convert_alpha()
    surf.fill((0, 0, 0, 0))
    rect = get_rect(surf, mode, x, y)
    if borderWidth:
        pygame.draw.rect(surf, color, get_rect(surf, "topleft", 0, 0), 0, radius)
        pygame.draw.rect(surf, borderColor, get_rect(surf, "topleft", 0, 0), borderWidth, radius)
    else:
        pygame.draw.rect(surf, color, get_rect(surf, "topleft", 0, 0), 0, radius)
    output = thing(surf, rect, f"{width}x{height} rectangle at ({x}, {y})")
    return output
    

def line(x1, y1, x2, y2, color = strokeColor, width = 1, anti_alias = True):
    surf = pygame.surface.Surface((abs(x1-x2)+1, abs(y1-y2)+1)).convert_alpha()
    surf.fill((0, 0, 0, 0))
    #I cannot use the provided bounding rect from pygame.draw.line() because it glitches for positive-slope lines.
    #Check all cases for x1, y1 being topleft, topright, bottomleft, bottomright

    #Make sure x1, y1 on left
    if x2 - x1 <= 0:
        temp = (x1, y1)
        x1, y1 = (x2, y2)
        x2, y2 = temp
    #Make sure line draws at the correct local coordinates of self surface instead of the screen coordinates
    localLineStart = (0, 0)
    localLineEnd = (surf.get_width(), surf.get_height())
    if x2 - x1 >= 0 and y2 - y1 > 0:
        rect = surf.get_rect(topleft = (x1, y1))
    elif x2 - x1 >= 0 and y2 - y1 <= 0:
        rect = surf.get_rect(bottomleft = (x1, y1))
        localLineStart = (0, rect.height)
        localLineEnd = (rect.width, 0)
    if anti_alias:
        pygame.draw.aaline(surf, color, localLineStart, localLineEnd, width)
    else:
        pygame.draw.line(surf, color, localLineStart, localLineEnd, width)
    output=thing(surf, rect, f"line between ({x1}, {y1}) and ({x2}, {y2})")
    return output

def circle(x, y, radius, color = fillColor):
    return ellipse(x, y, radius, radius, color, "radius")
    
def ellipse(x, y, width, height, color = fillColor, mode = ""):
    mode = mode.strip().replace(" ", "").lower().replace("_", "")
    surf = pygame.surface.Surface((width, height)).convert_alpha()
    if mode == "radius":
        surf = pygame.surface.Surface((2*width, 2*height)).convert_alpha()
    surf.fill((0, 0, 0, 0))
    rect = get_rect(surf, "topleft", 0, 0)
    pygame.draw.ellipse(surf, color, rect)
    rect.center = (x, y) 
    msg = f"Circle at ({x}, {y}) of radius {rect.width}" if width==height else f"{rect.width}x{rect.height} ellipse at ({x}, {y})"
    output = thing(surf, rect, msg)
    return output

def polygon(vertices, color = fillColor, borderWeight = 0, borderColor = strokeColor):
    vertices = [list(vertex) for vertex in vertices]
    s1 = sorted(vertices, key=lambda x: x[0])
    s2 = sorted(vertices, key=lambda x: x[1])
    surf = pygame.surface.Surface((abs(s1[0][0]-s1[-1][0]), abs(s2[0][1]-s2[-1][1])+1)).convert_alpha()
    surf.fill((0, 0, 0, 0))
    vertices = [(vertex[0]-s1[0][0], vertex[1]-s2[0][1]) for vertex in vertices]
    if(borderWeight > 0):
        pygame.draw.polygon(surf, color, vertices)
        rect = pygame.draw.polygon(surf, borderColor, vertices, borderWeight)
    else:
        rect = pygame.draw.polygon(surf, color, vertices, borderWeight)
    rect.topleft = (s1[0][0], s2[0][1])
    return thing(surf, rect, f"polygon with vertices {vertices} and bounding box {rect.width, rect.height}")

def arc(x, y, startAngle, stopAngle, width, height, stroke = strokeColor, weight = 1, color=fillColor,fill=False,angleMode=angleMode):
    surf = pygame.surface.Surface((width, height)).convert_alpha()
    if angleMode == "degrees":
        startAngle = startAngle/180*math.pi
        stopAngle = stopAngle/180*math.pi
    surf.fill((0, 0, 0, 0))
    rect = get_rect(surf, "topleft", 0, 0)
    if(fill):
        pygame.draw.arc(surf, color, rect, startAngle, stopAngle, max(width, height))
    pygame.draw.arc(surf, stroke, rect, startAngle, stopAngle, weight)
    rect.topleft = (x-width/2, y-height/2)
    return thing(surf, rect)

def text(x, y, txt, size = 15, font = None, mode = "topLeft", antialias = False, color = strokeColor, backgroundColor = backgroundColor):
    font = pygame.font.Font(font, size)
    outputSurf = pygame.surface.Surface((len(txt)*size, len(txt)*size)).convert_alpha()
    outputSurf.fill((0, 0, 0, 0))
    lines = txt.splitlines()
    for i in range(len(lines)):
        surf = font.render(lines[i], antialias, color, backgroundColor).convert_alpha()
        outputSurf.blit(surf, (0, i*size))
    rect = get_rect(outputSurf, mode, x, y)
    return thing(outputSurf, rect)

def image(x, y, filepath, mode = "topleft", scale = 1, smoothscale = True):
    return thing(pygame.image.load(filepath), get_rect(pygame.image.load(filepath), mode, x, y))

"""-------------------------Drawing-------------------------"""

def drawrect(x, y, width, height, color = fillColor, mode = "topleft", borderWidth=None,borderHeight=None,borderColor=strokeColor):
    draw(rect(x, y, width, height, color, mode, borderWidth, borderHeight, borderColor), screen)

def drawline(x1, y1, x2, y2, color = strokeColor, anti_alias = True):
    draw(line(x1, y1, x2, y2, color, anti_alias), screen)

def drawcircle(x, y, radius, color = fillColor):
    draw(circle(x, y, radius, color), screen)

def drawellipse(x, y, width, height, color = fillColor, mode = ""):
    draw(ellipse(x, y, width, height, color, mode), screen)

def drawpoly(vertices, color = fillColor, borderWeight = 0, borderColor = strokeColor):
    draw(polygon(vertices, color, borderWeight, borderColor), screen)

def drawarc(x, y, startAngle, stopAngle, width, height, stroke = strokeColor, weight = 1, color=fillColor,fill=False,angleMode=angleMode):
    draw(arc(x, y, startAngle, stopAngle, width, height, stroke, weight, color, fill, angleMode), screen)

def drawtext(x, y, txt, size = 20, font = None, mode = "topLeft", antialias = True, color=strokeColor,backgroundColor=backgroundColor):
    draw(text(x, y, txt, size, font, mode, antialias, color, backgroundColor), screen)

"""-------------------------File-------------------------"""

def screenshot(filename):
    pygame.image.save(screen, filename)
def screenshot_obj(fileobj, format=""):
    pygame.image.save(screen, fileobj, format)

def save(width, height, things = [], *args, filename):
    if(type(things) == thing):
        things = [things]
    try:
        things = list(things)
        things = things + list(args)
    except:
        pass
    img = pygame.surface.Surface((width, height))
    for thing in things:
        img.blit(thing.surf, thing.rect)
    pygame.image.save(img, filename)

"""-------------------------Run-------------------------"""

def onclick(event):
    pass

def whileclick():
    pass

def keyPressed(event):
    pass

def run(width=400, height=400, color="white", title = "Unnamed canvas", center = None, things = [], execute = []):
    if not initialized:
        init(width, height, color, title, center)
    while True:
        screen.fill(backgroundColor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                onclick(event)
            if event.type == pygame.KEYDOWN:
                keyPressed(event)
        if mouseIsPressed():
            whileclick()
        key = pygame.key.get_pressed()
        
        for todo in execute:
            todo()
        for thing in things:
            draw(thing, screen)
        clock.tick(fps_limit)
        if show_fps:
            screen.blit(pygame.font.Font(pygame.font.get_default_font()).render(str(round(get_fps())), True, "white"), (0, 0))
        pygame.display.update()
        
        

def test():
    draw(line(0, 0, 400, 400, "black", 10, False), screen)

if __name__ == "__main__":
    run(execute = [test])