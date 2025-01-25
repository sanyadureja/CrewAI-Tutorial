from dotenv import load_dotenv
from crewai import Crew
from tasks import MeetingPrepTasks
from agents import MeetingPrepAgents


def main():
    load_dotenv()

    # User Inputs (Custom)
    print("## Welcome to the Meeting Prep Crew")
    print('-------------------------------')
    meeting_participants = input("What are the emails for the participants (other than you) in the meeting?\n")
    meeting_context = input("What is the context of the meeting?\n")
    meeting_objective = input("What is your objective for this meeting?\n")

    # Initialize Tasks and Agents
    tasks=MeetingPrepTasks()
    agents=MeetingPrepAgents()

    # Create agents
    research_agent=agents.research_agent()
    industry_analysis_agent = agents.industry_analysis_agent()
    meeting_strategy_agent = agents.meeting_strategy_agent()
    summary_and_briefing_agent = agents.summary_and_briefing_agent()

    # Create Tasks
    research_task=tasks.research_task(research_agent, meeting_participants, meeting_context)
    industry_analysis_task = tasks.industry_analysis_task(industry_analysis_agent, meeting_participants, meeting_context)
    meeting_strategy_task = tasks.meeting_strategy_task(meeting_strategy_agent, meeting_context, meeting_objective)
    summary_and_briefing_task = tasks.summary_and_briefing_task(summary_and_briefing_agent, meeting_context, meeting_objective)

    # Context (O/p -> I/p)
    meeting_strategy_task.context = [research_task, industry_analysis_task]
    summary_and_briefing_task.context = [research_task, industry_analysis_task, meeting_strategy_task]

    # Crew
    crew = Crew(
      agents=[
        research_agent,
        industry_analysis_agent,
        meeting_strategy_agent,
        summary_and_briefing_agent
      ],
      tasks=[
        research_task,
        industry_analysis_task,
        meeting_strategy_task,
        summary_and_briefing_task
      ]
      #process=   (sequential by default)
    )

    result = crew.kickoff()
    print(result)

if __name__=="__main__":
    main()

# CrewAI by default works with GPT-4