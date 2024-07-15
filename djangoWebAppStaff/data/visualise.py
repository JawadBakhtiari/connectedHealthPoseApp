import cv2
import base64
import mediapipe as mp
import data.const as const

def create_2D_visualisation(poses: list, cap: cv2.VideoCapture) -> list:
    '''
    Return a list of frames that represent the video data for a clip overlayed with
    the pose data from that clip.

    Args:
        poses: a list representing the pose data from a clip.
        cap: the video capture for this clip.

    Returns:
        list representing pose data overlayed on video data for this clip.
    '''
    mp_pose = mp.solutions.pose
    frames = []
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
