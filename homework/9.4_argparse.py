import argparse

def timetoground(h,g=9.8):
    t=(h*2/g)**0.5
    return t

def main():
    #create parser and add arguments
    parser=argparse.ArgumentParser()
    parser.add_argument("height", type=float, help="Height of object (in meters)")
    parser.add_argument("--gravity", default=9.8, type=float, help="Acceleration due to gravity (in meters/second^2)")
    
    #parse arguments
    args=parser.parse_args()
    height=args.height
    gravity=args.gravity

    #the parser will automatically catch if any arguments aren't floats, but still need to catch negatives
    if height<0: #0 is okay just gives 0 fall time
        print("Height needs to be 0 or a postive number.")
        return
    if gravity<=0: #0 will give a divide by 0 error
        print("Gravity needs to be a postive number.")
        return

    #calculate and print time
    time=timetoground(height,g=gravity)
    print(f"With g={gravity:.2f}m/s^2, time to fall to the ground from {height:.2f}m is {time:.2f}s.")

if __name__=="__main__":
    main()