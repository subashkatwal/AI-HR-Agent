from langgraph.graph import StateGraph, END
from google import generativeai as genai 
from django.conf import settings 
from core_app.LangGraph_Agents.utils.file_reader import extract_txt_from_pdf
import json 
from core_app.LangGraph_Agents.models.resume_model import Resume
import pytesseract
genai.configure(api_key=settings.GEMINI_API_KEY)

class ResumeParseState(dict):
    pdf_path: str
    extracted_text: str
    structured_resume: str

def create_doc_graph():
    graph= StateGraph(ResumeParseState)

    def extract_text_node(state: ResumeParseState):
        text= extract_txt_from_pdf(state['pdf_path'])
        state['extracted_text'] = text
        return state
    
    def parse_resume_node(state: ResumeParseState):
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
        You are a reumse parsing agent. Extract the following information from the given resume text:

        - name
        - email
        - contact_number
        - skills (list)
        - education (list of degree, university, location, start_date, end_date)
        - work_experience (list of strings)
        - years_of_experience
        - projects (list of name, description, duration)


        Return JSON following the schema: 
        {json.dumps(Resume.model_json_schema(),indent= 2)}

        Resume Text:
        {state['extracted_text']}

"""
        response = model.generate_content(prompt)
        state['structured_resume']= response.text
        return state
    
    graph.add_node("extract_text", extract_text_node)
    graph.add_node("parse_resume", parse_resume_node)

    graph.set_entry_point("extract_text")
    graph.add_edge("extract_text", "parse_resume")
    graph.add_edge("parse_resume", END)

    return graph.compile()




