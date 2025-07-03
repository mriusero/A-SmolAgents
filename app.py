from smolagents import CodeAgent,DuckDuckGoSearchTool, InferenceClientModel, load_tool, tool
import os 
import datetime
import requests
import urllib.parse
import pytz
import yaml

from tools.final_answer import FinalAnswerTool
from tools.web_search import DuckDuckGoSearchTool
from tools.visit_webpage import VisitWebpageTool
from tools.get_timezone import get_current_time_in_timezone
from tools.calculate import calculator
from tools.analyze_repo import GitHubAnalyzerTool

from Gradio_UI import GradioUI

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_custom_tool(arg1:str, arg2:int)-> str: #it's import to specify the return type
    #Keep this format for the description / args / args description but feel free to modify the tool
    """A tool that does nothing yet 
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"

final_answer = FinalAnswerTool()
web_search = DuckDuckGoSearchTool()
visit_webpage = VisitWebpageTool()
analyze_github_repository = GitHubAnalyzerTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

model = InferenceClientModel(
max_tokens=2096,
temperature=0.5,
model_id='Qwen/Qwen2.5-Coder-32B-Instruct',# it is possible that this model may be overloaded
token=os.getenv('HF_TOKEN'),
custom_role_conversions=None,
)


# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        web_search,
        visit_webpage,
        get_current_time_in_timezone,
        calculator,
        analyze_github_repository,
    ], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


GradioUI(agent).launch()