import sys
import re
import numpy as np
import random

MARGIN = 20

def parse_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # Split by commas, remove empty entries, and strip spaces
    entries = re.split(r',(?![^()]*\))', content)
    entries = [entry.strip() for entry in entries if entry.strip()]

    result = []
    for entry in entries:
        parts = entry.split()
        if len(parts) >= 5:
            x = int(parts[0].replace("px", ""))   # Xpx
            y = int(parts[1].replace("px", ""))   # Ypx
            color = parts[4]  # Color
            result.append([x, y, color])

    return result

def create_random_map(count, size, maxX, maxY):
    count = int(count)
    size = int(size)

    mapped = mapped = np.zeros((size,size))

    positions = []

    completed = 0
    while completed < count:
        radX = int(random.random() * (size - maxX))
        radY = int(random.random() * (size - maxY))
        xLimitSub = radX-maxX-MARGIN if radX-maxX-MARGIN >= 0 else 0
        xLimitUp = radX+2*maxX+MARGIN if radX+2*maxX+MARGIN <= size else size
        yLimitSub = radY-maxY-MARGIN if radY-maxY-MARGIN >= 0 else 0
        yLimitUp = radY+2*maxY+MARGIN if radY+2*maxY+MARGIN <= size else size
        ##print(f"{xLimitSub} {xLimitUp} {yLimitSub} {yLimitUp}")
        canvas = mapped [xLimitSub:xLimitUp+1, yLimitSub:yLimitUp+1]
        flattenedMap = [item for sublist in canvas for item in sublist]
        ##print (flattenedMap)
        if max(flattenedMap) == 0:
            mapped [xLimitSub:xLimitUp+1, yLimitSub:yLimitUp+1] = 1
            positions.append((radX, radY))
            completed += 1

    print(positions)
    return positions

def print_bitmap_to_file(randomMap, parsedData, size):
    size = int(size)
    with open("output.txt", 'w', encoding='utf-8') as f:
        for item in randomMap:
            for pixel in parsedData:
                f.write(f"{pixel[0]+item[0]}px {pixel[1]+item[1]}px {pixel[2]},")
        for item in randomMap:
            for pixel in parsedData:
                f.write(f"{pixel[0]+item[0]}px {pixel[1]+item[1]+size}px {pixel[2]},")
        f.write(f";")



if __name__ == "__main__":
    filename = sys.argv[3]  # Change if needed
    parsed_data = parse_file(filename)

    # Print the resulting array
    for row in parsed_data:
        print(row)

    print(f"Stats:")
    flattenedX = [int(line[0]) for line in parsed_data]
    flattenedY = [int(line[1]) for line in parsed_data]
    ##flattened = list(map(int, flattened))
    print(f"max x: {max(flattenedX)}")
    print(f"max y: {max(flattenedY)}")

    randomMap = create_random_map(sys.argv[1], sys.argv[2], max(flattenedX), max(flattenedY))

    print_bitmap_to_file(randomMap, parsed_data, sys.argv[2])