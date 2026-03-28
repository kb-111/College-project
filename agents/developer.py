

# agents/developer.py
from langchain_community.llms import Ollama
import json
import os
import re

class DeveloperAgent:
    def __init__(self, llm, db_manager):
        """
        Initialize the DeveloperAgent with an Ollama model
        
        Args:
            model: The model to use (can be an Ollama instance or None)
            db_manager: Database manager for storing artifacts
        """
        # Initialize the model correctly
        # if model is None:
        #     # Create a default Ollama instance if no model is provided
        #     self.pipeline = Ollama(model="codellama:7b", base_url="http://localhost:11434")
        # elif isinstance(model, str):
        #     # If a string is provided, treat it as a model name for Ollama
        #     self.pipeline = Ollama(model=model, base_url="http://localhost:11434")
        # else:
        self.llm = llm
        self.db_manager = db_manager
    
    def _extract_code_blocks(self, text):
        """Extract code blocks from markdown text"""
        code_blocks = []
        pattern = r"```(?:python)?\s*(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        
        for match in matches:
            code_blocks.append(match.strip())
        
        return code_blocks
    
    def generate_code(self, user_stories):
        """Generate code based on user stories"""
        # Load code template
        template_path = "database/templates/code_template.py"
        with open(template_path, "r") as f:
            template_content = f.read()
        
        if isinstance(user_stories, str):
            try:
                user_stories = json.loads(user_stories)
            except json.JSONDecodeError:
                user_stories = [{"title": "Parsed from text", "description": user_stories}]
        
        # Create formatted prompt
        formatted_prompt = f"""
        You are an experienced Python Developer. Your task is to implement code based on the 
        following user stories.
        
        User Stories:
        {json.dumps(user_stories, indent=2)}
        
        Code Template:
        {template_content}
        
        Follow these guidelines:
        1. Generate clean, maintainable Python code that implements the functionality described in the user stories
        2. Include proper error handling
        3. Add comments explaining the key parts of your implementation
        4. Make sure your code follows PEP 8 style guidelines
        5. Return the code inside markdown code blocks with Python syntax highlighting
        
        For each user story, create a separate function or class as appropriate.
        """
        
        # Generate code using Ollama
        try:
            result = self.llm.invoke(
                formatted_prompt, 
                temperature=0.7,
                top_p=0.95,
                max_tokens=2048
            )
        except Exception as e:
            print(f"Error generating code with Ollama: {e}")
            # Simple fallback
            result = self.pipeline.invoke(formatted_prompt)
        
        # Extract code blocks from the result
        code_blocks = self._extract_code_blocks(result)
        
        # Save the generated code
        os.makedirs("artifacts/code", exist_ok=True)
        
        code_artifacts = []
        for idx, code_block in enumerate(code_blocks):
            code_id = f"code_artifact_{idx+1}"
            
            # Fix: Convert list of user story IDs to a comma-separated string for ChromaDB
            user_story_id_string = ",".join([f"user_story_{i+1}" for i in range(len(user_stories))])
            
            # Save to ChromaDB if available
            if self.db_manager:
                self.db_manager.store_artifact(
                    artifact_id=code_id,
                    content=code_block,
                    metadata={
                        "type": "code",
                        "language": "python",
                        "user_story_ids": user_story_id_string  # Fixed: String instead of list
                    }
                )
            
            # Save to file system
            file_path = f"artifacts/code/{code_id}.py"
            with open(file_path, "w") as f:
                f.write(code_block)
            
            code_artifacts.append({
                "id": code_id,
                "path": file_path,
                "content": code_block
            })
        
        # If no code blocks were extracted, save the raw output
        if not code_blocks:
            code_id = "code_artifact_raw"
            file_path = f"artifacts/code/{code_id}.txt"
            with open(file_path, "w") as f:
                f.write(result)
            
            # Fix: Convert list to string for ChromaDB
            user_story_id_string = ",".join([f"user_story_{i+1}" for i in range(len(user_stories))])
            
            if self.db_manager:
                self.db_manager.store_artifact(
                    artifact_id=code_id,
                    content=result,
                    metadata={
                        "type": "code_raw",
                        "user_story_ids": user_story_id_string  # Fixed: String instead of list
                    }
                )
            
            code_artifacts.append({
                "id": code_id,
                "path": file_path,
                "content": result
            })
        
        return code_artifacts