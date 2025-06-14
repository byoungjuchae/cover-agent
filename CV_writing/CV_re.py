from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
<<<<<<< HEAD
from langchain_google_genai import ChatGoogleGenerativeAI
=======
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
from langchain.document_loaders import PyPDFLoader
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()
API = os.getenv('OPENAI_KEY')
llm = ChatOpenAI(model='gpt-4.1-mini',openai_api_key= API)


class State(BaseModel):

        jd: str = Field(description='it is the jd information')
        cv : str = Field(description='it is the CV file')
        JD_analysis : str  = Field(default='',description='it is the CV file')
        cv_re : str = Field(default='',description='it is the CV file')
        final_response : str = Field(default='',description='it is the CV file')



<<<<<<< HEAD

=======
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
def JD(state:State):
    prompt_text = """You are a recruiter. you have to find the important keywords about JD.

    Here is the JD:
<<<<<<< HEAD
    {Jobdescription}

    """
    prompt = ChatPromptTemplate.from_template(prompt_text)
    chain = {"JD":RunnablePassthrough()} | prompt | llm | StrOutputParser()

    response = chain.invoke({"JD":state.jd})

=======
    {JD}

    """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    chain = {"JD":RunnablePassthrough()} | prompt | llm | StrOutputParser()

    response = chain.invoke({"JD":state.jd})
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
    state.JD_analysis =  response

    return state


def CV_Re(state:State):
    prompt_text = """ You are a writer about CV resume. you have to avoid the ATS with rewriting the CV.

                you have to rewrite the CV refer to the CV and JD analysis. 
                CV must have the keywords about the JD and maintain the base CV information and format.

                Here is the JD analysis:
                {JD_analysis}

                Here is the CV:
<<<<<<< HEAD
                {resume} 
=======
                {CV} 
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
    """

    prompt = ChatPromptTemplate.from_template(prompt_text)

<<<<<<< HEAD
    chain = {"JD_analysis":RunnablePassthrough(),"resume":RunnablePassthrough()} | prompt | llm | StrOutputParser()
=======
    chain = {"JD_analysis":RunnablePassthrough(),"CV":RunnablePassthrough()} | prompt | llm | StrOutputParser()

>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1

    response = chain.invoke({'JD_analysis':state.JD_analysis,"CV":state.cv})

    state.cv_re = response 

    return state


def Write_it_Latex(state:State):

        prompt_text = """ You are a writer about CV resume. you have to avoid the ATS with rewriting the CV.

                You have to write it through the pylatex code.

                Here is the CV:
<<<<<<< HEAD
                {cv} 
=======
                {CV} 
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
        """
        prompt = ChatPromptTemplate.from_template(prompt_text)

        chain = {"CV":RunnablePassthrough()} | prompt | llm | StrOutputParser()

        response = chain.invoke({"CV":state.cv_re})

        state.final_response = response
        return state


graph_state = StateGraph(State)
graph_state.add_node("JDs",JD)
graph_state.add_node("CVs",CV_Re)
graph_state.add_node("Write_it",Write_it_Latex)

graph_state.add_edge("JDs","CVs")
graph_state.add_edge("CVs","Write_it")
graph_state.set_entry_point("JDs")
graph = graph_state.compile()
<<<<<<< HEAD
<<<<<<< HEAD


def cv_rewriting(thread_id:str):

    docs = PyPDFLoader('./pdf/CV.pdf').load()
=======


def cv_rewriting(thread_id:str):
    docs = PyPDFLoader('./CV.pdf').load()
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1

    sd = "ResponsibilitiesByteDance Server platform team is responsible for architecting, designing and building best server and storage system to meet the requirements of high-performance, low cost and easy to operate. By joining this team, you will work with the best engineers and talents in this industry and have a broad opportunity to get in touch with the latest AI application system and newly emerged technology in computing, storage and silicon validation. You will gain remarkable hardware architect, development and validation experiences in most advanced hardware infrastructure at massive scale.We are looking for a self-motivated Cloud hardware system architect. As a system architect, your responsibilities will include: Track new technology from industry and partner vendors, work with hardware architects and cloud product experts closely on computing and storage solutions for Bytedance cloud products and all other application teams. Workout hardware solutions for cloud products, including computing, storage, database, bigdata, edge computing etc., based on deep analysis of cloud product design and operational data. Work closely with cloud product and r&amp;d team or performance and cost optimization. Work with industry consortiums and standard committees to investigate the emerging standards or technologies, and contribute our research results to the industry. Work with our technology partners and suppliers to setup PoC or prototypes to evaluate and test the new technologies or architectural designs. International travel requirement: up to four times per year, including but not limited to China, Europe, and South Asia. Candidates must have a valid passport and be able to obtain the necessary visas.QualificationsMinimum Qualifications Master’s degree or higher in Electrical Engineering, Computer Engineering, Computer Science or related majors. Experienced in hardware/software performance and power optimization is preferred. Deep understanding of computer system architecture. Demonstrated knowledge of the design principles and applications of CPU, memory, SSD, and network parts. Understand the implementation of virtualization technology, database, distributed storage system, and deep learning architecture. Demonstrated experience in working collaboratively in cross-functional teams.Preferred Qualifications 3 years of experience in Circuit Board Design, System debugging, Power/Signal Integrity, and Thermal solutions. 3 years experience in server or storage system architecture design or software-hardware co-design.Job Information【For Pay Transparency】Compensation Description (Annually)The base salary range for this position in the selected city is $194000 - $410000 annually.Compensation may vary outside of this range depending on a number of factors, including a candidate’s qualifications, skills, competencies and experience, and location. Base pay is one part of the Total Package that is provided to compensate and recognize employees for their work, and this role may be eligible for additional discretionary bonuses/incentives, and restricted stock units.Benefits may vary depending on the nature of employment and the country work location. Employees have day one access to medical, dental, and vision insurance, a 401(k) savings plan with company match, paid parental leave, short-term and long-term disability coverage, life insurance, wellbeing benefits, among others. Employees also receive 10 paid holidays per year, 10 paid sick days per year and 17 days of Paid Personal Time (prorated upon hire with increasing accruals by tenure).The Company reserves the right to modify or change these benefits programs at any time, with or without notice.For Los Angeles County (unincorporated) CandidatesQualified applicants with arrest or conviction records will be considered for employment in accordance with all federal, state, and local laws including the Los Angeles County Fair Chance Ordinance for Employers and the California Fair Chance Act. Our company believes that criminal history may have a direct, adverse and negative relationship on the following job duties, potentially resulting in the withdrawal of the conditional offer of employment: Interacting and occasionally having unsupervised contact with internal/external clients and/or colleagues; Appropriately handling and managing confidential information including proprietary and trade secret information and access to information technology systems; and Exercising sound judgment.About TikTokTikTok is the leading destination for short-form mobile video. At TikTok, our mission is to inspire creativity and bring joy. TikTok's global headquarters are in Los Angeles and Singapore, and we also have offices in New York City, London, Dublin, Paris, Berlin, Dubai, Jakarta, Seoul, and Tokyo.Why Join UsInspiring creativity is at the core of TikTok's mission. Our innovative product is built to help people authentically express themselves, discover and connect – and our global, diverse teams make that possible. Together, we create value for our communities, inspire creativity and bring joy - a mission we work towards every day.We strive to do great things with great people. We lead with curiosity, humility, and a desire to make impact in a rapidly growing tech company. Every challenge is an opportunity to learn and innovate as one team. We're resilient and embrace challenges as they come. By constantly iterating and fostering an \"Always Day 1\" mindset, we achieve meaningful breakthroughs for ourselves, our company, and our users. When we create and grow together, the possibilities are limitless. Join us.Diversity &amp; InclusionTikTok is committed to creating an inclusive space where employees are valued for their skills, experiences, and unique perspectives. Our platform connects people from across the globe and so does our workplace. At TikTok, our mission is to inspire creativity and bring joy. To achieve that goal, we are committed to celebrating our diverse voices and to creating an environment that reflects the many communities we reach. We are passionate about this and hope you are too.TikTok AccommodationTikTok is committed to providing reasonable accommodations in our recruitment processes for candidates with disabilities, pregnancy, sincerely held religious beliefs or other reasons protected by applicable laws. If you need assistance or a reasonable accommodation, please reach out to us at https://tinyurl.com/RA-request"
    state = State(cv=docs[0].page_content,jd=sd)

    base_folder = f'./process/{thread_id}'
    resp = graph.invoke(state)
    os.makedirs(base_folder,exist_ok=True)

    with open(os.path.join(base_folder,'abc.py'),'w',encoding='utf-8') as f:
        f.write(resp['final_response'])

<<<<<<< HEAD
cv_rewriting('5')

docs = PyPDFLoader('./pdf/CV.pdf').load()
JD = "ResponsibilitiesByteDance Server platform team is responsible for architecting, designing and building best server and storage system to meet the requirements of high-performance, low cost and easy to operate. By joining this team, you will work with the best engineers and talents in this industry and have a broad opportunity to get in touch with the latest AI application system and newly emerged technology in computing, storage and silicon validation. You will gain remarkable hardware architect, development and validation experiences in most advanced hardware infrastructure at massive scale.We are looking for a self-motivated Cloud hardware system architect. As a system architect, your responsibilities will include: Track new technology from industry and partner vendors, work with hardware architects and cloud product experts closely on computing and storage solutions for Bytedance cloud products and all other application teams. Workout hardware solutions for cloud products, including computing, storage, database, bigdata, edge computing etc., based on deep analysis of cloud product design and operational data. Work closely with cloud product and r&amp;d team or performance and cost optimization. Work with industry consortiums and standard committees to investigate the emerging standards or technologies, and contribute our research results to the industry. Work with our technology partners and suppliers to setup PoC or prototypes to evaluate and test the new technologies or architectural designs. International travel requirement: up to four times per year, including but not limited to China, Europe, and South Asia. Candidates must have a valid passport and be able to obtain the necessary visas.QualificationsMinimum Qualifications Master’s degree or higher in Electrical Engineering, Computer Engineering, Computer Science or related majors. Experienced in hardware/software performance and power optimization is preferred. Deep understanding of computer system architecture. Demonstrated knowledge of the design principles and applications of CPU, memory, SSD, and network parts. Understand the implementation of virtualization technology, database, distributed storage system, and deep learning architecture. Demonstrated experience in working collaboratively in cross-functional teams.Preferred Qualifications 3 years of experience in Circuit Board Design, System debugging, Power/Signal Integrity, and Thermal solutions. 3 years experience in server or storage system architecture design or software-hardware co-design.Job Information【For Pay Transparency】Compensation Description (Annually)The base salary range for this position in the selected city is $194000 - $410000 annually.Compensation may vary outside of this range depending on a number of factors, including a candidate’s qualifications, skills, competencies and experience, and location. Base pay is one part of the Total Package that is provided to compensate and recognize employees for their work, and this role may be eligible for additional discretionary bonuses/incentives, and restricted stock units.Benefits may vary depending on the nature of employment and the country work location. Employees have day one access to medical, dental, and vision insurance, a 401(k) savings plan with company match, paid parental leave, short-term and long-term disability coverage, life insurance, wellbeing benefits, among others. Employees also receive 10 paid holidays per year, 10 paid sick days per year and 17 days of Paid Personal Time (prorated upon hire with increasing accruals by tenure).The Company reserves the right to modify or change these benefits programs at any time, with or without notice.For Los Angeles County (unincorporated) CandidatesQualified applicants with arrest or conviction records will be considered for employment in accordance with all federal, state, and local laws including the Los Angeles County Fair Chance Ordinance for Employers and the California Fair Chance Act. Our company believes that criminal history may have a direct, adverse and negative relationship on the following job duties, potentially resulting in the withdrawal of the conditional offer of employment: Interacting and occasionally having unsupervised contact with internal/external clients and/or colleagues; Appropriately handling and managing confidential information including proprietary and trade secret information and access to information technology systems; and Exercising sound judgment.About TikTokTikTok is the leading destination for short-form mobile video. At TikTok, our mission is to inspire creativity and bring joy. TikTok's global headquarters are in Los Angeles and Singapore, and we also have offices in New York City, London, Dublin, Paris, Berlin, Dubai, Jakarta, Seoul, and Tokyo.Why Join UsInspiring creativity is at the core of TikTok's mission. Our innovative product is built to help people authentically express themselves, discover and connect – and our global, diverse teams make that possible. Together, we create value for our communities, inspire creativity and bring joy - a mission we work towards every day.We strive to do great things with great people. We lead with curiosity, humility, and a desire to make impact in a rapidly growing tech company. Every challenge is an opportunity to learn and innovate as one team. We're resilient and embrace challenges as they come. By constantly iterating and fostering an \"Always Day 1\" mindset, we achieve meaningful breakthroughs for ourselves, our company, and our users. When we create and grow together, the possibilities are limitless. Join us.Diversity &amp; InclusionTikTok is committed to creating an inclusive space where employees are valued for their skills, experiences, and unique perspectives. Our platform connects people from across the globe and so does our workplace. At TikTok, our mission is to inspire creativity and bring joy. To achieve that goal, we are committed to celebrating our diverse voices and to creating an environment that reflects the many communities we reach. We are passionate about this and hope you are too.TikTok AccommodationTikTok is committed to providing reasonable accommodations in our recruitment processes for candidates with disabilities, pregnancy, sincerely held religious beliefs or other reasons protected by applicable laws. If you need assistance or a reasonable accommodation, please reach out to us at https://tinyurl.com/RA-request"

def cv_write():
    state = State(cv=docs[0].page_content,jd=JD)
    resp = graph.invoke(state)
=======
cv_rewriting('5')
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
