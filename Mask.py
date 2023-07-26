import cv2
import numpy as np
import mediapipe as mp
import matplotlib as plt

landmarks = []
countr = []
face = []

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness = 1, circle_radius = 1)
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=False,
    ) as face_mesh:
        image = cv2.imread('photos/Closedeyes.png')

        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        landmarks.append(results.multi_face_landmarks)
        face.append(mp_face_mesh.FACEMESH_TESSELATION)
        countr.append(mp_face_mesh.FACEMESH_CONTOURS)


        annotated_image = image.copy()
        for face_landmarks in results.multi_face_landmarks:

            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())

            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())

        cv2.imwrite('annotated_image.png', annotated_image)

with open('Face.txt', 'w') as WriteFace:
    for i in range(len(face)):
        WriteFace.write(str(face[i]) + '\n')

with open('Countr.txt', 'w') as WriteCountr:
    for i in range(len(countr)):
        WriteCountr.write(str(countr[i]) + '\n')

with open('Marks.txt', 'w') as WriteTest:
    for i in range(len(landmarks)):
        WriteTest.write(str(landmarks[i]) + '\n')

readFace = open('Face.txt')
allface = []

for line in readFace:
    line = line[11:-3]
    line = line.split(', ')
    for i in range(0, len(line), 2):
        into = []
        into.append(int(line[i][1:len(line[i])]))
        into.append(int(line[i + 1][0:-1]))
        allface.append(into)

readCountr = open('Countr.txt')
finalcountr = []

for line in readCountr:
    line = line[11:-3]
    line = line.split(', ')
    for i in range(0, len(line), 2):
        into = []
        into.append(int(line[i][1:len(line[i])]))
        into.append(int(line[i + 1][0:-1]))
        finalcountr.append(into)

readMarks = open('Marks.txt')
count = 0
x = []
y = []
z = []
for line in readMarks:
    if (count % 5 == 1):
        x.append(np.float32(line[5:-1]) * 3)
    elif (count % 5 == 2):
        y.append(np.float32(line[5:-1]) * 3)
    elif (count % 5 == 3):
        z.append(np.float32(line[5:-1]) * 3)
    count += 1

for i in range(len(x)):
    #x[i] = 1 - x[i]
    y[i] = 1 - y[i]
    #z[i] = 1 - z[i]
    #print(x[i], y[i], z[i])

x_ = []
y_ = []
z_ = []

for i in range(len(finalcountr)):
    allface.append(finalcountr[i])

allface.sort()
print(allface)
counter = 0
for i in range(len(allface)):
    for j in range(i + 1, len(allface)):
        if allface[i][0] == allface[j][1] and allface[i][1] == allface[j][0]:
            allface.pop(j)
            break
        if allface[i][0] == allface[j][0] and allface[i][1] == allface[j][1]:
            allface.pop(j)
            break

print(len(allface))



'''for i in range(6):
    x_.append(x[i])
    y_.append(y[i])
    z_.append(z[i])

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')
ax.plot(x, y, z)
ax.plot(x_, y_, z_, 'r-')
plt.show()'''
