# Imports
import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    # Plotter class
    def __init__(self, numFrames, joint, interval, leftRoll, leftPitch, leftYaw, rightRoll, rightPitch, rightYaw, left3d, right3d) -> None:
        self.numFrames = numFrames
        self.numIntervals = int(360 / int(interval)) + 1
        self.joint = joint.lower().capitalize()
        self.leftRoll = leftRoll
        self.leftPitch = leftPitch
        self.leftYaw = leftYaw
        self.rightRoll = rightRoll
        self.rightPitch = rightPitch
        self.rightYaw = rightYaw
        self.left3d = left3d
        self.right3d = right3d
        self.plotted = False

        if int(interval) > 360:
            self.numIntervals = 13


    # Plot 2d values
    def plot2d(self, frame_number):
        fig, axs = plt.subplots(2)

        fig.suptitle('2D ' + self.joint + ' Angle Visualisation & Graph')
        fig.tight_layout()
        
        axs[0].plot(range(self.numFrames), self.leftRoll, label = 'Roll')
        axs[0].plot(range(self.numFrames), self.leftPitch, label = 'Pitch')
        axs[0].plot(range(self.numFrames), self.leftYaw, label = 'Yaw')
        axs[0].set_title('Left ' + self.joint)

        axs[1].plot(range(self.numFrames), self.rightRoll, label = 'Roll')
        axs[1].plot(range(self.numFrames), self.rightPitch, label = 'Pitch')
        axs[1].plot(range(self.numFrames), self.rightYaw, label = 'Yaw')
        axs[1].set_title('Right ' + self.joint)

        for ax in axs:
            ax.axvline(x=frame_number, color='r', linestyle='--')

        for ax in axs.flat:
            ax.set(xlabel='Frames', ylabel='Angle(Degrees)')
            ax.set(ylim=[-180, 180])
            ax.grid()
            ax.set_xticks(list(range(self.numFrames)), [str(i) for i in range(self.numFrames)])
            ax.set_yticks(list(np.linspace(start=-180, stop=180, num=self.numIntervals)))
            ax.legend()

        self.plotted = True


    # Plot 3d values
    def plot3d(self, frame_number):
        fig, axs = plt.subplots(2)
        fig.subplots_adjust(bottom=0.1, wspace=0.4, hspace=0.4)

        fig.suptitle('3D ' + self.joint + ' Angle Visualisation & Graph')
        axs[0].plot(range(self.numFrames), self.left3d)
        axs[0].set_title('Left ' + self.joint)

        axs[1].plot(range(self.numFrames), self.right3d)
        axs[1].set_title('Right ' + self.joint)

        for ax in axs:
            ax.axvline(x=frame_number, color='r', linestyle='--')

        for ax in axs.flat:
            ax.set(xlabel='Frames', ylabel='Angle(Degrees)')
            ax.set(ylim=[0, 180])
            ax.grid()
            ax.set_xticks(list(range(self.numFrames)), [str(i) for i in range(self.numFrames)])
            ax.set_yticks(list(np.linspace(start=0, stop=180, num=self.numIntervals)))

        self.plotted = True


    # Save plot
    def save(self, dimension, filename):
        if not self.plotted:
            print('Usage Error: Plot must be plotted first - Plotter.plot2d or Plotter.plot3d')
            exit(1)

        if dimension == '2d':
            plt.savefig(filename + '-2d.png')
            self.show("frames_angle_visulisation-2d.png")
        elif dimension == '3d':
            plt.savefig(filename + '-3d.png')
            self.show("frames_angle_visulisation-2d.png")
        else:
            print('Usage Error: Dimension must be "2d" or "3d"')
            exit(1)


    # Show plot
    def show(self, file_path):
        if not self.plotted:
            print('Usage Error: Plot must be plotted first - Plotter.plot2d or Plotter.plot3d')
            exit(1)
        plt.savefig(file_path)
