import cv2
import time
import datetime
import os

fourcc = cv2.VideoWriter_fourcc(*"mp4v")


class ActivitiesDetector:
    _DETECTOR_SENSITIVITY = 1.1
    _NO_ACTION_TIMEOUT = 5  # Second to continue record after no action on camera
    _FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    _BODY_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")
    _FOLDER_NAME = 'video'

    def __init__(self, resolution: tuple[int, int]):
        self._resolution = resolution
        self._recording: bool = False
        self._no_actions: bool = False
        self._no_actions_from: time.time = None

        self._out_file: cv2.VideoWriter
        self.__check_folder()

    @property
    def recording(self) -> bool:
        return self._recording

    def handle(self, frame) -> None:
        _gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _faces = self._FACE_CASCADE.detectMultiScale(_gray_frame, self._DETECTOR_SENSITIVITY, 5)
        _bodies = self._BODY_CASCADE.detectMultiScale(_gray_frame, self._DETECTOR_SENSITIVITY, 5)

        if len(_faces) + len(_bodies) > 0:
            # print(f'Detected faces: {len(_faces)} bodies: {len(_bodies)}')
            self._no_actions = False
            if not self._recording:
                self.__start_recording()
        elif self._recording:
            if not self._no_actions:
                self._no_actions_from = time.time()
            self._no_actions = True
            if time.time() - self._no_actions_from >= self._NO_ACTION_TIMEOUT:
                self.__stop_recording()

        if self._recording:
            self._out_file.write(frame)

        for (x, y, width, height) in _faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

    def __start_recording(self) -> None:
        self._recording = True
        _file_name = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        self._out_file = cv2.VideoWriter(f"./{self._FOLDER_NAME}/{_file_name}.mp4", fourcc, 20, self._resolution)
        print(f'Start recording {self._out_file.getBackendName()}')

    def __stop_recording(self) -> None:
        self._recording = False
        self._out_file.release()
        print(f'Stop recording')

    def __check_folder(self):
        if not os.path.isdir(self._FOLDER_NAME):
            os.makedirs(self._FOLDER_NAME)
            print(f'Create video folder - `{self._FOLDER_NAME}`')
