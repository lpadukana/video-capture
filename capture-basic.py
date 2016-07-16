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


def resize_reduce(img, factor):
  height, width = img.shape[:2]
  return cv2.resize(img, (width//factor, height//factor), interpolation = cv2.INTER_AREA)
  # INTER_CUBIC better for enlarging


with cv_window("preview") as win:
  with cv_camera(0) as camera:
    for frame in cv_frames(camera):
      cv2.imshow(win, resize_reduce(frame, 4))
      if esc_pressed(): break

# cv2.destroyAllWindows()
