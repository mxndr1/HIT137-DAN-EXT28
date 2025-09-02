import turtle

# Recursive function to draw one edge with indentation
def draw_edge(length, depth):
    if depth == 0:
        turtle.forward(length)
    else:
        l = length / 3
        draw_edge(l, depth - 1)
        turtle.left(60)
        draw_edge(l, depth - 1)
        turtle.right(120)
        draw_edge(l, depth - 1)
        turtle.left(60)
        draw_edge(l, depth - 1)

# Draw the whole polygon
def draw_pattern(sides, length, depth):
    angle = 360 / sides
    for _ in range(sides):
        draw_edge(length, depth)
        turtle.left(angle)

# User input
s = int(input("Enter the number of sides: "))
L = float(input("Enter the side length: "))
d = int(input("Enter the recursion depth: "))

# Setup turtle window
turtle.setup(800, 500)
turtle.speed(0)
turtle.pensize(2)

# Move starting point lower so the whole shape fits
turtle.penup()
turtle.goto(-L/2, -120)  # adjust -120 if needed for your screen/shape size
turtle.pendown()

# Draw and finish
draw_pattern(s, L, d)
turtle.hideturtle()
turtle.done()
