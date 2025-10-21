from django.shortcuts import render
from rest_framework import generics,permissions
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404,get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from openai import OpenAI

client=OpenAI()

class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    authentication_classes=[]
    permission_classes=[permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        
        return Response(
            {"message":f"Doctor with Employeeid-{user.employee_id} created"},status=status.HTTP_201_CREATED
        )
# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#     authentication_classes = []
#     permission_classes = [permissions.AllowAny]
    
#     def create(self, request, *args, **kwargs):
#         print("=== REGISTER VIEW REACHED ===")
#         print("Request data:", request.data)
        
#         serializer = self.get_serializer(data=request.data)
        
#         print("=== BEFORE VALIDATION ===")
#         if not serializer.is_valid():
#             print("=== VALIDATION ERRORS ===")
#             print("Errors:", serializer.errors)
#             print("Error details:", dict(serializer.errors))  # Fixed this line
#             # This will raise the exception and return 400
#             serializer.is_valid(raise_exception=True)
        
#         print("=== AFTER VALIDATION - SAVING ===")
#         user = serializer.save()
#         print("=== USER CREATED ===")
        
#         return Response(
#             {"message": f"Doctor with Employeeid-{user.employee_id} created"}, 
#             status=status.HTTP_201_CREATED
#         )

class PhoneTokenObtainPairView(TokenObtainPairView):
    serializer_class=PhoneTokenObtainPairSerializer

    
class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class=PatientSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Patient.objects.filter(doctor=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class PatientDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Patient.objects.all()
    serializer_class=PatientSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Ensuere docter can only access their own patients
        
        return Patient.objects.filter(doctor=self.request.user)

class VisitListCreateView(generics.ListCreateAPIView):
    serializer_class=VisitSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        patient_id=self.kwargs.get('patient_id')
        return Visit.objects.filter(patient_id=patient_id)
    
    def perform_create(self, serializer):
        patient_id=self.kwargs.get('patient_id')
        patient=Patient.objects.get(id=patient_id,doctor=self.request.user)
        serializer.save(patient=patient)

# class VisitRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Visit.objects.all()
#     serializers_class=VisitSerializer
#     permission_classes=[permissions.IsAuthenticated]
    
#     def  get_queryset(self):
#         Visit.objects.get(patient__doctor=self.request.user)
class VisitRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VisitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Visit,
            pk=self.kwargs['pk'],
            patient__doctor=self.request.user  # ✅ ensures visit belongs to logged-in doctor
        )

    def delete(self, request, *args, **kwargs):
        visit = self.get_object()
        visit.delete()
        return Response({"message": "Visit deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    
    
    

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def prompt_ai(request):
    content = request.data.get("content", [])
    patient=request.data.get("patient",[])
    


    if not isinstance(content, list):
        return Response(
            {"error": "Invalid format, expected a list of visits"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Convert visits list into readable text for GPT
    visits_text = "\n".join([
        f"Visit {v.get('visit_no', '?')}: Diagnosis - {v.get('diagnosis', 'N/A')}, "
        f"Treatment - {v.get('treatment', 'N/A')}, "
        f"Test - {v.get('test', 'None')}, "
        f"Date - {v.get('date_created', 'N/A')}"
        for v in content
    ])
    # print(patient["weight_kg"])

    messages = [
        {
            "role": "system",
            "content": f"""
                    Patient details: Age: {patient['age']}, Weight: {patient['weight_kg']} kg, Height: {patient['height_cm']} cm, Gender: {patient['gender']}.

                    You are a medical assistant. Summarize the patient's visit history in a concise, clear paragraph(200words) for a doctor highlight the important key words, focusing on:
                    1. The main health issues observed.
                    2. Treatments administered in previous visits.
                    3. Any anomalies or inconsistencies in the treatments.
                    4. Suggested future actions, including possible tests or follow-ups, if applicable.

                    Stay focused on providing a meaningful and actionable summary of the patient's medical history that helps the doctor plan the next visit efficiently.
                    """

        },
        {
            "role": "user",
            "content": f"Here are the patient's visits:\n{visits_text}"
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        summary = response.choices[0].message.content
        # print(summary)
        return Response({"summary": summary}, status=status.HTTP_200_OK)

    except Exception as e:
        print("OpenAI Error:", e)
        return Response(
            {"error": f"An error occurred with OpenAI: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
# @api_view(["POST"])
# @permission_classes([permissions.IsAuthenticated])
# def prompt_ai(request):
#     content=request.data.get("content",[])
#     print(content)
    
#     if not isinstance(content,list):
#         return Response({"error":"Invalid format, Expected list of messages"},status=status.HTTP_400_BAD_REQUEST)
    
    
#     content.insert(0,{
#         "role":"assistant",
#         "content":"Give summary of patient visits so doctor can understand patients history"})
#     try:
#         response=client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=content
#         )
#         summary=response.choices[0].message.content
#         return Response({"summary":summary},status=status.HTTP_200_OK)
#     except Exception as e:
#         print(e)
#         return Response({"error":f"An error occured with OpenAI:{str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class=MyTokenObtainPairSerializer