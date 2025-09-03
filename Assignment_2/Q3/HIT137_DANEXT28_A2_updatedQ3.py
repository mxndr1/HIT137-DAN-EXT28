'''

Group Name: DAN/EXT 28

Group Members:
FATEEN RAHMAN - s387983
HENDRICK DANG (VAN HOI DANG)- s395598
KEVIN ZHU (JIAWEI ZHU) - s387035
MEHRAAB FERDOUSE - s393148

'''

import turtle



def draw_edge(length, depth):
    """
    A recursive function that draws one edge of the geometric shape called a fractal
    using the length and recursion depth inputted by the user
    """

    # Base case: when there is no more depth left, it draws a straight line
    if depth == 0:
        turtle.forward(length)

    # Recursive case: breaks the line into four smaller segments
    else:
        # Divides the current line into 3 equal parts
        l = length / 3
        # Draws the first 1/3 segment
        draw_edge(l, depth - 1)
        # Turns left 60° to create the side of the equilateral triangle
        turtle.left(60)
        # Draws the second 1/3 segment slanting upward
        draw_edge(l, depth - 1)
        # Turns right 120° to create the other side of the equilateral triangle
        turtle.right(120)
        # Draws the third 1/3 segment slanting downward
        draw_edge(l, depth - 1)
        # Turns left 60° to straighten the direction back
        turtle.left(60)
        # Draws the last 1/3 segment to complete the edge
        draw_edge(l, depth - 1)



def draw_pattern(sides, length, depth):
    """
    Calls draw_edge() and creates the entire geometric pattern using edges
    created by the draw_edge() function
    """
    
    # Calculates the angle to turn at each corner of the pattern
    angle = 360 / sides

    # Loops through each side of the pattern
    for _ in range(sides):
        # Converts one straight edge of the base shape to a fractal edge by calling draw_edge()
        draw_edge(length, depth)
        # Turns left by the shape’s interior angle to prepare for the next side
        turtle.left(angle)
        
    # Hides the turtle after drawing is complete
    turtle.hideturtle()  
    # Finishes the drawing and displays the window
    turtle.done()  



def user_input():
    """
    Prompts the user for valid values for number of sides, length of each side and the recursion depth
    This ensures that the program does not try to create a polygon with insufficient sides or invalid lengths/depths
    """
    
    # While the user does not enter a valid integer that is greater than or equal to 3, the program will keep asking for an input for sides
    while True:
        try:
            sides = int(input("Enter the number of sides (min 3): "))
            if sides >= 3:
                break
            else:
                print("A polygon must have at least 3 sides.")
        except ValueError:
            print("Please enter a valid integer for the number of sides.")

    # While the user does not enter a valid number that is positive, the program will keep asking for an input for length
    while True:
        try:
            length = float(input("Enter the side length: "))
            if length > 0:
                break
            else:
                print("Length must be positive.")
        except ValueError:
            print("Please enter a valid length for the side.")

    # While the user does not enter a valid integer that is greater than or equal to 0, the program will keep asking for an input for depth
    while True:
        try:
            depth = int(input("Enter the recursion depth (0 or greater): "))
            if depth >= 0:
                break
            else:
                print("Depth must be 0 or greater.")
        except ValueError:
            print("Please enter a valid integer for the recursion depth.")

    # Returns the values for sides, length and depth
    return sides, length, depth



def turtle_Setup(length):
    """
    Sets up the turtle window and the parameters for drawing the fractal.
    Places the fractal roughly in the center of the screen.
    """
    
    # Sets a fixed size for the turtle window
    turtle.setup(800, 550)         
    # Sets drawing speed
    turtle.speed(0)  
    # Sets the pen size
    turtle.pensize(2)

    # Lifts the pen to move without drawing
    turtle.penup()  

    # Move turtle so the first side is centered horizontally:
    # start at the left end of the first side, facing east
    turtle.goto(-length/2, -length/2)

    # Ensure the turtle faces east before drawing
    turtle.setheading(0)

    # Put pen down to start drawing
    turtle.pendown()



def main():
    """
    The main function that prompts the user for the inputs and calls a function to draw the pattern using those inputs
    """
    
    # Calls a function that takes inputs from the user
    sides, length, depth = user_input()
    
    # Calls a function to set up the turtle window
    turtle_Setup(length)              # <— pass length so setup can center correctly

    # Calls a function to draw the pattern with the correct values 
    draw_pattern(sides, length, depth)



if __name__ == "__main__":
    main()
