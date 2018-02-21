import logging

# below two lines create a logger with the name of the current module. and set its logging level to INFO.
mylogger = logging.getLogger(__name__)
mylogger.setLevel(level=logging.INFO)

# creating a filehandler which can be attached to any logger.
# Here we assign a file and also define a level of INFO at the file handler level.
# this basically acts like a filter on top of the logger.
# if the logger is set to lowest level of DEBUG and the filehandler is set to INFO.
# all the .DEBUG statements would not be sent to the below filehandleer
# because file handler has set a higher level of criteria of INFO compared to DEBUG.
myfileHandler = logging.FileHandler('D://python.logger')
myfileHandler.setLevel(level = logging.INFO)


myfileHandler2 = logging.FileHandler('D://python.logger.error')
myfileHandler2.setLevel(level = logging.ERROR)

mylogger.addHandler(myfileHandler)
mylogger.addHandler(myfileHandler2)

mylogger.info("ne ayya2")
mylogger.error("po bey")
mylogger.debug("debugging")

print(logging.ERROR, logging.DEBUG, logging.INFO, logging.WARN, logging.WARNING)
