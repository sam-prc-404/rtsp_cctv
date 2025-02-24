import cv2


# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# Replace with your RTSP URL
rtsp_url = "rtsp://admin:123456@192.168.1.66:554/mpeg4"
cv2.namedWindow("RTSP Stream", cv2.WINDOW_NORMAL)  # Make it resizable
cv2.resizeWindow("RTSP Stream", 640, 360)  # Set initial size


# Open the RTSP stream
cap = cv2.VideoCapture(rtsp_url)
# cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

if not cap.isOpened():
    print("Error: Couldn't open the RTSP stream.")
    exit()

while True:
    # print("hih")
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

       # Convert frame to grayscale (needed for Haar cascades)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
      # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw boxes around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("RTSP Stream", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
