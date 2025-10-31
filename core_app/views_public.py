# views_public.py (new file or just new functions)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .LangGraph_Agents.Parser_agent import create_doc_graph
import tempfile
import os
import json
from core_app.models import Resume as ResumeModel
import fitz

@csrf_exempt
def public_parse_resume_view(request):
    """
    Public endpoint to upload and parse resumes.
    Can be exposed to friends for practice.
    """
    if request.method == "POST" and request.FILES.get("resume"):
        uploaded_file = request.FILES["resume"]

        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            for chunk in uploaded_file.chunks():
                tmp.write(chunk)
            temp_pdf_path = tmp.name

        # Parse resume
        graph = create_doc_graph()
        result = graph.invoke({'pdf_path': temp_pdf_path})

        structured = result.get("structured_resume", "No output")

        # Remove markdown-style code blocks if present
        if structured.startswith("```") and structured.endswith("```"):
            structured = "\n".join(structured.split("\n")[1:-1])

        # Convert to JSON
        structured_json = json.loads(structured)

        # Save to DB
        resume_instance = save_public_resume(structured_json, pdf_file=uploaded_file)

        return JsonResponse({
            "message": "Resume uploaded and saved successfully!",
            "resume_id": resume_instance.id
        })

    return JsonResponse({"error": "POST a PDF file under 'resume'"}, status=400)


def save_public_resume(parsed_json, pdf_file=None):
    """
    Save the parsed resume in the DB without affecting old implementation
    """
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


@csrf_exempt
def public_upload_resume_page(request):
    """
    Optional: simple HTML form for friends to upload resumes
    """
    if request.method == "POST" and request.FILES.get("resume"):
        uploaded_file = request.FILES["resume"]
        os.makedirs("uploads_public", exist_ok=True)
        save_path = os.path.join("uploads_public", uploaded_file.name)
        with open(save_path, "wb+") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        return JsonResponse({"message": "Resume uploaded successfully!", "file_path": save_path})

    return render(request, "public_upload_resume.html")
