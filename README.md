# Face Identification

Fece tracking and recognition using OpenCV and Microsoft Azure's Face APIs. The API request is sent only when a new face is detected. When a face is detected, a tracker is associated with it until the tracking confidence drops below a threshold (configurable).

## Installation
The `requirements.txt` file contains much more than the strict requirements to run this app, but saves time to just install everything at once.

### Setup
Run these scripts sequentialy. You will need to appropriately edit these scripts to include the correct Face API subscription key, names, and images of the people.

```sh
# Create a group
python Azure/train_faces_create_person_group_1.py

# Add people to the group
python Azure/train_faces_add_person_2.py

# Add faces for the poeple
python Azure/train_faces_add_face_3.py

# Train the API to learn the faces and associate the features wiht the people
python Azure/train_faces_train_4.py
```

### Execution
To run the detector:
```sh
python demo - detect and track.py
```

This script internally imports `train_faces_detect_face_5.py` which takes the address of a local image on the disk and returns the `name`, `confidence` of the person with highest score.

# Screenshots

The `PersonGroup` contained one image each of 6 people including `Garvit` and `Obama`. With only one image, the classifier returns a high confidence level.

![Screenshot 1](https://github.com/TheGarvitGupta/Face-Identification/blob/master/Screenshots/scr_1.png "Screenshot 1")
Screenshot 1

![Screenshot 2](https://github.com/TheGarvitGupta/Face-Identification/blob/master/Screenshots/scr_2.png "Screenshot 2")
Screenshot 2

# Reference

Tracking code forked from: https://www.guidodiepen.nl/2017/02/detecting-and-tracking-a-face-with-python-and-opencv/
GitHub Link: https://github.com/gdiepen/face-recognition