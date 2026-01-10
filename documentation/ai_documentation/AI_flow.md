AI Flow overview

-------- Initial : generate the first schedule --------

1️⃣ Backend sends user data (all exam and projects) -> AI Orchestrator

2️⃣ AI Orchestrator: 
- selects an appropriate agent for each subject
- calls each agent (parallel)
- all the agent results are concatenated 
- the Orchestrator organizes the concatenation in a final, optimized schedule

-------- Feedback (this usually happens after generating the initial schedule) --------

1️⃣ Backend sends updated user data: 
- last feedback (if any)
- last generated plan 
- current input feedback the user gives

2️⃣ AI Rescheduler takes the now broader context from 1) and just makes smaller or bigger changes to the previous generated schedule

The model we chose for all agents and mini-agents is openai/gpt-oss-20b, as it does not require high HuggingFace inference use (such as Qwen), is fast, and although the prompt has to be shorter (it does not have such a large context windows as Qwen), can be easier to convince and prompt engineering in special cases works better, when working with it.


