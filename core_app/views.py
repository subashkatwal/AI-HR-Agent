from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .LangGraph_Agents.Parser_agent import * 
import tempfile
import os 
import fitz
from core_app.models import Resume as ResumeModel

@csrf_exempt
def parse_resume_view(request):
    if request.method == "POST" and request.FILES.get("resume"):
        file = request.FILES["resume"]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            pdf_path = tmp.name

        graph = create_doc_graph()
        result = graph.invoke({'pdf_path':pdf_path})

        structured = result.get("structured_resume", "No output")
        
        if structured.startswith("```") and structured.endswith("```"):
            structured = "\n".join(structured.split("\n")[1:-1])
        
        
        structured_json = json.loads(structured)

        resume_instance = save_parsed_resume(structured_json, pdf_file=file)

        return JsonResponse({
    "message": "Resume saved successfully!",
    "resume_id": resume_instance.id
})


def upload_resume(request):
    if request.method == "POST" and request.FILES.get("resume"):
        resume_file = request.FILES["resume"]
        os.makedirs("uploads", exist_ok=True)
        save_path = os.path.join("uploads", resume_file.name)

        with open(save_path, "wb+") as f:
            for chunk in resume_file.chunks():
                f.write(chunk)

        return JsonResponse({
            "message": "Resume uploaded successfully!",
            "file_path": save_path
        })

    return render(request, "upload_resume.html")   

def view_resume_content(request, filename):
    
    file_path = f"uploads/{filename}"

    try:
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

   
    return JsonResponse({"content": text})


def save_parsed_resume(parsed_json, pdf_file=None):
    resume = ResumeModel.objects.create(
        name=parsed_json.get("name"),
        contact_number=parsed_json.get("contact_number"),
        email=parsed_json.get("email"),
        skills=parsed_json.get("skills", []),
        educations=parsed_json.get("educations", []),
        work_experiences=parsed_json.get("work_experiences", []),
        YoE=parsed_json.get("YoE"),
        pdf_file=pdf_file
    )
    if pdf_file:
        resume.pdf_file = pdf_file
    
    resume.save()
    return resume