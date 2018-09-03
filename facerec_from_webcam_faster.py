import face_recognition
import cv2,os
from datetime import datetime
import glob

video_capture = cv2.VideoCapture(0)


# from face_recognition_encoding_data import *
# Create arrays of known face encodings and their names
while True:
	known_face_encodings = []
	known_face_names = []
	#loads the dataset in the given path below
	for img in glob.glob("img_data/*.jpg"):
		image = face_recognition.load_image_file(img)
		data = face_recognition.face_encodings(image)[0]
		known_face_encodings.append(data)
		known_face_names.append(img)

	# Initialize some variables
	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True

	name = "Unknown_or_new"
	id=0
	while True:
	    # Grab a single frame of video
	    ret, frame = video_capture.read()

	    # Resize frame of video to 1/4 size for faster face recognition processing
	    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

	    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	    rgb_small_frame = small_frame[:, :, ::-1]

	    # Only process every other frame of video to save time
	    if process_this_frame:
	        # Find all the faces and face encodings in the current frame of video
	        face_locations = face_recognition.face_locations(rgb_small_frame)
	        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

	        face_names = []
	        for face_encoding in face_encodings:
	            # See if the face is a match for the known face(s)
	            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

	            # If a match was found in known_face_encodings, just use the first one.
	            if True in matches:
	                first_match_index = matches.index(True)
	                name = known_face_names[first_match_index]
	            face_names.append(name)
	    process_this_frame = not process_this_frame
	    # print name

	    # # Display the results
	    # for (top, right, bottom, left), name in zip(face_locations, face_names):
	    #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
	    #     top *= 4
	    #     right *= 4
	    #     bottom *= 4
	    #     left *= 4

	    #     # Draw a box around the face
	    #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

	    #     # Draw a label with a name below the face
	    #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
	    #     font = cv2.FONT_HERSHEY_DUPLEX
	    #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	    if name=="Unknown_or_new":
	    	ret, frame = video_capture.read()
	    	user_id="sample_"+str(id)
	    	#store the new image with the current time stamp 
	    	filename='img_data/new_'+str(datetime.now())+'.jpg'
	    	out = cv2.imwrite(filename, frame)
	    	break;
	    else:
	    	print "last recognized Time:",name
	    	#store the rename image with the current time stamp if the user is alredy exits
	    	os.rename(name, "img_data/sample_"+str(datetime.now())+".jpg") 
	    	break;
	    cv2.imshow('Video', frame)
	    # Hit 'q' on the keyboard to quit!
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
