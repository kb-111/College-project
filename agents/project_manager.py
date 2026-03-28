

from langchain.prompts import PromptTemplate
from langchain.agents import Tool
from langchain.agents import AgentExecutor
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain_core.language_models import BaseLanguageModel
import json

class ProjectManagerAgent:
    def __init__(self, llm_model, db_manager=None):
        if isinstance(llm_model, str):
            print(f"✅ Loading Ollama model: {llm_model}")
            self.llm = Ollama(model=llm_model, base_url="http://localhost:11434", temperature=0.7)
        elif isinstance(llm_model, BaseLanguageModel):
            print(f"✅ Using existing LLM model instance: {type(llm_model).__name__}")
            self.llm = llm_model
        else:
             raise ValueError(f"llm_model must be a string or LangChain-compatible model. Got: {type(llm_model)}")
        
        # # Create Ollama directly - no need for tokenizer/model loading
        # self.llm = Ollama(
        #     model=llm_model,
        #     base_url="http://localhost:11434",
        #     temperature=0.7,
        #     # max_tokens=256
        # )
        
        # my_llm = Ollama(model="codellama:7b")
        # self.pm_agent = ProjectManagerAgent(my_llm, self.db_manager)

        self.db_manager = db_manager
    
    def get_status(self, query):
        """Get project status based on PM query."""
        tools = [
            Tool(name="retrieve_user_stories", func=self._retrieve_user_stories,
                 description="Retrieve user stories from the project repository"),
            Tool(name="retrieve_code", func=self._retrieve_code,
                 description="Retrieve code artifacts from the project repository"),
            Tool(name="retrieve_test_cases", func=self._retrieve_test_cases,
                 description="Retrieve test cases from the project repository"),
            Tool(name="retrieve_test_results", func=self._retrieve_test_results,
                 description="Retrieve test execution results from the project repository"),
            Tool(name="search_artifacts", func=self._search_artifacts,
                 description="Search through all project artifacts based on query")
        ]
        
        prompt = PromptTemplate(
            template="""
            You are a Project Manager overseeing a software development project. Your team consists of 
            Business Analysts, Developers, and QA Testers.
            
            Your task is to provide status updates and answer questions about the project artifacts and progress.
            
            Query: {query}
            
            Use the tools available to retrieve information and provide a precise response.
            {agent_scratchpad}
            """,
            input_variables=["query", "agent_scratchpad"]
        )
        
        # For direct usage without tools, use this simplified approach
        if query.lower().strip() in ["summary", "overview", "help"]:
            formatted_prompt = prompt.format(
                query=query,
                agent_scratchpad=""
            )
            response = self.llm.invoke(formatted_prompt)
            # Strip the original prompt if it's in the response
            if formatted_prompt in response:
                response = response.replace(formatted_prompt, "").strip()
            return response
        
        # For more complex queries, use the agent approach
        try:
            # Create the agent using Ollama for LangChain compatibility
            agent_executor = AgentExecutor.from_agent_and_tools(
                agent=self.llm,
                tools=tools,
                verbose=True
            )
            
            result = agent_executor.run(query)
            return result
        except Exception as e:
            # Fallback if agent execution fails
            print(f"Agent execution failed: {e}")
            formatted_prompt = f"""
            You are a Project Manager. Please provide a general response to this query 
            without using external tools: {query}
            """
            response = self.llm.invoke(formatted_prompt)
            if formatted_prompt in response:
                response = response.replace(formatted_prompt, "").strip()
            return f"I had some difficulty processing that with my tools, but here's what I can tell you:\n\n{response}"
    
    def _retrieve_user_stories(self):
        """Retrieve all user stories from the database."""
        user_stories = self.db_manager.retrieve_artifacts_by_type("user_story")
        return json.dumps(user_stories, indent=2)
    
    def _retrieve_code(self):
        """Retrieve all code artifacts from the database."""
        code_artifacts = self.db_manager.retrieve_artifacts_by_type("code")
        return json.dumps(code_artifacts, indent=2)
    
    def _retrieve_test_cases(self):
        """Retrieve all test cases from the database."""
        test_cases = self.db_manager.retrieve_artifacts_by_type("test_case")
        return json.dumps(test_cases, indent=2)
    
    def _retrieve_test_results(self):
        """Retrieve test execution results from the database."""
        test_results = self.db_manager.retrieve_artifacts_by_type("test_results")
        return json.dumps(test_results, indent=2)
    
    def _search_artifacts(self, query):
        """Search for artifacts based on query."""
        artifacts = self.db_manager.search_artifacts(query)
        return json.dumps(artifacts, indent=2)