# Imports
import base64
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO


def plot2d(numFrames, frame, joint, leftRoll, leftPitch, leftYaw, rightRoll, rightPitch, rightYaw):
    # Preload common parameters
    time_frames = np.arange(numFrames)
    y_ticks = np.linspace(start=0, stop=180, num=10)

    # Use non-interactive backend for faster rendering
    plt.switch_backend('agg')

    # Add plots and titles
    fig, axs = plt.subplots(2)
    fig.suptitle('2D ' + joint + ' Angle Graph')
    fig.subplots_adjust(bottom=0.1, wspace=0.4, hspace=0.6)
    
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
        ax.set_yticks(y_ticks)
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
    # Preload common parameters
    time_frames = np.arange(numFrames)
    y_ticks = np.linspace(start=0, stop=180, num=10)

    # Use non-interactive backend for faster rendering
    plt.switch_backend('agg')

    # Use non-interactive backend for faster rendering
    plt.switch_backend('agg')

    # Add plots and titles
    fig, axs = plt.subplots(2)
    fig.suptitle('3D ' + joint + ' Angle Graph')
    fig.subplots_adjust(bottom=0.1, wspace=0.4, hspace=0.6)
    
    # Plot
    axs[0].plot(time_frames, left3d)
    axs[0].set_title('Left ' + joint)

    axs[1].plot(time_frames, right3d)
    axs[1].set_title('Right ' + joint)

    # Add line and labels
    for ax in axs:
        ax.axvline(x=frame, color='r', linestyle='--')
        ax.set(xlabel='Time (Seconds)', ylabel='Angle (Degrees)')
        ax.set(ylim=[0, 180])
        ax.set_yticks(y_ticks)
        ax.grid()

    # Convert plot to image
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight", dpi=150)  # Reduced dpi for speed
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.close(fig)

    return data