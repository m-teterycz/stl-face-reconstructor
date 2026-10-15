
import struct
import math

# EDIT THESE SETTINGS
TRIANGLE_COUNT = 1_000
OUTPUT_FILE = f"C:/Users/user/Desktop/Project/stl-face-reconstructor/{TRIANGLE_COUNT} test.stl"
SIZE = 100.0
THICKNESS = 2.0


def generate_box(triangle_count, filename, size, thickness):
    # Six faces, with two triangles per square.
    # Use a subdivision count that gets close to the target.
    n = max(1, round(math.sqrt(triangle_count / 12)))

    triangles = []

    def add_triangle(a, b, c):
        ab = [b[i] - a[i] for i in range(3)]
        ac = [c[i] - a[i] for i in range(3)]

        normal = [
            ab[1]*ac[2] - ab[2]*ac[1],
            ab[2]*ac[0] - ab[0]*ac[2],
            ab[0]*ac[1] - ab[1]*ac[0],
        ]

        length = math.sqrt(sum(v*v for v in normal))
        normal = [v / length for v in normal]

        triangles.append((normal, a, b, c))

    def add_quad(a, b, c, d):
        for i in range(n):
            for j in range(n):
                def point(u, v):
                    return tuple(
                        a[k]*(1-u)*(1-v)
                        + b[k]*u*(1-v)
                        + c[k]*u*v
                        + d[k]*(1-u)*v
                        for k in range(3)
                    )

                p00 = point(i/n, j/n)
                p10 = point((i+1)/n, j/n)
                p11 = point((i+1)/n, (j+1)/n)
                p01 = point(i/n, (j+1)/n)

                add_triangle(p00, p10, p11)
                add_triangle(p00, p11, p01)

    s, t = size, thickness

    add_quad((0,0,0), (s,0,0), (s,s,0), (0,s,0))
    add_quad((0,0,t), (0,s,t), (s,s,t), (s,0,t))
    add_quad((0,0,0), (0,s,0), (0,s,t), (0,0,t))
    add_quad((s,0,0), (s,0,t), (s,s,t), (s,s,0))
    add_quad((0,0,0), (0,0,t), (s,0,t), (s,0,0))
    add_quad((0,s,0), (s,s,0), (s,s,t), (0,s,t))

    with open(filename, "wb") as f:
        f.write(b"Performance test box".ljust(80, b"\0"))
        f.write(struct.pack("<I", len(triangles)))

        for normal, a, b, c in triangles:
            f.write(struct.pack(
                "<12fH", *normal, *a, *b, *c, 0
            ))

    print(f"Created {filename}")
    print(f"Triangles: {len(triangles):,}")
    print(f"File size: {84 + 50*len(triangles):,} bytes")


generate_box(TRIANGLE_COUNT, OUTPUT_FILE, SIZE, THICKNESS)
