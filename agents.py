from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url
from dotenv import load_dotenv

load_dotenv()

#model setup
llm=init_chat_model("openai/gpt-oss-120b",model_provider="groq")


#1st agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

#2nd agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


#writer chain
writer_prompt=ChatPromptTemplate.from_messages([
    ("system","You are an expert research writer.Write clear,structured and insightful report"),
    ("human","""Write a detailed research report on the topic below.messages
Topic:{topic}

Research Gathered:
{research}

Structure the report as:
-Introduction
-Key Findings (minimum 3 well-explained points)
-Conclusion
-Sources(list all URLs found in the research

Be detailed,factual and professional,"""),])

writer_chain=writer_prompt | llm | StrOutputParser()

#critic chain

critic_prompt=ChatPromptTemplate.from_messages([
    ("system","You are a sharp and constructive research critic.Be honest and specific,"),
    ("human","""Review the research report below and evaluate it stritly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:

-...
-...

Areas to Improve:
-...
-...

One line verdict
...""")
])

critic_chain=critic_prompt | llm | StrOutputParser()

response=llm.invoke("Write a short paragraph")
result=writer_chain.invoke({
    "topic":"what was the impact of iran israil war on india",
    "research":"India may face energy price fluctuations.Source: https://example.com"
})
result2=critic_chain.invoke({
    "report":"India may face energy price fluctuations due to geographical tensions"
})
print(result2)