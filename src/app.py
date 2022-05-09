import cv2
import numpy as np

from src.detector import ActivitiesDetector

Layer = np.ndarray
fourcc = cv2.VideoWriter_fourcc(*"mp4v")


class AppController:
    _AUTHOR = 'meok'
    _RES_CAM = 800, 600  # 1280, 720
    _UI_HEIGHT = 30
    _UI_FONT = cv2.FONT_HERSHEY_COMPLEX_SMALL
    _UI_COLOR = (0, 255, 0)

    def __init__(self):
        self._running: bool = True
        self._ui_need_refresh: bool = False
        # Resolution must be set before using class methods
        self._resolution: tuple[int, int] = self._RES_CAM[0], self._RES_CAM[1] + self._UI_HEIGHT
        self._detector = ActivitiesDetector(self._RES_CAM)
        self._ui: Layer = self.__ui_create()
        self.__init_capture()
        self._x = 0

    def __ui_create(self) -> Layer:
        _ui_arr: Layer = np.zeros((self._UI_HEIGHT, self._resolution[0], 3), np.uint8)
        # ui[:] = 0, 255, 0  # Fill by color
        cv2.line(_ui_arr, (0, 0), (_ui_arr.shape[1], 0), self._UI_COLOR, 1)  # Delimiter
        _author: str = f'created by: {self._AUTHOR}'
        cv2.putText(_ui_arr, _author, (_ui_arr.shape[1] - len(_author) * 9, 20), self._UI_FONT, 0.6, self._UI_COLOR, 1)
        return _ui_arr

    def __handle_recording(self) -> None:
        if self._detector.recording:
            self._ui_need_refresh = True
            _half_height = self._ui.shape[0] // 2
            _red_color = (0, 0, 255)
            cv2.circle(self._ui, (_half_height + 2, _half_height), _half_height - 6, _red_color, cv2.FILLED)
            cv2.putText(self._ui, "RECORDING", (self._ui.shape[0], _half_height + 7), self._UI_FONT, 1, _red_color, 1)
        elif self._ui_need_refresh:
            self._ui_need_refresh = False
            cv2.rectangle(self._ui, (1, 1), (200, self._ui.shape[0]), (0, 0, 0), cv2.FILLED)
            print('Ui refreshed')

    def __init_capture(self) -> None:
        self._capture = cv2.VideoCapture(0)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self._RES_CAM[0])
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self._RES_CAM[1])
        # self._capture.set(cv2.CAP_PROP_BRIGHTNESS, 50)
        # self._capture.set(cv2.CAP_PROP_CONTRAST, 50)
        # self._capture.set(cv2.CAP_PROP_SATURATION, 50)  # Насыщенность
        # self._capture.set(cv2.CAP_PROP_HUE, 5)   # Оттенок
        # self._capture.set(cv2.CAP_PROP_GAIN, 5)  # Усиление
        # self._capture.set(cv2.CAP_PROP_FPS, 10)

    def run(self):
        while self._running:
            _, _frame = self._capture.read()

            self._detector.handle(_frame)
            self.__handle_keys()
            self.__handle_recording()

            picture = np.vstack((_frame, self._ui))  # Join camera and ui
            cv2.imshow("Security system", picture)

    def __handle_keys(self) -> None:
        _key = cv2.waitKey(1)
        if _key == ord('q'):
            self._running = False
        elif _key == ord('i'):
            self.__print_capture_params()
        elif _key == ord('z'):
            self.__low_brightness()
        elif _key >= 0:
            print(f'Press `q` to quit')

    def __print_capture_params(self):
        x = self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        print(f'Parameter FRAME_WIDTH = {x}')
        x = self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f'Parameter FRAME_HEIGHT = {x}')
        x = self._capture.get(cv2.CAP_PROP_BRIGHTNESS)
        print(f'Parameter BRIGHTNESS = {x}')
        x = self._capture.get(cv2.CAP_PROP_CONTRAST)
        print(f'Parameter CONTRAST = {x}')
        x = self._capture.get(cv2.CAP_PROP_SATURATION)  # Насыщенность
        print(f'Parameter SATURATION = {x}')
        x = self._capture.get(cv2.CAP_PROP_HUE)   # Оттенок
        print(f'Parameter HUE = {x}')
        x = self._capture.get(cv2.CAP_PROP_GAIN)  # Усиление
        print(f'Parameter GAIN = {x}')
        x = self._capture.get(cv2.CAP_PROP_FPS)
        print(f'Parameter FPS = {x}')

    def __low_brightness(self):
        if not self._x:
            self._x = self._capture.get(cv2.CAP_PROP_BRIGHTNESS)
        self._x -= 5
        self._capture.set(cv2.CAP_PROP_BRIGHTNESS, self._x)
        print(f'Set brightness to {self._x}')
