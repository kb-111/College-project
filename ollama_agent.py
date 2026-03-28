"""
Ollama Agent Implementation 
Provides a wrapper around Ollama API for different project roles
"""
import os
from utils.helpers import call_ollama, extract_code_blocks, parse_json_safely, generate_system_prompt_for_role

class OllamaAgent:
    """Agent that uses Ollama for various project roles"""
    
    def __init__(self, role):
        """Initialize the agent with a specific role"""
        self.role = role
        self.system_prompt = generate_system_prompt_for_role(role)
    
    def generate_response(self, prompt, extract_code=False, parse_json=False):
        """Generate a response from Ollama based on the prompt"""
        response = call_ollama(prompt, self.role, self.system_prompt)
        
        if extract_code:
            return extract_code_blocks(response)
        
        if parse_json:
            return parse_json_safely(response)
        
        return response
    
    def generate_user_stories(self, business_requirements, template):
        """Generate user stories from business requirements"""
        from utils.prompts import BA_USER_STORY_TEMPLATE
        
        prompt = BA_USER_STORY_TEMPLATE.format(
            business_requirements=business_requirements,
            template=template
        )
        
        response = self.generate_response(prompt, parse_json=True)
        return response
    
    def generate_code(self, user_stories, template=""):
        """Generate code based on user stories"""
        from utils.prompts import DEV_CODE_TEMPLATE
        
        prompt = DEV_CODE_TEMPLATE.format(
            user_stories=user_stories,
            template=template
        )
        
        response = self.generate_response(prompt, extract_code=True)
        return response
    
    def generate_test_cases(self, user_stories, code, template=""):
        """Generate test cases for the provided code"""
        from utils.prompts import TESTER_TEST_CASE_TEMPLATE
        
        prompt = TESTER_TEST_CASE_TEMPLATE.format(
            user_stories=user_stories,
            code=code,
            template=template
        )
        
        response = self.generate_response(prompt, extract_code=True)
        return response
    
    def analyze_test_execution(self, code, test_cases):
        """Analyze test execution results"""
        from utils.prompts import TESTER_EXECUTION_TEMPLATE
        
        prompt = TESTER_EXECUTION_TEMPLATE.format(
            code=code,
            test_cases=test_cases
        )
        
        response = self.generate_response(prompt, parse_json=True)
        return response
    
    def answer_project_query(self, query):
        """Answer a project-related query"""
        from utils.prompts import PM_QUERY_TEMPLATE
        
        prompt = PM_QUERY_TEMPLATE.format(query=query)
        
        response = self.generate_response(prompt)
        return response