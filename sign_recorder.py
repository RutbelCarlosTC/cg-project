import pandas as pd
import numpy as np
from collections import Counter

from utils.dtw import dtw_distances
from models.sign_model import SignModel
from utils.landmark_utils import extract_landmarks


class SignRecorder(object):
    def __init__(self, reference_signs: pd.DataFrame, seq_len=50):
        # Variables para la grabación
        self.is_recording = False
        self.seq_len = seq_len

        # Lista para almacenar los resultados de cada fotograma
        self.recorded_results = []

        # DataFrame que almacena las distancias entre la seña grabada y las señas de referencia del dataset
        self.reference_signs = reference_signs

    def record(self):
        """
        Inicializa las distancias y comienza la grabación
        """
        self.reference_signs["distance"].values[:] = 0
        self.is_recording = True

    def process_results(self, results) -> (str, bool):  # type: ignore
        """
        Si el SignRecorder está en estado de grabación:
            almacena los puntos de referencia durante seq_len fotogramas
            y luego calcula las distancias con las señas de referencia

        :param results: salida de mediapipe
        :return: Devuelve la palabra predicha (texto vacío si no se han calculado distancias)
                 y el estado de grabación
        """
        if self.is_recording:
            if len(self.recorded_results) < self.seq_len:
                self.recorded_results.append(results)
            else:
                self.compute_distances()
                print(self.reference_signs)

        if np.sum(self.reference_signs["distance"].values) == 0:
            return "", self.is_recording
        return self._get_sign_predicted(), self.is_recording

    def compute_distances(self):
        """
        Actualiza la columna de distancias del DataFrame reference_signs
        y reinicia las variables de grabación
        """
        left_hand_list, right_hand_list = [], []
        for results in self.recorded_results:
            _, left_hand, right_hand = extract_landmarks(results)
            left_hand_list.append(left_hand)
            right_hand_list.append(right_hand)

        # Crear un objeto SignModel con los puntos recolectados durante la grabación
        recorded_sign = SignModel(left_hand_list, right_hand_list)

        # Calcular la similitud con otras señas usando DTW (orden ascendente)
        self.reference_signs = dtw_distances(recorded_sign, self.reference_signs)

        # Reiniciar variables
        self.recorded_results = []
        self.is_recording = False

    def _get_sign_predicted(self, batch_size=5, threshold=0.2):
        """
        Método que determina la seña más común en el lote de señas de referencia más cercanas,
        siempre que su proporción sea mayor al umbral especificado

        :param batch_size: Tamaño del lote de señas de referencia a comparar con la seña grabada
        :param threshold: Si la proporción de la seña más representada supera el umbral,
                          se devuelve el nombre de la seña
                          Si no, se devuelve "Seña desconocida"
        :return: El nombre de la seña predicha
        """
        # Obtener la lista (de tamaño batch_size) de las señas más similares
        sign_names = self.reference_signs.iloc[:batch_size]["name"].values

        # Contar las ocurrencias de cada seña y ordenarlas de forma descendente
        sign_counter = Counter(sign_names).most_common()

        predicted_sign, count = sign_counter[0]
        if count / batch_size < threshold:
            return "Seña desconocida"
        return predicted_sign
