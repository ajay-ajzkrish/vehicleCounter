import cv2
import numpy as np
import streamlit as st
st.title("Vehicle Counter")
st.markdown("Please choose a footage")
st.warning("Consider that the program is calibrated based solely on the initial footage; the others serve as illustrations.")
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    count_line_position = 530
    min_width_rect = 80
    min_height_rect = 80

    algo = cv2.bgsegm.createBackgroundSubtractorMOG()

    def center_handle(x, y, w, h):
        x1 = int(w/2)
        y1 = int(h/2)
        cx = x + x1
        cy = y + y1
        return cx, cy

    detect = []
    offset = 6
    counter = 0
    frame_placeholder = st.empty()

    while True:
        ret, frame1 = cap.read()
        if not ret:
            st.write("The video capture has ended.")
            break

        grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (3, 3), 5)
        img_sub = algo.apply(blur)
        dilat = cv2.dilate(img_sub, np.ones((3, 3)))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
        dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
        counterShape, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (255, 127, 0), 3)

        for (i, c) in enumerate(counterShape):
            (x, y, w, h) = cv2.boundingRect(c)
            validate_counter = ((w >= min_width_rect) and (h >= min_height_rect))
            if not validate_counter:
                continue
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)
            center = center_handle(x, y, w, h)
            detect.append(center)
            cv2.circle(frame1, center, 4, (0, 0, 255), -1)

            for (x, y) in detect:
                if y < (count_line_position+offset) and y > (count_line_position-offset):
                    counter += 1
                    cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (0, 127, 255), 3)
                    detect.remove((x, y))
                    print("Vehicle Counter: "+str(counter))

        cv2.putText(frame1, "Vehicle Counter : "+str(counter), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

        frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame1, channels="BGR")

    cap.release()

st.title("Vehicle Counter")
st.markdown("Select a video from the list")



col1, col2, col3, col4 = st.columns(4)

with col1:
    vdo1 = st.button('Use Footage 1')
with col2:
    vdo2 = st.button('Use Footage 2')
with col3:
    vdo3 = st.button('Use Footage 3')
with col4:
    vdo4 = st.button('Use Footage 4')

if vdo1:
    process_video('video1.mp4')
elif vdo2:
    process_video('video2.mp4')
elif vdo3:
    process_video('video3.mp4')
elif vdo4:
    process_video('video4.mp4')
