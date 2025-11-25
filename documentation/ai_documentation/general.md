Flow overview

1️⃣ Backend sends user data → AI Orchestrator TODO

2️⃣ Orchestrator queries LangChain memory for last plan + feedback. It has also the user data at every iteration * TODO

3️⃣ Orchestrator calls each agent (parallel) DONE

4️⃣ Agents generate JSON plan proposals DONE

5️⃣ Orchestrator merges all into final plan DONE

6️⃣ Saves plan in memory + backend TODO

7️⃣ Frontend displays plan TODO

8️⃣ When feedback is sent → refresh cycle (steps 2–6 again) TODO

* The feedback should be got from the frontend, through a backend api, the user data can also be taken either from the backend API(keep the preferences of the user in the database maybe for later modifications of the app and scalability), or kept (the last version) in the langchain memory, and the plans also, keep both in the database (for later integration with Google Calendar and in lcmemory for speed