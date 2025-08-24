from .plan import planner_graph
from .analyze import analyze_resume, analyze_JD, analyze_portfolio
from .writing import write_coverletter, rewrite_cv
from .llm_type import llm
from .recommend import JD_recommendation_system
from .util.total_state import SwarmState
from langgraph_swarm import create_swarm, create_handoff_tool
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import InMemorySaver



analyze_llm = create_react_agent(llm,
                                tools=[analyze_resume,analyze_JD, analyze_portfolio,create_handoff_tool(agent_name='writing_agent',description='transfer to writing agent,it can help your writing')],
                                prompt="""You are a agent. you have to analyze the CV, JD or portfolio analysis.
                                        If you want to analyze the CV, JD or portfolio analysis, you use the analyze_resume, analyze_JD, analyze_portfolio tool.""",
                                name="analyze_agent")
writing_llm = create_react_agent(llm,
                                tools =[write_coverletter,rewrite_cv,create_handoff_tool(agent_name='analyze_agent',description='transfer to analyze agent, it can help your analyzing')],
                                prompt="""You are a writer agent. if you write a cover letter based on the CV and JD analysis, you use the writer tool.""",
                                name="writing_agent")

workflow_graph = create_swarm(
    [analyze_llm,writing_llm],
    default_active_agent="analyze_agent"
)

workflow_compile = workflow_graph.compile()


checkpointer = InMemorySaver()
graph_build = StateGraph(SwarmState)
graph_build.add_node("planner_graph",planner_graph)
graph_build.add_node("workflow_compile",workflow_compile)
graph_build.add_edge("planner_graph","workflow_compile")
graph_build.set_entry_point("planner_graph")
graph_total = graph_build.compile()
