import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.interpolate import CubicSpline

def getcolors(scenario,displaychoice):
    if scenario=='threestars':
        if displaychoice=='plot':
            return ["deeppink","green","blue"]
        elif 'animate' in displaychoice:
            return [["lightpink", "deeppink"],["lightgreen", "green"],["lightblue", "blue"]]
    elif scenario=='threestarsandplanet':
        if displaychoice=='plot':
            return ["deeppink","green","blue","black"]
        elif 'animate' in displaychoice:
            return [["lightpink", "deeppink"],["lightgreen", "green"],["lightblue", "blue"],["gray","black"]]
    elif scenario=='twostars':
        if displaychoice=='plot':
            return ["deeppink","green"]
        elif 'animate' in displaychoice:
            return [["lightpink", "deeppink"],["lightgreen", "green"]]
    elif scenario=='twostarsandplanet':
        if displaychoice=='plot':
            return ["deeppink","green","black"]
        elif 'animate' in displaychoice:
            return [["lightpink", "deeppink"],["lightgreen", "green"],["gray","black"]]
    elif scenario=='oneorbit':
        if displaychoice=='plot':
            return ["black"]
        elif 'animate' in displaychoice:
            return [["gray","black"]]

def animate(Ts,Rs,colors,trailing=True,filename=None):
    #colors needs to be something like colors = [["lightpink", "deeppink"],["lightgreen", "green"],["lightblue", "blue"]]
    
    numobjects=Rs.shape[1]//4 #because four fields per object and want it to be an int

    #create lists of arrays for coordinates
    Xs=[]
    Ys=[]
    for i in range(numobjects):
        Xs.append(Rs[:,4*i])
        Ys.append(Rs[:,4*i+1])
        
    fig,ax=plt.subplots()
    
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_title(f'Evolution of the {numobjects} Objects')
    
    #set the limits of the plot to be the range of the points with a buffer zone
    allX=np.concatenate(Xs)
    allY=np.concatenate(Ys)
    Xmax=allX.max()
    Xmin=allX.min()
    Ymax=allY.max()
    Ymin=allY.min()
    width=Xmax-Xmin
    height=Ymax-Ymin
    ax.set_xlim(Xmin-0.1*width,Xmax+0.1*width)
    ax.set_ylim(Ymin-0.1*height,Ymax+0.1*height)
    
    # want 1000 frames for the gif
    step = round(len(Ts)/1000)
    frame_indices = range(0, len(Ts), step)
    line_step=step//10 

    if trailing==True:
        trail_length=step*50
    
    #initialize empty line and scatter plots
    lines = []
    scatters = []
    for i in range(numobjects):
        line_color = colors[i][0]
        scatter_color = colors[i][1]
        line, = ax.plot([], [], color=line_color, zorder=2)
        scatter = ax.scatter([], [], color=scatter_color, zorder=3)
        lines.append(line)
        scatters.append(scatter)
    
    def animate(frame):
        index=frame*step

        for i in range(numobjects):
            Xi=Xs[i]
            Yi=Ys[i]
    
            if trailing==False:
                lines[i].set_data(Xi[:index+1:line_step],Yi[:index+1:line_step])
            elif trailing==True:
                startindex=index-trail_length
                if startindex<0:
                    startindex=0
                lines[i].set_data(Xi[startindex:index+1:line_step],Yi[startindex:index+1:line_step])
            
            scatters[i].set_offsets([[Xi[index], Yi[index]]])
        
        return lines+scatters
    
    anim=animation.FuncAnimation(fig,animate,frames=len(frame_indices),
                                 interval=50,repeat=True,blit=True)
    if filename is not None:
        anim.save(f'{filename}.gif',writer='pillow',fps=20)
    return anim

def plotnohs(Ts,Rs,colors,filename=None):
    #colors should be something like colors=["deeppink","green","blue"]

    numobjects=Rs.shape[1]//4 #because four fields per object and want it to be an int

    #create lists of arrays for coordinates
    Xs=[]
    Ys=[]
    for i in range(numobjects):
        Xs.append(Rs[:,4*i])
        Ys.append(Rs[:,4*i+1])

    fig,ax=plt.subplots()

    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_title(f'Paths of the {numobjects} Objects')

    #set the limits of the plot to be the range of the points with a buffer zone
    allX=np.concatenate(Xs)
    allY=np.concatenate(Ys)
    Xmax=allX.max()
    Xmin=allX.min()
    Ymax=allY.max()
    Ymin=allY.min()
    width=Xmax-Xmin
    height=Ymax-Ymin
    ax.set_xlim(Xmin-0.1*width,Xmax+0.1*width)
    ax.set_ylim(Ymin-0.1*height,Ymax+0.1*height)

    line_step=1
    if len(Ts)>10000:
        line_step=len(Ts)//10000 #only do this many points
        
    for i in range(numobjects):
        line_color = colors[i]
        ax.plot(Xs[i][::line_step], Ys[i][::line_step], color=line_color)

    if filename is not None:
        fig.savefig(f'{filename}.png')
    return fig

def ploths(Ts,Rs,Hs,colors,filename=None):
    #colors should be something like colors=["deeppink","green","blue"]

    numobjects=Rs.shape[1]//4 #because four fields per object and want it to be an int

    #create lists of arrays for coordinates
    Xs=[]
    Ys=[]
    for i in range(numobjects):
        Xs.append(Rs[:,4*i])
        Ys.append(Rs[:,4*i+1])

    fig,axs=plt.subplots(1,2,figsize=(10,4))

    axs[0].set_xlabel('X coordinate')
    axs[0].set_ylabel('Y coordinate')
    axs[0].set_title(f'Paths of the {numobjects} Objects')

    #set the limits of the plot to be the range of the points with a buffer zone
    allX=np.concatenate(Xs)
    allY=np.concatenate(Ys)
    Xmax=allX.max()
    Xmin=allX.min()
    Ymax=allY.max()
    Ymin=allY.min()
    width=Xmax-Xmin
    height=Ymax-Ymin
    axs[0].set_xlim(Xmin-0.1*width,Xmax+0.1*width)
    axs[0].set_ylim(Ymin-0.1*height,Ymax+0.1*height)

    line_step=1
    if len(Ts)>10000:
        line_step=len(Ts)//10000 #only do this many points

    for i in range(numobjects):
        line_color = colors[i]
        axs[0].plot(Xs[i][::line_step], Ys[i][::line_step], color=line_color)

    axs[1].plot(Ts,np.log10(Hs),color='black')
    axs[1].set_xlabel('t')
    axs[1].set_ylabel('log10(h)')
    axs[1].set_title('Step-Size vs Time')

    plt.tight_layout()
    
    if filename is not None:
        fig.savefig(f'{filename}.png')
    return fig

def plot(Ts,Rs,Hs,plotHs,colors,filename=None):
    if Hs is not None and plotHs==True:
        return ploths(Ts,Rs,Hs,colors,filename=filename)
    else:
        return plotnohs(Ts,Rs,colors,filename=filename)


def resample(Ts,Rs,N=10000): #modified from ChatGPT after I asked it how to do time-uniform resampling of my Ts and Rs arrays
    Ts_uniform = np.linspace(Ts[0], Ts[-1], N)
    Rs_uniform = np.empty((N, Rs.shape[1]))

    for i in range(Rs.shape[1]):
        cs = CubicSpline(Ts, Rs[:, i])
        Rs_uniform[:, i] = cs(Ts_uniform)

    return Ts_uniform, Rs_uniform