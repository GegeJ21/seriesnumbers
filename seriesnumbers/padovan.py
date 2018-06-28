import time


def pad(n, off, multiply):
    """
    generator that returns n numbers of the padovan series

    :param n: number of recursions
    :type n: int

    :param offset: offset from the beginnig of the series
    :type offset: int

    :param multiply: multiply the whole series for the value
    :type multiply: int

    :return: series numbers
    :rtype: int
    """

    if multiply is None:
        multiply = 1
    seq = []
    for x in range(n + off ):
        if x == 0 or x == 1 or x == 2:
            seq.append(1)
            if x > off - 1:
                time.sleep(1)
                yield seq[x]*multiply
        else:
            seq.append(seq[x-2] + seq[x-3])
            if x > off - 1:
                time.sleep(1)
                yield seq[x]*multiply

def drawPadovan(seq, pen_color, background_color):
    """
    displays the series with TurtleGraphics

    :param seq: the series of numbers to rapresent
    :type seq: list[int]

    :param pen_color, background_color: the colors expressed in hex selected with the picker
    :type pen_color, bakground_color: str
    """
    import turtle
    pointer = turtle.Turtle()
    pointer.color(pen_color)
    wn = turtle.Screen()
    wn.bgcolor(background_color)
    pointer.left(90)
    step = 0

    for x in range(len(seq)):
        # the series is drawn in five steps that than repeat
        if step == 0:
            pointer.left(150)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x]) 
            step +=1

        elif step == 1:
            pointer.left(60)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            step += 1

        elif step == 2:
            pointer.left(60)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            step +=1

        elif step == 3:
            pointer.right(120)
            pointer.forward(seq[x])
            pointer.right(120)
            pointer.forward(seq[x])
            step += 1

        elif step == 4:
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            step += 1

        elif step == 5:
            pointer.right(120)
            pointer.forward(seq[x])
            pointer.right(120)
            pointer.forward(seq[x])
            pointer.right(180)
            pointer.forward(seq[x])
            pointer.left(30)
            step = 0


    input()