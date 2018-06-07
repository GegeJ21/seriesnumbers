import webbrowser
import argparse


fibonacci_URL = "https://en.wikipedia.org/wiki/Fibonacci_number"
padovan_URL = "https://en.wikipedia.org/wiki/Padovan_sequence"

def do_pad(args):
    pass

def main():
    import sys
    print sys.path
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(help='sub-options help')

    
    #arguments for the Fibonacci series
    
    parser_fib = subparser.add_parser("fib", help="Fibonacci series")
    parser_fib.set_defaults(seriestype="fib")
    parser_fib.add_argument("num", help="Number of recursions", type=int)
    parser_fib.add_argument("-of", "--offset", help="Start sequence from an offset", type=int)
    parser_fib.add_argument("--multiply", help="Multiply the sequence", type=int) 
    parser_fib.add_argument("--wiki", help="Link to Wikipedia page", action='store_true')
    parser_fib.add_argument("--draw", help="Draw sequence shell", action="store_true")
    parser_fib.add_argument("--output", help="Writes result on a txt file", type=str)

    #arguments for the Pell series

    parser_pad = subparser.add_parser("pad", help="Padovan series")
    parser_pad.set_defaults(seriestype="pad")
    parser_pad.set_defaults(func=do_pad)
    parser_pad.add_argument("num", help="Number of recursions", type=int)
    parser_pad.add_argument("--multiply", help="Multiply the sequence", type=int)
    parser_pad.add_argument("--wiki", help="Link to Wikipedia page", action='store_true')
    parser_pad.add_argument("--draw", help="Draw sequence triangles", action="store_true")
    parser_pad.add_argument("--output", help="Writes result on a txt file", type=str)

    args = parser.parse_args()
    args.func(args)
    if args.seriestype == "fib":
        import fibonacci
        result = fibonacci.fib(args.num,args.offset,args.multiply)
        print result
        if args.draw == True:
            fibonacci.draw_fibonacci(result)
        if args.wiki == True:
            webbrowser.open(fibonacci_URL)
        if args.output is not None:
            import output
            output.write_txt(result,args.output)
    elif args.seriestype =="pad":
        import seriesnumbers.padovan
        result = seriesnumbers.padovan.pad(args.num,args.multiply)
        print result
        if args.draw == True:
            padovan.draw_padovan(result)
        if args.wiki == True:
            webbrowser.open(padovan_URL)
        if args.output is not None:
            import output
            output.write_txt(result,args.output)




if __name__ =='__main__':
    main()