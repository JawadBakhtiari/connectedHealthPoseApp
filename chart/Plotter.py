# Imports
import base64
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO



def plot2d(numFrames, frame, joint, leftRoll, leftPitch, leftYaw, rightRoll, rightPitch, rightYaw):
    # Preload common parameters
    time_frames = np.arange(numFrames)
    yticks = np.linspace(start=0, stop=180, num=10)

    # Use non-interactive backend for faster rendering
    plt.switch_backend('agg')

    # Add plots and titles
    fig, axs = plt.subplots(2)
    fig.suptitle('2D ' + joint + ' Angle Graph')
    
    # Plot data with bitmaps
    axs[0].plot(time_frames, leftRoll, label='Roll', rasterized=True)
    axs[0].plot(time_frames, leftPitch, label='Pitch', rasterized=True)
    axs[0].plot(time_frames, leftYaw, label='Yaw', rasterized=True)
    axs[0].set_title('Left ' + joint)

    axs[1].plot(time_frames, rightRoll, label='Roll', rasterized=True)
    axs[1].plot(time_frames, rightPitch, label='Pitch', rasterized=True)
    axs[1].plot(time_frames, rightYaw, label='Yaw', rasterized=True)
    axs[1].set_title('Right ' + joint)

    # Add line and labels
    for ax in axs:
        ax.axvline(x=frame, color='r', linestyle='--')
        ax.set(xlabel='Time (Seconds)', ylabel='Angle (Degrees)')
        ax.set(ylim=[0, 180])
        ax.set_yticks(yticks)
        ax.grid()

    # Add legend
    axs[0].legend()

    # Convert plot to image
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight", dpi=150)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.close(fig)

    return data


def plot3d(numFrames, frame, joint, left3d, right3d):
    x_range = np.arange(numFrames)
    yticks = np.linspace(start=0, stop=180, num=10)
    # Optimization: Use the 'agg' backend for faster rendering
    plt.switch_backend('agg')

    fig, axs = plt.subplots(2)

    fig.suptitle('3D ' + joint + ' Angle Graph')
    
    # Optimization: Plot with precomputed x_range
    axs[0].plot(x_range, left3d)
    axs[0].set_title('Left ' + joint)

    axs[1].plot(x_range, right3d)
    axs[1].set_title('Right ' + joint)

    # Optimization: Vectorize the repetitive axvline setting
    for ax in axs:
        ax.axvline(x=frame, color='r', linestyle='--')
        ax.set(xlabel='Time (Seconds)', ylabel='Angle (Degrees)')
        ax.set(ylim=[0, 180])
        ax.set_yticks(yticks)
        ax.grid()

    # Optimization: Use a BytesIO buffer and reduce the dpi if high resolution is not required
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight", dpi=100)  # Reduced dpi for speed
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    # Optimization: Explicitly close the plt to free up memory
    plt.close(fig)

    return data