

def fib(n,off,multiply):
    if off is None:
        off = 0
    if multiply is None:
        multiply = 1
    a = 0
    b = 1
    seq = []
    for i in range(n + off):
        a, b = b, a+b
        if i > off-1:
            seq.append(a)
    return [seq[x]*multiply for x in range(len(seq))]

def draw_fibonacci(seq):
    import turtle
    pointer = turtle.Turtle()
    pointer.color("white")
    wn = turtle.Screen()
    wn.bgcolor("black")

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


