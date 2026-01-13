# Frontend Flow Overview

-------- Application Initialization --------

1️⃣ User accesses the Next.js application URL

2️⃣ Frontend checks for stored JWT token in localStorage

3️⃣ If token exists:
- Validates token expiration
- Loads user profile and redirects to main dashboard

4️⃣ If no token or invalid:
- Redirects to login page

-------- User Authentication --------

1️⃣ User enters credentials on login/register page

2️⃣ Frontend sends POST request to `/api/auth/login` or `/api/auth/register`

3️⃣ Backend validates credentials and returns JWT token

4️⃣ Frontend stores token in localStorage and user data in context

5️⃣ Redirects to main calendar dashboard

-------- Dashboard Loading --------

1️⃣ Frontend fetches user subjects via GET `/api/subjects`

2️⃣ Fetches existing plans/tasks via GET `/api/plans` and `/api/ai-tasks`

3️⃣ Initializes FullCalendar with user's timezone and preferences

4️⃣ Renders calendar view with existing tasks color-coded by type

-------- Subject Management --------

1️⃣ User clicks "Add Subject" button in sidebar

2️⃣ Opens subject creation modal with form fields (name, exam date, etc.)

3️⃣ User submits form -> Frontend validates input

4️⃣ POST request to `/api/subjects` with subject data

5️⃣ Backend creates subject record and returns success

6️⃣ Frontend refreshes subjects list and updates calendar

-------- AI Plan Generation --------

1️⃣ User clicks "Generate Plan" button

2️⃣ Opens plan generation modal with subject selection

3️⃣ User selects subjects and submits

4️⃣ POST request to `/api/plans/generate` with selected subjects

5️⃣ Backend processes through AI system and returns generated plan

6️⃣ Frontend receives plan data and renders new tasks on calendar

7️⃣ Updates local state with new generation_id

-------- Task Interaction --------

1️⃣ User clicks on calendar event/task

2️⃣ Opens task details modal with task information

3️⃣ User can:
- Mark task as complete/incomplete
- Edit task details
- Delete task

4️⃣ Changes trigger PUT/DELETE requests to `/api/ai-tasks/{id}`

5️⃣ Backend updates database and returns success

6️⃣ Frontend refreshes calendar view

-------- Feedback Submission --------

1️⃣ User clicks "Provide Feedback" button

2️⃣ Opens feedback modal with rating (1-5) and comments

3️⃣ User submits feedback

4️⃣ POST request to `/api/feedback` with rating and comments

5️⃣ Backend stores feedback linked to current generation_id

-------- Plan Rescheduling --------

1️⃣ User clicks "Reschedule Plan" button

2️⃣ Opens reschedule modal (optionally with feedback prompt)

3️⃣ User submits reschedule request

4️⃣ POST request to `/api/plans/reschedule`

5️⃣ Backend processes through AI rescheduler with feedback context

6️⃣ Returns refined plan with new generation_id

7️⃣ Frontend updates calendar with rescheduled tasks

-------- Theme Management --------

1️⃣ User toggles theme switch in sidebar

2️⃣ Frontend updates CSS variables and localStorage

3️⃣ Applies dark/light theme classes to document root

4️⃣ Persists theme preference across sessions

-------- Error Handling --------

1️⃣ API requests include error handling for:
- Network failures (retry logic)
- Authentication errors (redirect to login)
- Validation errors (display field-specific messages)
- Server errors (generic error modals)

2️⃣ User-friendly error messages displayed in modals/toasts

-------- State Management --------

- **Authentication State**: Managed via React Context (user profile, token)
- **Theme State**: Global theme provider with localStorage persistence
- **Calendar State**: FullCalendar instance with event data
- **Modal State**: Individual component state for modal visibility

-------- API Integration Details --------

All API calls use:
- JWT token in Authorization header
- JSON content-type
- Consistent error response handling
- Loading states during requests

See `api/` folder for endpoint-specific implementations and `utils/apiUtils.ts` for shared API logic.