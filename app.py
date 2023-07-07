from flask import Flask, request, Response, render_template
import cv2
import numpy as np

app = Flask(__name__, template_folder="templates")


# Endpoint to receive video frames
@app.route('/video_feed', methods=['GET'])
def video_feed():
    # Get the video frame from the request
    frame = request.files['frame'].read()
    nparr = np.frombuffer(frame, np.uint8)
    video_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    

    # Store the video frame in the application context
    app.video_frame = video_frame
    
    return render_template('video_feed.html')

# Endpoint to display the video
@app.route('/video_display')
def video_display():
   return render_template('video.html')

# Endpoint to stream video
@app.route('/stream')
def stream():
    def generate():
        while True:
            # Check if the video frame is available in the application context
            if hasattr(app, 'video_frame') and app.video_frame is not None:
                video_frame = app.video_frame
                resized_frame = cv2.resize(video_frame, (200, 200))

                # Encode the video frame as JPEG
                ret, jpeg = cv2.imencode('.jpg', resized_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 20])
                headers = {
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                }
                
                # Yield the encoded frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
            
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.config['COMPRESS_RESPONSE'] = True
    app.run(host='0.0.0.0', port ="8080", debug=True)
