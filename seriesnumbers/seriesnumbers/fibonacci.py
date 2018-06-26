import time


def fib(n, off, multiply):
    a = 0
    b = 1
    for i in range(n + off):
        a, b = b, a+b
        if i > off-1:
            time.sleep(0.5)
            yield a*multiply
        

def draw_fibonacci(seq, pen_color, background_color):
    import turtle
    pointer = turtle.Turtle()
    pointer.color((pen_color),(pen_color))
    wn = turtle.Screen()
    wn.bgcolor((background_color))

    for x in range(6):
        pointer.left(90)
        pointer.forward(seq[0])

    for n in range(len(seq)-1):
        pointer.speed(5)
        pointer.left(90)
        pointer.forward(seq[n+1] + seq[n])
        pointer.left(90)
        pointer.forward(seq[n+1])
        pointer.left(90)
        pointer.forward(seq[n+1] + seq[n]) 
    input()
