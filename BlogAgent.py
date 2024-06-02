# Warning control
import warnings
warnings.filterwarnings('ignore')

import markdown2
from crewai import Agent, Task, Crew
from IPython.display import Markdown
import os
from utils import get_openai_api_key

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

# Define the Content Planner agent
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article about the topic: {topic}. "
              "You collect information that helps the audience learn something new "
              "and make informed decisions. Your work forms the basis for the Content Writer "
              "to write an insightful and accurate article on this topic.",
    allow_delegation=False,
    verbose=True
)

# Define the Content Writer agent
writer = Agent(
    role="Content Writer",
    goal="Write an insightful and factually accurate opinion piece about the topic: {topic}",
    backstory="You're tasked with writing a new opinion piece about the topic: {topic}. "
              "Your writing is based on the detailed outline and context provided by the Content Planner. "
              "Follow the main objectives and direction of the outline, incorporating suggestions: {specifications}. "
              "Provide objective and impartial insights backed by information from the Content Planner, "
              "clearly distinguishing between opinions and objective statements.",
    allow_delegation=False,
    verbose=True
)

# Define the Editor agent
editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with the writing style of the organization.",
    backstory="You are an editor who receives a blog post from the Content Writer. "
              "Your goal is to review the blog post to ensure it follows journalistic best practices, "
              "provides balanced viewpoints, and avoids major controversial topics or opinions when possible. "
              "Ensure the content is aligned with the brand's voice and is catered to the target audience.",
    allow_delegation=False,
    verbose=True
)

# Define the planning task
plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering their interests and pain points.\n"
        "3. Develop a detailed content outline including an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources.\n"
        "5. Plan the content to be written in a {tone} tone.\n"
        "6. Ensure the content caters to the specified audience: {audience}.\n"
        "7. Make sure to focus on: {specifications}.\n"
    ),
    expected_output="A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources.",
    agent=planner,
)

# Define the writing task
write = Task(
    description=(
        "1. Use the content plan to craft a compelling blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
        "3. Name sections/subtitles in an engaging manner.\n"
        "4. Structure the post with an engaging introduction, insightful body, and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and alignment with the brand's voice.\n"
        "6. Ensure the word limit is strictly adhered to: {word_limit} words.\n"
        "7. Write the blog in a {tone} tone.\n"
        "8. Ensure the content caters to the specified audience: {audience}.\n"
        "9. Make sure to focus on: {specifications}.\n"
    ),
    expected_output="A well-written blog post in markdown format, ready for publication, with each section having 2 or 3 paragraphs.",
    agent=writer,
)

# Define the editing task
edit = Task(
    description=(
        "1. Proofread the given blog post for grammatical errors and alignment with the brand's voice.\n"
        "2. Ensure the content caters to the specified audience: {audience}.\n"
        "3. Verify the word limit is adhered to: {word_limit} words.\n"
        "4. Make sure to focus on: {specifications}.\n"
    ),
    expected_output="A well-edited blog post in markdown format, ready for publication, with each section having 2 or 3 paragraphs.",
    agent=editor
)

# Set up the Crew
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)

# Function to generate a blog post
def blog_writer(blog_topic, audience, tone, word_limit, specifications):
    result = crew.kickoff(inputs={"topic": blog_topic, "audience": audience, "tone": tone, "word_limit": word_limit, "specifications": specifications})
    formatted_result = markdown2.markdown(result)  # Convert the result to Markdown format
    return formatted_result
