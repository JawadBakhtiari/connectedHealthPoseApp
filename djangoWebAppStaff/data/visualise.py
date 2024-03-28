'''Code for creating visualisations of videos and keypoints.'''

import cv2
import base64
import mediapipe as mp
import data.const as const
import matplotlib.pyplot as plt
from io import BytesIO

mp_pose = mp.solutions.pose

def create_2D_visualisation(poses, cap):
    '''Return a list of strings (base64 encoded images) that represent video frames
    overlayed with corresponding keypoints.'''
    frames = []
    # Create a Pose model for static images
    with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=0,
        enable_segmentation=True,
        min_detection_confidence=0.5) as pose:

        for _ in poses:
            ret, frame_image = cap.read()
            if not ret:
                # video has reached the end
                break

            frame_height, frame_width, _ = frame_image.shape

            # Convert the BGR image to RGB before processing.
            results = pose.process(cv2.cvtColor(frame_image, cv2.COLOR_BGR2RGB))

            # Create a copy of the frame for overlaying keypoints
            overlay_image = frame_image.copy()

            if results.pose_landmarks:
                # Overlay each keypoint onto the image for this frame
                keypoints = [(int(lm.x * frame_width), int(lm.y * frame_height)) for lm in results.pose_landmarks.landmark]

                for kp in keypoints:
                    cv2.circle(overlay_image, kp, radius=2, color=(0, 255, 0), thickness=-1)

                # Connect the dots - draw lines between joints to form a human stick-figure shape
                for joint1, joint2 in const.KP_CONNS:
                    pt1 = keypoints[joint1]
                    pt2 = keypoints[joint2]
                    cv2.line(overlay_image, pt1, pt2, (0, 255, 0), 1)

            _, buffer = cv2.imencode('.png', overlay_image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            frames.append(img_base64)
    cv2.destroyAllWindows()
    return frames

def create_3D_visualisation(poses):
    '''Return a list of strings (base64 encoded images) that represent a 3D display of
    keypoints'''
    frames = []
    for p in poses:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        keypoints = []
        for kp in p.get("keypoints3D"):
            x, y, z = kp['x'], kp['y'], kp['z']
             
            # Swap Y and Z axes, and adjust X, Y, Z as needed
            x_new = x  # X remains the same
            y_new = z  # Y in Matplotlib is -Z in BlazePose
            z_new = -y  # Z in Matplotlib is Y in BlazePose

            ax.scatter(x_new, y_new, z_new, c='g', marker='o')
            keypoints.append((x_new, y_new, z_new))

        for joint1, joint2 in const.KP_CONNS:
            x1, y1, z1 = keypoints[joint1]
            x2, y2, z2 = keypoints[joint2]
            ax.plot([x1, x2], [y1, y2], [z1, z2], c='b')
        # Set the view angle of the plot here
        ax.view_init(elev=10, azim=-50) 

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        frames.append(img_base64)
    return frames

# WORK IN PROGRESS 3D VISUALISATION
#def create_3D_visualisation_alt(poses):
#     frames = []
#     for frame_num, session_frame in enumerate(poses):
#         keypoints3D_arrays = []
#         for kp in session_frame.get("keypoints3D"):
#             keypoints3D_arrays.append(np.array([kp.get('x', 0), kp.get('y', 0), kp.get('z', 0)]))
#         xdata = np.array([kp[0] for kp in keypoints3D_arrays])
#         ydata = np.array([kp[1] for kp in keypoints3D_arrays])
#         zdata = np.array([kp[2] for kp in keypoints3D_arrays])
#         trace = go.Scatter3d(
#             x=xdata,
#             y=ydata,
#             z=zdata,
#             mode='markers',
#             marker=dict(size=2, color='red')
#         )
#         lines = [
#             go.Scatter3d(
#                 x=[xdata[joint1], xdata[joint2]],
#                 y=[ydata[joint1], ydata[joint2]],
#                 z=[zdata[joint1], zdata[joint2]],
#                 mode='lines',
#                 line=dict(width=2, color='blue')
#             )
#             for joint1, joint2 in const.KP_CONNS
#         ]
#         frames.append(go.Frame(data=[trace] + lines, name=str(frame_num)))
#     layout = go.Layout(
#         scene=dict(
#             aspectmode="data",
#             aspectratio=dict(x=2, y=2, z=1),
#             xaxis=dict(range=[-2, 2], visible=False),
#             yaxis=dict(range=[-2, 2], visible=False),
#             zaxis=dict(range=[-2, 2]),
#         ),
#         showlegend=False,
#         height=800,
#         margin=dict(l=0, r=0, b=0, t=0),
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         updatemenus=[
#             dict(
#                 type="buttons",
#                 showactive=False,
#                 buttons=[dict(label="Play",
#                             method="animate",
#                             args=[None, {"frame": {"duration": 100, "redraw": True}}])])  # Adjust duration for speed
#         ]
#     )
#     fig = go.Figure(
#         data=[trace] + lines,
#         layout=layout,
#         frames=frames
#     )
#     
#     return frames
