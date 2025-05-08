from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key= API)


def CV_Re(state:State):
    prompt_text = """ You are a writer about CV resume. you have to avoid the ATS with rewriting the CV.

                you have to rewrite the CV refer to the CV and JD analysis. 
                CV must have the keywords about the JD and maintain the base CV information and format.

                Here is the JD analysis:
                {JD_analysis}

                Here is the CV:
                {CV} 
    """

    prompt = ChatPromptTemplate.from_template(prompt_text)

    chain = {"JD_analysis":RunnablePassthrough(),"CV":RunnablePassthrough()} | prompt | llm | StrOutputParser()


    response = chain.invoke({'JD_analysis':state.JD_analysis,"CV":state.CV})

    state.cv_re = response 

    return state


def Write_it_Latex(state:State):

        prompt_text = """ You are a writer about CV resume. you have to avoid the ATS with rewriting the CV.

                You have to write it through the pylatex code.

                Here is the CV:
                {CV} 
        """
        prompt = ChatPromptTemplate.from_template(prompt_text)

        chain = {"CV":RunnablePassthrough()} | prompt | llm | StrOutputParser()

        response = chain.invoke({"CV":state.cv_re})



graph_state = StateGraph(State)
graph_state.add_node("CV",CV_Re)
graph_state.add_node("Write_it",Write_it_Latex)

graph
import pdb
pdb.set_trace()