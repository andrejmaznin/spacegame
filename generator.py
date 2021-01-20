import random
import traceback


def generate_map(filename):
    try:
        with open(filename, 'w') as mapFile:
            a = [["." for i in range(50)] for j in range(50)]
            a[24][24] = "S"
            planets = []
            x1, y1 = random.randint(4, 45), random.randint(4, 45)
            while True:
                if abs(x1 - 24) >= 5 and abs(y1 - 24) >= 5:
                    a[y1][x1] = str(random.randint(0, 2))
                    planets.append([x1, y1])
                    break
                else:
                    x1, y1 = random.randint(4, 45), random.randint(4, 45)

            x1, y1 = random.randint(4, 45), random.randint(4, 45)
            for i in range(random.randint(1, 6)):
                while True:
                    counts = [abs(j[0] - x1) >= 3 and abs(j[1] - y1) >= 3 for j in planets]

                    if abs(x1 - 24) >= 4 and abs(y1 - 24) >= 4 and counts.count(True) == len(counts):
                        a[y1][x1] = str(random.randint(0, 2))
                        planets.append([x1, y1])
                        break
                    else:
                        x1, y1 = random.randint(4, 45), random.randint(4, 45)

            a[23][23] = "@"
            a[22][22] = "A"
            a = "".join(["".join(i) + "\n" for i in a])
            mapFile.write(a)
    except Exception:
        print(traceback.format_exc())


generate_map("map_0.txt")
generate_map("map_1.txt")
generate_map("map_2.txt")
generate_map("map_3.txt")
