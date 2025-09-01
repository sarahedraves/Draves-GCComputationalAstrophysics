if __name__=="__main__":

    import argparse

    parser=argparse.ArgumentParser()
    parser.add_argument("height", type=float, help="Height of object")
    
    args=parser.parse_args()
    print(args)
    height=args.height
    
    def timetoground(h,g=9.8):
        t=(h*2/g)**0.5
        return t
    
    print(timetoground(height))