from PIL import Image, ImageDraw, ImageChops
import random
import colorsys
import config


def random_color():
    h = random.random()
    s = 1
    v = 1

    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    rgb = [int(x * 255) for x in float_rgb]
    return tuple(rgb)


def interpolate(start_color, end_color, factor: float):
    recip = 1 - factor
    return(
        int(start_color[0] * recip + end_color[0] * factor),
        int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor)
    )

def generate_art(path: str):
    target_size = config.image_size
    scale_factor = 2
    img_size = target_size * scale_factor
    paddign_px = config.image_padding * scale_factor
    img_bg_color = (13, 16, 36)
    start_color = random_color()
    end_color = random_color()
    image = Image.new(
        "RGB",
        size=(img_size, img_size),
        color=(1, 1, 3)
    )

    draw = ImageDraw.Draw(image)

    points = []
    for _ in range(10):
        random_point = (
            random.randint(paddign_px, img_size), 
            random.randint(paddign_px, img_size)
        )
        points.append(random_point)

    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    delta_x = min_x - (img_size -  max_x)
    delta_y = min_y - (img_size - max_y)

    for i, point in enumerate(points):
        points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)
    
    thickness = 0
    n_points = len(points) - 1
    for i, point in enumerate(points):
        overlay_image = Image.new(
            "RGB",
            size=(img_size, img_size),
            color=(1, 1, 3)
        )
        overlay_draw = ImageDraw.Draw(overlay_image)

        p1 = point
        
        if i == n_points:
            p2 = points[0]
        else:
            p2 = points[i + 1]

        line_xy = (p1, p2) 
        color_factor = i / n_points
        line_color = interpolate(start_color, end_color, color_factor)
        thickness += scale_factor
        overlay_draw.line(line_xy, fill=line_color, width=thickness)
        image = ImageChops.add(image, overlay_image)
    image = image.resize((target_size, target_size), resample=Image.ANTIALIAS)
    image.save(path)

if __name__ == "__main__":
    for i in range(config.number_images):
        generate_art(f"image_{i}.png")