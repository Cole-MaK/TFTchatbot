from google.genai.types import GenerateContentConfig

class GenerateContent:
    def __init__(self, client, model, tools, system):
        self.client = client
        self.model = model
        self.tools = tools
        self.system = system
    
    def generate(self, contents):
        config = GenerateContentConfig(
            system_instruction = self.system,
            tools = self.tools)
        
        response = self.client.models.generate_content(
            model = self.model,
            contents = contents,
            config = config
        )
        
        return response