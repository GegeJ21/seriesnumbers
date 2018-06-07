import argparse
import webbrowser

def fib(n,off):
    seq = []
	a = 0
	b = 1
	for i in range(n + off):
		a, b = b, a+b
		if i > off-1:
			seq.append(a)
	return seq

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("num", help="The number of recursions", type=int)
	parser.add_argument("--offset", help="Start sequence from an offset", type=int)
	parser.add_argument("--multiply", help="Multiply the sequence", type=int) 
	parser.add_argument("--show", help="Show that juicy cabbage", action='store_true')
	args = parser.parse_args()
	if args.offset is not None:
		result = Fib(args.num, args.offset)
	else:
	    result = Fib(args.num, 0)
	if args.multiply is not None:
               for x in range(len(result)):
                      result[x] *= args.multiply

	print(result)

	if args.show is True:
		webbrowser.open('https://www.google.co.uk/search?q=fibonacci+serie&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjq3ebr063bAhVIQ8AKHdRfBZgQ_AUICigB&biw=1536&bih=758#imgrc=B0wbg6lva7jfGM:')

if __name__ =='__main__':
	main()
