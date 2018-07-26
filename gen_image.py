import cv2 as cv
import numpy

shape = (3000, 200)
oo = numpy.zeros(shape, dtype=None, order='C')
oo.fill(127)
cv.imwrite('200.bmp', oo)


shape = (3000, 300)
oo = numpy.zeros(shape, dtype=None, order='C')
oo.fill(127)
cv.imwrite('300.bmp', oo)

shape = (3000, 400)
oo = numpy.zeros(shape, dtype=None, order='C')
oo.fill(127)
cv.imwrite('400.bmp', oo)
