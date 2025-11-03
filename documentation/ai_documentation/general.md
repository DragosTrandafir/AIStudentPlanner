Flow overview

1️⃣ Backend sends user data → AI Orchestrator

2️⃣ Orchestrator queries LangChain memory for last plan + feedback. It has also the user data at every iteration

3️⃣ Orchestrator calls each agent (parallel)

4️⃣ Agents generate JSON plan proposals

5️⃣ Orchestrator merges all into final plan

6️⃣ Saves plan in memory + backend

7️⃣ Frontend displays plan

8️⃣ When feedback is sent → refresh cycle (steps 2–6 again)