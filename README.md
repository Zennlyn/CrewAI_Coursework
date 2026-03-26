# AgentSociety
This course work was completed for the elective course **Large Language Models and Applications**, where I implemented a **static baseline system** using [CrewAI](https://crewai.com/), a multi-agent orchestration framework. 

The system operates on subsets of the Yelp dataset, which contain the characteristics of the most active users along with their ratings and reviews for various businesses (see more details [here](https://github.com/Zennlyn/CrewAI_Coursework/blob/main/knowledge/Yelp%20Data%20Translation.pdf)). 

## Objective
Given two inputs: `user_id` and `item_id`, which sampled from `test_review_subset.json`, the system predicts:
* a star rating (`stars`)
* a natural language review (`text`)

that the user would likely assign to the specified business.

## Implementation Details
This coursework implements **Retrieval-Augmented Generation (RAG)** system is implemented to enable agents to incorporate external knowledge during reasoning and predicting. Additionally, **knowledge scoping** is applied at both the agent and crew levels to control information visibility for each agent: either restricted to individual agents or shared across the entire crew (all agents). There are three agents handling different task in this system:
* `user_profiler`: It acts as consumer behavior analyst which gives an accurate and structured profile of the user's preferences (e.g., dining preferences, behavioral patterns, etc.). This agent is granted permission to query the user database (`user_subset.json`), and the review database (`review_subset.json`).
* `item_analyst`: It acts as restaurant intelligence analyst which extracts and summarize the most relevant attributes of a restaurant, including signature dishes, common customer complants, etc. This agent is granted permission to query the business/entity database (`item_subset.json`).
* `prediction_modeler`: This agent is responsible for generating the final output, which are the predicted rating and synthesized review the customer would likely give, given the reports provided by the first two agents.

A shared knowledge describing the details of each key field in the database is made accessible to all agents by assigning it to the crew-level `knowledge_sources`.

## Output Example
```
{
  "stars": 4.5,
  "text": "I had a great experience at this restaurant. The service was top-notch, the menu variety was impressive, and the ambiance was cozy and inviting. The prices were reasonable, and the food was delicious. I would highly recommend this place to anyone looking for a great dining experience."
}
```
