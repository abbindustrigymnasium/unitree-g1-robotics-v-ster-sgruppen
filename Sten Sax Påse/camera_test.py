
import cv2

# Öppna datorns standardkamera
camera = cv2.VideoCapture(0)

# Kontrollera att kameran kunde öppnas
if not camera.isOpened():
    print("Kunde inte öppna kameran.")
    exit()

print("Kameran fungerar! Tryck på Q för att avsluta.")

while True:
    # Läs en bild från kameran
    success, frame = camera.read()

    if not success:
        print("Kunde inte läsa bilden från kameran.")
        break

    # Visa bilden på skärmen
    cv2.imshow("Min kamera", frame)

    # Avsluta om du trycker på Q
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Stäng kameran och fönstret
camera.release()
cv2.destroyAllWindows()
