#!/usr/bin/env python

from contextlib import contextmanager
import cv2

@contextmanager
def cv_camera(src):
  capture = cv2.VideoCapture(src)
  try:
    if not capture.isOpened():
      capture.open()
    yield capture
  finally:
    print 'Releasing video capture'
    capture.release()


@contextmanager
def cv_window(name):
  cv2.namedWindow(name)
  try:
    yield name
  finally:
    print 'Destroying window'
    cv2.destroyWindow(name)


def cv_frames(camera):
  while True:
    rval, frame = camera.read()
    if not rval:
      break
    yield frame


def esc_pressed():
  return cv2.waitKey(1) == 27 # ESC


with cv_window("preview") as win:
  with cv_camera(0) as camera:
    for frame in cv_frames(camera):
      height, width = frame.shape[:2]
      small = cv2.resize(frame, (width//2, height//2), interpolation = cv2.INTER_AREA) # INTER_CUBIC better for enlarging
      cv2.imshow(win, small)
      if esc_pressed(): break

# cv2.destroyAllWindows()
