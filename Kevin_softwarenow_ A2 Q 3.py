import turtle

def draw_edge(length, depth):
    if depth == 0:
        turtle.forward(length)
    else:
        length /= 3
        draw_edge(length, depth - 1)
        turtle.right(60)
        draw_edge(length, depth - 1)
        turtle.left(120)
        draw_edge(length, depth - 1)
        turtle.right(60)
        draw_edge(length, depth - 1)

def draw_pattern(sides, length, depth):
    angle = 360 / sides
    for _ in range(sides):
        draw_edge(length, depth)
        turtle.right(angle) 

sides = int(input("Enter number of sides: "))
length = int(input("Enter side length: "))
depth = int(input("Enter recursion depth: "))

turtle.speed(0)
turtle.penup()
turtle.goto(-length/2, length/2)
turtle.setheading(0)
turtle.pendown()

draw_pattern(sides, length, depth)

turtle.done()
