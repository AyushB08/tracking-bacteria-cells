from PIL import Image
import sys

sys.setrecursionlimit(80000)

frames = 40

""" 
with Image.open('../assets/bacteria.gif") as image:
    for i in range(frames):
        image.seek(image.n_frames // frames * i)
        image.save('{}.png'.format(i))

"""

pink = (255, 127, 127)
gray = (127, 127, 127)
red = (127, 0, 0)
black = (0, 0, 0)


def get_num_bacteria(image_path):
    height = 240
    width = 320

    pixels = []

    # Obtain Image

    for i in range(1):
        # image = Image.open("bacteria/" + str(i) + ".png", "r")
        image = Image.open("" + image_path)
        pixels = list(image.getdata())

    # Transform 1D Array into 2D Array

    rgb_values = []

    for i in range(height):
        rgb_values.append([])
        for a in range(width):
            array = pixels[i * width + a]

            rgb_values[i].append((array[0], array[1], array[2]))

    # Turn all pixels that are not gray, pink, and red to gray
    # Turn all pink pixels to red

    for i in range(height):
        for a in range(width):
            if rgb_values[i][a] == pink:
                rgb_values[i][a] = red

            if rgb_values[i][a] != red and rgb_values[i][a] != pink and rgb_values[i][a] != gray:
                rgb_values[i][a] = gray

    # Fill in holes

    for row in range(height):
        for col in range(width):
            if 5 < row < 235 and 5 < col < 315:

                if rgb_values[row][col] == gray:

                    if rgb_values[row][col - 1] == rgb_values[row][col + 1] == gray:

                        if rgb_values[row - 1][col] != gray and rgb_values[row + 1][col] != gray:
                            rgb_values[row][col] = red

                    if rgb_values[row - 1][col] == rgb_values[row + 1][col] == gray:

                        if rgb_values[row][col - 1] != gray and rgb_values[row][col + 1] != gray:
                            rgb_values[row][col] = red

                if rgb_values[row][col] != gray:

                    # 2 left, 1 down
                    if rgb_values[row][col - 1] == gray and rgb_values[row + 1][col - 1] == gray and \
                            rgb_values[row + 1][col - 2] != gray:
                        rgb_values[row][col - 1] = red

                    # 1 left, 2 down
                    if rgb_values[row + 1][col] == gray and rgb_values[row + 1][col - 1] == gray and \
                            rgb_values[row + 2][
                                col - 1] != gray:
                        rgb_values[row + 1][col] = red

    # Set New Image

    image = Image.new("RGB", (width, height))

    def process_island(visited_squares, row, col, depth_limit=80000, current_depth=0):
        if row < 0 or row >= height or col < 0 or col >= width or [row, col] in visited_squares:
            return

        if rgb_values[row][col] != gray:
            return

        if current_depth >= depth_limit:
            return 0

        rgb_values[row][col] = black

        process_island(rgb_values, row - 1, col, depth_limit, current_depth + 1)  # Up
        process_island(rgb_values, row + 1, col, depth_limit, current_depth + 1)  # Down
        process_island(rgb_values, row, col - 1, depth_limit, current_depth + 1)  # Left
        process_island(rgb_values, row, col + 1, depth_limit, current_depth + 1)  # Right

    visited_squares = []
    process_island(visited_squares, 0, 0)

    for y in range(height):
        for x in range(width):
            image.putpixel((x, y), rgb_values[y][x])

    """
    start_index = image_path.find("a/") + 2
    end_index = image_path.find(".", start_index)
    image.save("output_bacteria_" + image_path[start_index:end_index] + ".png")
    """

    def count_bacteria(visited_pixels, row, col, count):
        if [row, col] not in visited_pixels and rgb_values[row][col] == gray:
            visited_pixels.append([row, col])
            count = 1
            count += count_bacteria(visited_pixels, row + 1, col, count)
            count += count_bacteria(visited_pixels, row - 1, col, count)
            count += count_bacteria(visited_pixels, row, col + 1, count)
            count += count_bacteria(visited_pixels, row, col - 1, count)
            return count

        return 0

    visited_pixels = []

    bacteria_count = []
    for row in range(height):
        for col in range(width):
            if rgb_values[row][col] == gray and 0 < row < height - 1 and 0 < col < width - 1 and [row,
                                                                                                  col] not in visited_pixels:
                num = count_bacteria(visited_pixels, row, col, 0)
                bacteria_count.append(num)

    bacteria = 0
    for i in range(len(bacteria_count)):
        if bacteria_count[i] > 50:
            bacteria += 1

    return bacteria


def iterate_through_frames():
    with open('../solution/solution.txt', 'w') as file:
        for i in range(39):
            count = get_num_bacteria("../bacteria/" + str(i) + ".png")
            file.write(str(count) + "\n")


iterate_through_frames()
#get_num_bacteria("../bacteria/" + str(17 + 1) + ".png")
