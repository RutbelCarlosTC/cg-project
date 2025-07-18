import cv2
import mediapipe

from utils.dataset_utils import load_dataset, load_reference_signs
from utils.mediapipe_utils import mediapipe_detection
from sign_recorder import SignRecorder
from webcam_manager import WebcamManager


if __name__ == "__main__":
    # Create dataset of the videos where landmarks have not been extracted yet
    videos = load_dataset()

    # Create a DataFrame of reference signs (name: str, model: SignModel, distance: int)
    reference_signs = load_reference_signs(videos)

    # Object that stores mediapipe results and computes sign similarities
    sign_recorder = SignRecorder(reference_signs)

    # Object that draws keypoints & displays results
    webcam_manager = WebcamManager()

    # Turn on the webcam
    print("Attempting to open webcam...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    # Check if webcam opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam")
        print("Trying without CAP_DSHOW...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Still could not open webcam")
            exit(1)
    
    print("Webcam opened successfully!")
    print("Press 'r' to record a sign, 'q' to quit")
    
    # Set up the Mediapipe environment
    with mediapipe.solutions.holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
        while cap.isOpened():

            # Read feed
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Could not read frame from webcam")
                break

            # Make detections
            image, results = mediapipe_detection(frame, holistic)

            # Process results
            sign_detected, is_recording = sign_recorder.process_results(results)

            # Update the frame (draw landmarks & display result)
            webcam_manager.update(frame, results, sign_detected, is_recording)

            pressedKey = cv2.waitKey(1) & 0xFF
            if pressedKey == ord("r"):  # Record pressing r
                print("Recording toggled!")
                sign_recorder.record()
            elif pressedKey == ord("q"):  # Break pressing q
                print("Quitting...")
                break

        cap.release()
        cv2.destroyAllWindows()
        print("Program ended successfully")