import cv2    
# Library for threading -- which allows code to run in backend     
import threading   
import playsound  
# Library for email sending 
import smtplib     

# To access xml file which includes positive and negative images of fire. 
fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml')

# To start camera this command is used "0" for laptop inbuilt camera 
# and "1" for USB attached camera
# vid = cv2.VideoCapture(0) 

vid = cv2.VideoCapture("videos\\fire_video.mp4")

# Get the screen resolution
screen_width = 1920  # Set your screen width here
screen_height = 1080  # Set your screen height here

# Set the resolution for displaying the webcam feed
display_width = screen_width // 1
display_height = screen_height // 1

# Set the video writer for saving the output
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (display_width, display_height))

runOnce = False # created boolean

# defined function to play alarm post fire detection using threading
def play_alarm_sound_function(): 
    # to play alarm
    playsound.playsound('fire_alarm.mp3',True) 
    print("Fire alarm end") 

# Defined function to send mail post fire detection using threading
def send_mail_function(): 
    recipientmail = "rajnibnti000077@gmail.com" # recipients mail
    recipientmail = recipientmail.lower() # To lower case mail
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # Senders mail ID and password
        server.login("khuswahasarwan@gmail.com", 'sarwan@6377') 
        # recipients mail with mail message
        server.sendmail('rajnibnti000077@gmail.com', recipientmail, "Warning fire accident has been reported") 
        # to print in console to whome mail is sent
        print("Alert mail sent successfully to {}".format(recipientmail))
        server.close() ## To close server
        
    except Exception as e:
        print(e) # To print error if any

while(True):
    Alarm_Status = False
    # Value in ret is True # To read video frame
    ret, frame = vid.read() 
    
    # Resize the frame to fit the screen size
    frame = cv2.resize(frame, (display_width, display_height))
    
    # To convert frame into gray color
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    # to provide frame resolution
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) 

    ## to highlight fire with square 
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        print("Fire alarm initiated")
        # To call alarm thread
        threading.Thread(target=play_alarm_sound_function).start()  

        if runOnce == False:
            print("Mail send initiated")
            # To call alarm thread
            threading.Thread(target=send_mail_function).start() 
            runOnce = True
        if runOnce == True:
            print("Mail is already sent once")
            runOnce = True

    # Write the processed frame to the output video
    out.write(frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and video writer objects
out.release()
vid.release()
cv2.destroyAllWindows()

























