# Autogen 0.2
from autogen import AssitantAgent
import check_robot_status, get_position

llm_config = {
    "config_list": [
        {
            "api_type": "groq",
            "model": "llama3-8b-8192",
            "api_key": "",
        }
    ]
}

agent2 = AssitantAgent(
    name = "Assistant",
    llm_config = llm_config,
    function_map = {"check_robot_status": check_robot_status,
                    "get_position": get_position}
)

agent2.generate_reply(
    messages = [{"role": "user/assistant", "content": "Padoru padoru"}],
    sender = None
)

# --------------------------------------------------------------

# Autogen 0.4
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage

model_client = OpenAIChatCompletionClient(
    # fill config here
)

agent4 = AssitantAgent(
    name="Assistant",
    model_client = model_client,
    tools = [check_robot_status, get_position]
)

agent4.on_message([TextMessage(content="Padoru padoru", source="user")])

# more examples: 
# 0.2: https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/conversable_agent#generate_reply
# 0,4: https://microsoft.github.io/autogen/0.4.0.dev11/reference/python/autogen_agentchat.agents.html#autogen_agentchat.agents.AssistantAgent
