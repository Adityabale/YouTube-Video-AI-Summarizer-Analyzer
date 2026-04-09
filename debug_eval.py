import os
import mlflow
import mlflow.genai
import pandas as pd
from mlflow.genai.scorers import RelevanceToQuery, Safety, Completeness
from dotenv import load_dotenv
import traceback

load_dotenv()

# Configure MLflow tracking
tracking_path = os.path.join(os.getcwd(), "mlruns").replace("\\", "/")
mlflow.set_tracking_uri(f"file:///{tracking_path}")

JUDGE_MODEL = "gemini:/gemini-2.5-flash-lite"
if not os.getenv("GOOGLE_API_KEY") and os.getenv("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

relevance_scorer = RelevanceToQuery(model=JUDGE_MODEL)
safety_scorer = Safety(model=JUDGE_MODEL)
completeness_scorer = Completeness(model=JUDGE_MODEL)

def main():
    transcript = "This is a video about building a house. First you lay the foundation, then you build walls."
    summary = "A video guide on house construction starting with foundation and walls."
    
    eval_data = [{"inputs": {"query": transcript}, "outputs": summary}]

    with mlflow.start_run(run_name="Diagnostic"):
        results = mlflow.genai.evaluate(
            data=eval_data,
            scorers=[relevance_scorer, safety_scorer, completeness_scorer]
        )
        
        eval_table = results.tables["eval_results"]
        for col in eval_table.columns:
            print(f"Col {col}: {eval_table[col][0]}")
            
        print("Assessments list:")
        for asm in eval_table["assessments"][0]:
            print(asm)

if __name__ == "__main__":
    main()
