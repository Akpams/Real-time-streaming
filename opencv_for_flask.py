import cv2
import requests

# Your OpenCV code to capture video frames
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Encode the frame as JPEG
    _, encoded_frame = cv2.imencode('.jpg', frame)
    
    # Send the frame to the Flask server
    url = 'http://127.0.0.1:3000/video_feed'
    files = {'frame': encoded_frame.tobytes()}
    response = requests.post(url, files=files)
    
    # Display the frame locally (optional)
    cv2.imshow('Frame', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
