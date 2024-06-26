

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import ShellTool
import warnings
warnings.filterwarnings('ignore')

tools = [ShellTool()]
llm = ChatOpenAI(base_url="http://127.0.0.1:8080/v1")

template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)




# Use with chat history
result = agent_executor.invoke(
    {
        "input": "Please list all files and directories in current path ?",
        "chat_history": ""
    })

print(result['output'])
