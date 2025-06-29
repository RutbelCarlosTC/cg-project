# otro_script.py
from main import SignRecognizer

# Crear objeto
recognizer = SignRecognizer()
recognizer.run_loop()
print("Última seña detectada:", recognizer.get_last_sign())

# O ejecutar en bucle
# recognizer.run_loop()
# print("Última seña detectada:", recognizer.get_last_sign())
