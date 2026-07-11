from llm import LLMManager

llm = LLMManager().load_model("Gemini")

response = llm.invoke("Say Hello!")

print(response.content)
llm_manager = LLMManager()


def get_llm(model_name):
    return llm_manager.load_model(model_name)