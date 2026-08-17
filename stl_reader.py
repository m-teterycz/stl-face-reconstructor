import struct

def stl_type(data):
    if 'vertex' in data:
        return 'ascii'
    return 'binary'

def read_data(path):
    with open(path, "r") as f:
        if 'vertex' in f.read():
            return format_data_ascii(path)
        else:
            return format_data_binary(path)

def format_data_ascii(path):
    print('ascii mode')
    
    f = open(path, 'r')
    data = f.read()
    words = data.split()
    
    formatted_data = []
    i = 0
        
    while i < len(words):
        if words[i].lower() == 'vertex':
            coords = words[i + 1: i + 4]
            if coords_check(coords) == False:
                return 'Invalid STL'
            formatted_data.append(coords)
        i += 1
        
    f.close()
    return formatted_data
    
def format_data_binary(path):
    f = open(path, 'rb')
    data = f.read()[80:] # Removes unecessary 80 byte header
    triangle_count = int.from_bytes(data[:4], 'little')
    data = data[4:] # removes triangle count to make processing easier later

    formatted_data = []

    if len(data) % 50 != 0:
        return "Invalid stl"

    if triangle_count != len(data) // 50:
        return "Warning: triangle count does not match file size"
    
    for i in range(triangle_count):
        triangle_offset = 50 * i
        
        for j in range(3):
            vertex_offset = 12 * j
            x, y, z = struct.unpack("<fff", (data[12 + triangle_offset + vertex_offset : 24 + triangle_offset + vertex_offset]))
            formatted_data.append([x, y, z])
            
    f.close()
    return formatted_data
    

def coords_check(coords):
    if len(coords) != 3:
        return False
    
    for coord in coords:
        try:
            float(coord)
        except:
            return False
    return True
      
        
