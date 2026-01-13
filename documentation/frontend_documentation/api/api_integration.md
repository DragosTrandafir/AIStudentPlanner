# API Integration

## Backend Communication

The frontend communicates with a FastAPI backend running on `http://localhost:8000`. All API calls use REST endpoints with JSON payloads.

## Authentication

### Headers
All authenticated requests include:
```typescript
{
  "Authorization": `Bearer ${token}`,
  "Content-Type": "application/json"
}
```

### User Management
- `getCurrentUserId()`: Retrieves stored user ID
- `getAuthHeaders()`: Generates authentication headers

## API Modules

### apiSubjects.ts
Handles subject-related operations:

**Functions:**
- `getSubjects()`: Fetch all user subjects
- `createSubject(subject)`: Create new subject
- `updateSubject(id, subject)`: Update existing subject
- `deleteSubject(id)`: Delete subject

**Subject Interface:**
```typescript
interface Subject {
  id: number;
  name: string;
  description?: string;
  color?: string;
  user_id: number;
}
```

### apiPlans.ts
Manages AI plan generation and scheduling:

**Key Functions:**
- `generatePlan()`: Generate new AI study plan
- `reschedulePlan(feedback)`: Reschedule based on user feedback
- `getLatestSchedule()`: Fetch most recent AI schedule
- `getPlans()`: Get all user plans
- `deleteAiTask(id)`: Remove AI-generated task
- `submitFeedback(planId, feedback)`: Submit feedback for plan

**Data Structures:**
```typescript
interface AITaskEntry {
  id?: number;
  time_allotted: string;
  ai_task_name: string;
  task_name: string;
  difficulty: number;
  priority: number;
}

interface PlanResponse {
  id?: number;
  plan_date: string;
  entries: AITaskEntry[];
  notes: string | null;
  generation_id?: string;
}

interface GeneratedPlanResponse {
  plans: PlanResponse[];
  message: string;
}
```

## Data Mapping

### Task Mapping
Frontend uses a unified `Task` interface for both manual and AI-generated tasks:

**Manual Tasks (Subjects):**
- Mapped via `mapSubjectToTask()` in `subjectMapper.ts`
- Converts Subject objects to Task format

**AI Tasks:**
- Mapped via `mapPlansToTasks()` in `aiTaskMapper.ts`
- Converts PlanResponse entries to Task objects

### Task Interface
```typescript
interface Task {
  id: number;
  title: string;
  subject?: string;
  type: TaskType;
  difficulty?: number;
  description?: string;
  status?: TaskStatus;
  startDate: Date;
  endDate: Date;
  color?: string;

  
  isAiTask?: boolean;
  planId?: number;
  aiTaskId?: number;
  priority?: number;
}
```

## Error Handling

### API Error Responses
- HTTP status codes indicate success/failure
- Error messages logged to console
- User-friendly error handling in components
- Graceful fallbacks for failed requests

### Loading States
- `isGenerating` state for AI plan generation
- Loading indicators in UI components
- Disabled states during API calls

## API Utilities

### apiUtils.ts
Common utilities for API communication:

- `getAuthHeaders()`: Authentication header generation
- `getCurrentUserId()`: User ID retrieval from storage
- Error handling helpers
- Request/response interceptors

## State Management

### Local State
- React `useState` for component-level state
- `useMemo` for computed values (task combinations, calendar matrices)
- `useEffect` for data loading on mount

### Data Flow
1. Components trigger API calls via lib functions
2. API responses update local state
3. State changes re-render components
4. User interactions update backend via API calls

## Caching Strategy

- No explicit caching implemented
- Data refetched on component mount
- Real-time updates for user actions
- Future enhancement: React Query/SWR for caching