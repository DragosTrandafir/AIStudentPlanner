# Types and Utilities

## TypeScript Configuration

**Version:** TypeScript 5.x
**Configuration:** `tsconfig.json` with strict mode enabled
**Path Mapping:** `@/` alias for `src/` directory

## Type Definitions

### Core Types (`/types`)

#### Task.ts
Primary data structure for calendar tasks:

```typescript
export type TaskStatus = "Pending" | "In Progress" | "Completed";
export type TaskType =  "Project" | "Practical Exam" | "Written Exam" ;

export interface Task {
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

  // AI Task specific fields
  isAiTask?: boolean;
  planId?: number;
  aiTaskId?: number;
  priority?: number;
}
```

#### AITask.ts
AI-specific task interface:

```typescript
export interface AITask {
  id: number;
  planId: number;
  taskName: string;
  subjectName: string;
  timeAllotted: string;
  difficulty: number;
  priority: number;
  date: string;
}
```

#### SubjectResponse.ts
Backend subject data structure:

```typescript
export interface SubjectResponse {
  id: number;
  name: string;
  description?: string;
  color?: string;
  user_id: number;
  created_at: string;
  updated_at: string;
}
```

## Utility Functions

### Date Utilities (`/utils/dateUtils.ts`)

#### Date Formatting and Parsing
- `formatDate(date, format)`: Format dates consistently
- `parseDate(dateString)`: Parse date strings safely
- `isValidDate(date)`: Validate date objects

#### Calendar Calculations
- `getMonthMatrix(date)`: Generate month grid for calendar
- `getWeekDates(date)`: Get dates for week view
- `isSameDay(date1, date2)`: Compare dates ignoring time
- `addDays(date, days)`: Date arithmetic

#### Business Logic
- `getDaysInMonth(date)`: Days in month calculation
- `getFirstDayOfMonth(date)`: First day of month
- `getLastDayOfMonth(date)`: Last day of month

### API Utilities (`/utils/apiUtils.ts`)

#### Authentication Helpers
- `getAuthHeaders()`: Generate Bearer token headers
- `getCurrentUserId()`: Retrieve user ID from storage
- `isAuthenticated()`: Check authentication status

#### Request/Response Handling
- `handleApiError(error)`: Standardized error handling
- `retryRequest(fn, retries)`: Retry failed requests

### Data Mappers

#### aiTaskMapper.ts
Converts backend AI plan data to frontend Task format:

```typescript
export function mapPlansToTasks(plans: PlanResponse[]): Task[] {
  // Implementation maps PlanResponse.entries to Task[]
}
```

#### subjectMapper.ts
Converts SubjectResponse to Task format:

```typescript
export function mapSubjectToTask(subject: SubjectResponse): Task {
  // Implementation creates Task from SubjectResponse
}
```

#### eventMapper.ts
Maps tasks to calendar event format for FullCalendar:

```typescript
export function mapTaskToEvent(task: Task): CalendarEvent {
  // Implementation for FullCalendar integration
}
```

### Calendar Utilities (`/utils/calendarStyles.ts`)

#### Styling Helpers
- `getTaskColor(task)`: Get color based on task type/status
- `getEventStyles(task)`: Generate CSS classes for calendar events
- `calculateEventPosition(task, view)`: Position calculations

### User Storage (`/utils/userStorage.ts`)

#### Local Storage Management
- `saveUser(user)`: Store user data
- `getUser()`: Retrieve user data
- `clearUser()`: Remove user data
- `saveToken(token)`: Store auth token
- `getToken()`: Retrieve auth token

## Custom Hooks (Future Enhancement)

Potential custom hooks for reusability:

```typescript
// useAuth.ts
export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  // Authentication logic
}

// useTasks.ts
export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  // Task management logic
}
```

## Constants and Enums

### Task Types and Status
Defined as string unions for type safety:

```typescript
type TaskType =  "Project" | "Practical Exam" | "Written Exam" ;
type TaskStatus = "Pending" | "In Progress" | "Completed";
```

### API Endpoints
Centralized endpoint definitions:

```typescript
const API_ENDPOINTS = {
  USERS: '/users',
  PLANS: '/plans',
  SUBJECTS: '/subjects',
} as const;
```

## Error Types

Custom error classes for better error handling:

```typescript
export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

export class ValidationError extends Error {
  constructor(public field: string, message: string) {
    super(message);
  }
}
```

## Type Guards

Runtime type checking functions:

```typescript
export function isTask(obj: any): obj is Task {
  return obj && typeof obj.id === 'number' && typeof obj.title === 'string';
}

export function isAITask(task: Task): task is Task & { isAiTask: true } {
  return task.isAiTask === true;
}
```

## Performance Optimizations

### Memoization
- `useMemo` for expensive calculations
- `useCallback` for event handlers
- `React.memo` for component memoization

### Lazy Loading
- Dynamic imports for heavy components
- Route-based code splitting with Next.js

## Development Utilities

### Type Checking
- Strict TypeScript configuration
- ESLint rules for type safety
- Pre-commit hooks for type checking

### Testing Types
- Test utilities for component props
- Mock data generators with proper typing
- API response type assertions