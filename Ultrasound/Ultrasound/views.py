import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
import joblib
from keras.models import load_model # type: ignore
from keras.applications.xception import preprocess_input # type: ignore
from PIL import Image
from numpy import array # type: ignore
import gzip
import shutil
from .models import Patient


# Home page
def home(request):

    return render(request, 'home.html')



# Add an ultrasound kidney to detect renal failure
def addUltrasoundImg(request):

    return render(request, 'addUltrasoundImg.html')

def addKidneyFeatures(request):

    return render(request, 'addKidneyFeature.html')


# Decting renal failure
def predictFromUltrasoundImg(request):
    if request.method == 'POST':
        PatientName = request.POST.get('PatientName')
        UltrasoundImg = request.FILES.get('UltrasoundImg')
        noteMedical = request.POST.get('noteMedical')
       # Enrégistrer les données
        patient = Patient(PatientName=PatientName, noteMedical=noteMedical, UltrasoundImg=UltrasoundImg)
        patient.save()
       # Transformer l'image en array et la redimensionner au format d'entrée (1, 224, 224, 3)
        Img = Image.open(UltrasoundImg).convert('RGB')
        Img = Img.resize((224, 224))
        #Img = open(UltrasoundImg).resize((224, 224))
        X = array(Img).reshape(1, 224, 224, 3)
        # Prétraitement de les données d'entées avec preprocess_input de Xception
        X = preprocess_input(X).astype('float32')

        # Charger le modèle de machine learning pour la prédiction
        model = load_model('static/model/HyperbandModel.h5')

        # Prediction
        y_predict = model.predict(X)
        result = float(y_predict[0][1])
        #result =0.9916
        result = f"{result * 100:.2f}%"
        # Retourner la réponse au format JSON
        return JsonResponse({'prediction': result})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def predictFromKidneyFeatures(request):
    if request.method == 'POST':
        #PatientName = request.POST.get('PatientName')
        TypeDiabete = request.POST.get('TypeDiabete')
        TensionArterielle = request.POST.get('TensionArterielle')
        Age = request.POST.get('Age')
        GraviteSpecifique = request.POST.get('GraviteSpecifique')
        CreatinineSerique = request.POST.get('CreatinineSerique')
        Hypertension = request.POST.get('Hypertension')
        UreeSanguine = request.POST.get('UreeSanguine')
        GlycemieAleatoire = request.POST.get('GlycemieAleatoire')
        Albumine = request.POST.get('Albumine')
        #NoteMedicale = request.POST.get('NoteMedicale')
        
       # Enrégistrer les données

       # Créer un DataFrame avec les données du patient
        data = pd.DataFrame({
           "albumine" :[Albumine] , "créatinine sérique":[CreatinineSerique], "urée sanguine" :[UreeSanguine], 
           "tension artérielle": [TensionArterielle],  " gravité spécifique":[GraviteSpecifique], "glycémie aléatoire": [GlycemieAleatoire] ,
           "age": [Age], "diabète sucré_Oui": [TypeDiabete], "hypertension_Oui" : [Hypertension]
          })
       
      
        # Charger le modèle de machine learning pour la prédiction
        model= joblib.load('static/model/logit.joblib')
       
        # Prediction
        y_predict = model.predict(data)
        result = float(y_predict)
        #result =0.9916
        result = f"{result * 100:.2f}%"
        # Retourner la réponse au format JSON
        return JsonResponse({'prediction': result})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def decompress_h5_file(input_file, output_file):
    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


