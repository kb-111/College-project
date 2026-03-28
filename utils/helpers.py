# # utils/helpers.py
# """
# Helper functions for the project team simulation
# """
# import re
# import json
# import os

# def extract_code_blocks(text):
#     """Extract code blocks from markdown text"""
#     code_blocks = []
#     pattern = r"```(?:python)?\s*(.*?)```"
#     matches = re.findall(pattern, text, re.DOTALL)
    
#     for match in matches:
#         code_blocks.append(match.strip())
    
#     return code_blocks

# def ensure_directory_exists(directory_path):
#     """Ensure a directory exists, create it if it doesn't"""
#     if not os.path.exists(directory_path):
#         os.makedirs(directory_path)

# def load_template(template_path):
#     """Load a template file"""
#     with open(template_path, "r") as f:
#         return f.read()

# def save_artifact(artifact_id, content, artifact_type, directory=None):
#     """Save an artifact to a file"""
#     if directory is None:
#         directory = f"artifacts/{artifact_type}s"
    
#     ensure_directory_exists(directory)
    
#     file_extension = ".py" if artifact_type == "code" else ".json" if artifact_type == "user_story" else ".txt"
#     file_path = f"{directory}/{artifact_id}{file_extension}"
    
#     with open(file_path, "w") as f:
#         if artifact_type == "user_story" and isinstance(content, dict):
#             json.dump(content, f, indent=2)
#         else:
#             f.write(content)
    
#     return file_path

# def parse_json_safely(json_string):
#     """Safely parse JSON string with fallback for malformed JSON"""
#     try:
#         return json.loads(json_string)
#     except json.JSONDecodeError:
#         # Try to fix common JSON errors
#         # 1. Missing quotes around keys
#         fixed_string = re.sub(r'(\s*?)(\w+)(\s*?):', r'\1"\2"\3:', json_string)
#         # 2. Single quotes instead of double quotes
#         fixed_string = fixed_string.replace("'", "\"")
        
#         try:
#             return json.loads(fixed_string)
#         except json.JSONDecodeError:
#             # Return a basic structure if all else fails
#             return {"error": "Could not parse JSON", "content": json_string}

"""
Helper functions for the project team simulation with Ollama integration
"""
import re
import json
import os
import requests

def extract_code_blocks(text):
    """Extract code blocks from markdown text"""
    code_blocks = []
    pattern = r"```(?:python)?\s*(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    
    for match in matches:
        code_blocks.append(match.strip())
    
    return code_blocks

def ensure_directory_exists(directory_path):
    """Ensure a directory exists, create it if it doesn't"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def load_template(template_path):
    """Load a template file"""
    with open(template_path, "r") as f:
        return f.read()

def save_artifact(artifact_id, content, artifact_type, directory=None):
    """Save an artifact to a file"""
    if directory is None:
        directory = f"artifacts/{artifact_type}s"
    
    ensure_directory_exists(directory)
    
    file_extension = ".py" if artifact_type == "code" else ".json" if artifact_type == "user_story" else ".txt"
    file_path = f"{directory}/{artifact_id}{file_extension}"
    
    with open(file_path, "w") as f:
        if artifact_type == "user_story" and isinstance(content, dict):
            json.dump(content, f, indent=2)
        else:
            f.write(content)
    
    return file_path

def parse_json_safely(json_string):
    """Safely parse JSON string with fallback for malformed JSON"""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        # Try to fix common JSON errors
        # 1. Missing quotes around keys
        fixed_string = re.sub(r'(\s*?)(\w+)(\s*?):', r'\1"\2"\3:', json_string)
        # 2. Single quotes instead of double quotes
        fixed_string = fixed_string.replace("'", "\"")
        
        try:
            return json.loads(fixed_string)
        except json.JSONDecodeError:
            # Return a basic structure if all else fails
            return {"error": "Could not parse JSON", "content": json_string}

def call_ollama(prompt, role, system_prompt=None):
    """Call Ollama API with the specified prompt and parameters"""
    # Get parameters for the specified role
    from utils.prompts import OLLAMA_PARAMS
    params = OLLAMA_PARAMS.get(role, OLLAMA_PARAMS["developer"])
    
    # Prepare the request data
    data = {
        "model": params["model"],
        "prompt": prompt,
        "options": {
            "temperature": params["temperature"],
            "top_p": params["top_p"],
            "num_predict": params["num_predict"]
        },
        "stream": params["stream"]
    }
    
    # Add system prompt if provided
    if system_prompt:
        data["system"] = system_prompt
    
    # Make the API call
    try:
        response = requests.post("http://localhost:11434/api/generate", json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama: {e}")
        return f"Error calling Ollama: {e}"

def generate_system_prompt_for_role(role):
    """Generate a system prompt for the specified role"""
    system_prompts = {
        "business_analyst": "You are an experienced Business Analyst helping to translate business requirements into clear user stories.",
        "developer": "You are an experienced Python Developer writing clean, maintainable code to implement user stories.",
        "tester": "You are an experienced QA Tester creating thorough test cases to validate code against user stories.",
        "project_manager": "You are a Project Manager overseeing a software development project and reporting on its status."
    }
    return system_prompts.get(role, "You are an AI assistant helping with a software development project.")