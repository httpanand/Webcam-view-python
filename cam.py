from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import os
import sys
import time
  
class MainWindow(QMainWindow):
  

    def __init__(self):
        super().__init__()
  
        self.setGeometry(100, 100,
                         800, 600)

        self.setStyleSheet("background : lightgrey;")
        self.available_cameras = QCameraInfo.availableCameras()
  
        if not self.available_cameras:

            alert('cam not found')
            sys.exit()

        self.status = QStatusBar()
        self.status.setStyleSheet("background : white;")
  
        self.setStatusBar(self.status)

        self.save_path = ""

        self.viewfinder = QCameraViewfinder()

        self.viewfinder.show()
        self.setCentralWidget(self.viewfinder)
        self.select_camera(0)

        toolbar = QToolBar("Camera Tool Bar")
  
        self.addToolBar(toolbar)

 
  

        camera_selector = QComboBox()
        camera_selector.setStatusTip("Choose camera to take pictures")
        camera_selector.setToolTip("Select Camera")
        camera_selector.setToolTipDuration(2500)
        camera_selector.addItems([camera.description()
                                  for camera in self.available_cameras])

        camera_selector.currentIndexChanged.connect(self.select_camera)

        toolbar.addWidget(camera_selector)

        toolbar.setStyleSheet("background : white;")
  
        self.setWindowTitle("CAM")
  
        self.show()
  

    def select_camera(self, i):

        self.camera = QCamera(self.available_cameras[i])
  
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
  
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
  
        self.camera.start()
  
        self.capture = QCameraImageCapture(self.camera)
  
    
        self.capture.error.connect(lambda error_msg, error,
                                   msg: self.alert(msg))
  

        self.capture.imageCaptured.connect(lambda d,
                                           i: self.status.showMessage("Image captured : " 
                                                                      + str(self.save_seq)))
  
        
        self.current_camera_name = self.available_cameras[i].description()
  
       
        self.save_seq = 0
  
  
    def click_photo(self):
  
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
  
       
        self.capture.capture(os.path.join(self.save_path, 
                                          "%s-%04d-%s.jpg" % (
            self.current_camera_name,
            self.save_seq,
            timestamp
        )))
  
        
        self.save_seq += 1
  
 
        if path:
  
          
            self.save_path = path
            self.save_seq = 0
  
    def alert(self, msg):
        error = QErrorMessage(self)
        error.showMessage(msg)
  
if __name__ == "__main__" :

  App = QApplication(sys.argv)
  window = MainWindow()
  sys.exit(App.exec())