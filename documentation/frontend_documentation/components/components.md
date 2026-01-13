# Components Documentation

## Component Organization

Components are organized by feature in the `/components` directory:

```
components/
├── authenticate/     # Login/Register components
├── buttons/         # Reusable button components
├── calendar/        # Calendar-related components
├── context/         # React context providers
├── modals/          # Modal dialogs
└── sidebar/         # Sidebar navigation
```

## Authentication Components

### LoginLayout
- Handles user login form
- Validates credentials
- Transitions to main app on success
- Provides link to registration

**Props:**
- `onLogin`: Callback when login succeeds
- `onRegister`: Callback to switch to register view

### RegisterLayout
- User registration form
- Input validation
- Success/error feedback
- Navigation back to login

**Props:**
- `onRegisterSuccess`: Callback when registration succeeds
- `onGoToLogin`: Callback to switch to login view

## Calendar Components

### MainCalendar
**Primary component for the main application view.**

**Features:**
- State management for tasks, dates, and view modes
- API integration for loading subjects and AI plans
- Modal management for task creation/details
- Calendar navigation and view switching

**State:**
- `subjectTasks`: Manual user-created tasks
- `aiTasks`: AI-generated study tasks
- `selectedDate`: Currently selected date
- `currentMonth`: Current month being displayed
- `viewMode`: Current calendar view (month/week/day)

**Key Functions:**
- `loadSubjects()`: Fetches user subjects from backend
- `loadPlans()`: Fetches latest AI-generated schedule
- `handleGeneratePlan()`: Triggers AI plan generation
- `handleReschedule()`: Reschedules existing plan with feedback

### CalendarHeader
- Navigation controls (previous/next month/week)
- View mode selector (month/week/day)
- Current period display
- Quick navigation to today

### WeekView
- Weekly calendar grid
- Task display for selected week
- Time slot visualization
- Click handlers for date/task selection

### DayView
- Daily schedule view
- Hourly time slots
- Task positioning by time
- Detailed day planning

### MiniMonthView
- Compact month calendar
- Date selection
- Current date highlighting
- Navigation between months

## Modal Components

### AddTaskModal
- Form for creating new tasks
- Subject selection
- Date/time pickers
- Task type selection (Assignment/Project/Exam)

### TaskDetailsModal
- Display task information
- Edit task details
- Status updates
- Delete task functionality

## Button Components

### PrimaryButton, SecondaryButton, etc.
- Consistent button styling
- Loading states
- Icon support
- Accessibility features

## Sidebar Component

### Sidebar
- Navigation menu
- User profile section
- Theme toggle
- Logout functionality
- Collapsible design

## Context Providers

### ThemeProvider
- Manages dark/light theme state
- Provides theme toggle functionality
- Persists theme preference
- Applies theme classes to document

## Styling Approach

Components use a combination of:
- **Tailwind CSS**: Utility classes for layout and basic styling
- **Custom CSS**: Component-specific styles in `/styles` directory
- **CSS Variables**: Theme-aware color schemes
- **CSS Modules**: Scoped component styles where needed