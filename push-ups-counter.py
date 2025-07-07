import cv2
import mediapipe as md

md_drawing = md.solutions.drawing_utils
md_drawing_styles = md.solutions.drawing_styles
md_pose = md.solutions.pose

t = open('high_score.txt', 'r')
high_score = int(t.read())
count = 0

if count > high_score:
    t.close('high_score.txt')
    t.write(count)

postion = None

cap = cv2.VideoCapture(0)

with md_pose.Pose(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.) as pose:
    while cap.isOpened():
        success,image = cap.read()
        if not success: 
            print('no cam')
            break
        image= cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        result = pose.process(image)

        bodyparts=[]

        if result.pose_landmarks:
            md_drawing.draw_landmarks(
                image, result.pose_landmarks, md_pose.POSE_CONNECTIONS)
            for id, im  in enumerate(result.pose_landmarks.landmark):
                h,w,_=image.shape
                X,Y = int(im.x*w), int(im.y*h)
                bodyparts.append([id, X, Y])
        if len(bodyparts) != 0:  
            if(bodyparts[12][2] and bodyparts[11][2] > bodyparts[14][2] and bodyparts[13][2]):
                postion = 'down'
            if(bodyparts[12][2] and bodyparts[11][2] < bodyparts[14][2] and bodyparts[13][2] and postion =='down'):
                postion = 'up'
                count +=1
                print('Record: {}'.format(count)) 
                print('Acutual: {}'.format(count)) 

        cv2.imshow("Push up counter", cv2.flip(image, 1))
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

cap.release()