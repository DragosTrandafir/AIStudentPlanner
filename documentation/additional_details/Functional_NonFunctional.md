## 2. User-Oriented Specifications

### 2.1 Functional Requirements
The application provides the following core functionalities:
* **Academic Profiling:** Users can input subjects, project descriptions, and exam dates.
* **AI-Driven Scheduling:** Generates a personalized study roadmap using multi-agent negotiation based on task difficulty.
* **Interactive Dashboard:** A web-based calendar to visualize study sessions and deadlines.
* **Adaptive Feedback Loop:** Users can report progress (e.g., "Task completed" or "Task missed").

### 2.2 Use Case Scenarios
1.  **The "High-Pressure" Scenario:** A student has two exams on the same day. The AI agents for both subjects negotiate with the Coordinator Agent to distribute study hours over the previous two weeks, prioritizing the subject with higher difficulty.
2.  **The "Life Happens" Scenario:** A student misses a planned study block on a Tuesday. By providing feedback to the AI, the system automatically redistributes the missed topics into the remaining days of the week without overloading the student.

### 2.3 Non-Functional Requirements (Quality & Constraints)

The following requirements define the operational standards and quality attributes of the system:

* **Performance & Latency:** The AI Coordinator must process agent negotiations and generate a full weekly schedule in under 10 seconds to maintain a seamless user experience.
* **Reliability & Accuracy:** The adaptation logic must ensure zero overlap between study sessions. AI agents must treat deadlines as "hard constraints" to ensure no exam preparation is overlooked.
* **Scalability:** The backend architecture must be capable of orchestrating multiple concurrent LangChain agent instances as users increase their subject load or project complexity.
* **Usability:** The UI must follow a "low-friction" design philosophy, ensuring that core actions—such as providing feedback (e.g., "Task not finished")—can be completed in two clicks or less.
* **Data Persistence:** All user-defined preferences, subject parameters, and AI-generated schedules must be stored securely in a persistent database, ensuring zero data loss across user sessions.
