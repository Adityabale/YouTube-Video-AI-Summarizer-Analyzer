import os
import mlflow
import mlflow.genai
from mlflow.genai.scorers import RelevanceToQuery, Safety, Completeness
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Configure MLflow tracking
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# Judge Model
JUDGE_MODEL = "gemini:/gemini-2.5-flash-lite"

# Ensure API Key is available for MLflow (it uses GOOGLE_API_KEY environment variable)
if not os.getenv("GOOGLE_API_KEY") and os.getenv("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# 1. Initialize built-in MLflow 3.x GenAI Scorers
relevance_scorer = RelevanceToQuery(model=JUDGE_MODEL)
safety_scorer = Safety(model=JUDGE_MODEL)
completeness_scorer = Completeness(model=JUDGE_MODEL)

def evaluate_summary(transcript, summary):
    """
    Evaluates the generated summary using MLflow 3.x GenAI evaluation framework.
    """
    try:
        # Prepare evaluation data
        # MLflow 3.x GenAI evaluation expects 'inputs' to be a dict
        eval_data = [
            {
                "inputs": {"query": transcript},
                "outputs": summary
            }
        ]

        # Run MLflow GenAI evaluation
        with mlflow.start_run(run_name="Summary_Evaluation_v3"):
            results = mlflow.genai.evaluate(
                data=eval_data,
                scorers=[relevance_scorer, safety_scorer, completeness_scorer]
            )
            
            # Extract results from the 'eval_results' table
            eval_table = results.tables["eval_results"]
            
            # Helper to extract score and explanation from the assessments list
            def get_assessment_data(table, scorer_name):
                # Columns for scores in 3.x are usually [scorer_name]/value
                score_col = f"{scorer_name}/value"
                score = 0.0
                if score_col in table.columns:
                    raw_val = table[score_col][0]
                    try:
                        score = float(raw_val)
                    except (ValueError, TypeError):
                        val_str = str(raw_val).strip().lower()
                        if val_str in ['yes', 'true', 'good', 'pass']:
                            score = 5.0
                        elif val_str in ['no', 'false', 'bad', 'fail']:
                            score = 1.0
                        else:
                            score = 0.0
                
                # Explanations are housed within the 'assessments' list column items
                explanation = "No explanation provided."
                if "assessments" in table.columns:
                    assessments_list = table["assessments"][0]
                    for assessment in assessments_list:
                        if assessment.get("assessment_name") == scorer_name:
                            explanation = assessment.get("rationale", "No explanation provided.")
                            break
                return {"score": score, "justification": explanation}

            metrics = {
                "relevance": get_assessment_data(eval_table, "relevance_to_query"),
                "safety": get_assessment_data(eval_table, "safety"),
                "completeness": get_assessment_data(eval_table, "completeness")
            }
            
            return metrics
            
    except Exception as e:
        print(f"Error during MLflow 3.x evaluation: {e}")
        import traceback
        traceback.print_exc()
        return None
