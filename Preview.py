import cv


cv.NamedWindow("preview",1)

capture = cv.CaptureFromCAM(0)

while True:
    frame = cv.QueryFrame(capture)
    cv.ShowImage("preview",frame)
    if cv.WaitKey(10) >= 0:
        break

cv.DestroyWindow("preview")
