import docx2txt
import os
import cv2

ABS_PATH = os.path.dirname(os.path.realpath(__file__))
face_cascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_alt_tree.xml")


def main():
    source = os.path.join(ABS_PATH, 'docs/')

    for root, dirs, filenames in os.walk(source):
        for f in filenames:
            filename, file_extension = os.path.splitext(f)
            print(filename)
            directory = os.path.join(ABS_PATH, "images/%s" % filename)
            if not os.path.exists(directory):
                os.makedirs(directory)
            # openCv magic
            for root, dirs, filenames in os.walk(directory):
                # print(root)
                for fl in filenames:
                    pass
                    img = cv2.imread(directory+"/"+fl)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.2, 1)
                    print("faces for file ", fl , ": ", len(faces))
                    for (x,y,w,h) in faces:
                        # adding blur
                        face_color = img[y:y + h, x:x + w]
                        blur = cv2.GaussianBlur(face_color, (51, 51), 0)
                        img[y:y + h, x:x + w] = blur

                    # new directory for 
                    an_directory = "anonymized/" + os.path.basename(directory)

                    if not os.path.exists(an_directory):
                        os.makedirs(an_directory)                

                    cv2.imwrite(an_directory+"/"+fl, img)

            docx2txt.process("%s%s" % (source, f), directory)

if __name__ == "__main__":
    main()