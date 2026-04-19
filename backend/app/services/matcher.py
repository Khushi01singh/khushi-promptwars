import os
import logging
from typing import TypedDict, List, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langgraph.graph import StateGraph, END

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the structured output format
class MatchResult(BaseModel):
    match_score: int = Field(description="Integer between 0 and 100 representing the match score")
    matched_skills: List[str] = Field(description="List of skills from the job description that the candidate possesses")
    missing_skills: List[str] = Field(description="List of core skills required by the job that the candidate lacks")
    reasoning: str = Field(description="A 2-3 sentence explanation of the match focusing on evidence and transferable skills")

# Define the LangGraph state
class JobMatchState(TypedDict):
    resume_text: str
    job_description: str
    output_json: Dict[str, Any]
    error: str

class JobMatcher:
    def __init__(self, model_name: str = "gemini-pro"):
        """Initialize the JobMatcher with a specific LLM and prompts."""
        self.model_name = model_name
        self.parser = PydanticOutputParser(pydantic_object=MatchResult)
        
        # System prompt with Persona Engineering
        self.system_prompt = """
        You are a Professional Technical Recruiter. Your task is to evaluate a candidate's resume against a job description.
        Focus on evidence-based matching and recognize transferable skills.
        Additionally, assess whether the candidate's professional trajectory aligns with the growth potential required for this specific role.
        Provide a fair, objective assessment based strictly on the text provided.
        
        {format_instructions}
        """
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", "Job Description:\n{job_description}\n\nCandidate Resume:\n{resume_text}")
        ])
        
        # Build the LangGraph workflow
        self.workflow = self._build_graph()

    def _build_graph(self):
        """Constructs the LangGraph state machine."""
        workflow = StateGraph(JobMatchState)
        workflow.add_node("evaluate_candidate", self._evaluate_node)
        workflow.set_entry_point("evaluate_candidate")
        workflow.add_edge("evaluate_candidate", END)
        return workflow.compile()

    def _evaluate_node(self, state: JobMatchState) -> JobMatchState:
        """LangGraph Node to run the LLM evaluation."""
        logger.info("Starting candidate evaluation node.")
        
        # --- DEBUGGING SNIPPET FOR CLOUD RUN ---
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            logger.error("DEBUG: GOOGLE_API_KEY environment variable is explicitly None or empty!")
        else:
            # Mask the key for security in logs
            masked_key = api_key[:4] + "***" + api_key[-4:] if len(api_key) > 8 else "***"
            logger.info(f"DEBUG: GOOGLE_API_KEY is detected successfully! Masked value: {masked_key}")
        # ----------------------------------------

        try:
            # Initialize the LLM explicitly passing the key to avoid Langchain autodetection bugs
            llm = ChatGoogleGenerativeAI(
                model=self.model_name, 
                temperature=0.1,
                google_api_key=api_key
            )
            
            # Create the LangChain processing pipeline
            chain = self.prompt | llm | self.parser
            
            logger.info("Invoking LLM chain for match analysis...")
            result: MatchResult = chain.invoke({
                "job_description": state["job_description"],
                "resume_text": state["resume_text"],
                "format_instructions": self.parser.get_format_instructions()
            })
            
            logger.info(f"Evaluation complete. Match Score: {result.match_score}")
            return {"output_json": result.model_dump(), "error": ""}
            
        except Exception as e:
            logger.error(f"Error during LLM evaluation: {str(e)}")
            # Fallback for graceful failure if API key is missing or parsing fails
            fallback_result = {
                "match_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "reasoning": "Evaluation failed. Please ensure GOOGLE_API_KEY is configured in the environment."
            }
            return {"output_json": fallback_result, "error": str(e)}

    def evaluate(self, sanitized_resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Public method to evaluate a candidate.
        Accepts sanitized resume text and a job description.
        Returns a structured JSON result.
        """
        logger.info("JobMatcher.evaluate called.")
        initial_state = {
            "resume_text": sanitized_resume_text,
            "job_description": job_description,
            "output_json": {},
            "error": ""
        }
        
        result = self.workflow.invoke(initial_state)
        return result.get("output_json", {})

# Singleton instance to be used by the FastAPI routers
matcher_service = JobMatcher()
