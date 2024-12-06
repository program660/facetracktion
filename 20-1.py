 #https://motchallenge.net/vis/MOT17-09-SDP/gt/


import pandas as pd
import cv2
import numpy as np


col_list = ["frame_number","identity_number","left","top","width","height","score","class","visibility"]


data = pd.read_csv("gt.txt",names=col_list)


obj = data[data["class"] == 1]


video_path = "video.mp4"


cap = cv2.VideoCapture(video_path)
id1 = 19 # teyzenin id
number_of_images = np.max(data["frame_number"])
fps = 30 # videonun çalışma hızı
bound_box = [] # liste bağlı kutu


for i in range(number_of_images-1):
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, dsize=(960,540))
        filter_id1 = np.logical_and(obj["frame_number"]==i, obj["identity_number"]==id1)
        if len(obj[filter_id1]) != 0:
            x = int(obj[filter_id1].left.values[0]/2) 
            y = int(obj[filter_id1].top.values[0]/2) 
            w = int(obj[filter_id1].width.values[0]/2)
            h = int(obj[filter_id1].height.values[0]/2)  


            cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,255), 2)
            cv2.circle(frame, (int(x+w/2),int(y+h/2)),2,(0,255,255),-1)


            bound_box.append([i,x,y,w,h,int(x+w/2),int(y+h/2)])


        cv2.putText(frame, "Frame Numarasi" + str(i), (10,30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,255,255),2)


        # Çerçeveyi görüntüle
        cv2.imshow("Frame", frame)
        
        # 'q' tuşuna basıldığında döngüyü kır
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break
    else:
        break


# Video dosyasını serbest bırak ve OpenCV pencerelerini kapat
cap.release()
cv2.destroyAllWindows()