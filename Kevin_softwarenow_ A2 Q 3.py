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
        turtle.right(angle)   # 顺时针转，保证内凹方向正确

# ===== 主程序 =====
sides = int(input("Enter number of sides: "))
length = int(input("Enter side length: "))
depth = int(input("Enter recursion depth: "))

turtle.speed(0)
turtle.penup()
turtle.goto(-length/2, length/2)  # 从左上角开始
turtle.setheading(0)              # 向右
turtle.pendown()

draw_pattern(sides, length, depth)

turtle.done()