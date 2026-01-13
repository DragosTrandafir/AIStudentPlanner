# Styling and Theming

## CSS Architecture

The application uses a modular CSS approach combining Tailwind CSS with custom stylesheets.

## Tailwind CSS Configuration

**Version:** Tailwind CSS v4
**Configuration:** `tailwind.config.js` (if present) or inline config
**PostCSS:** Configured via `postcss.config.mjs`

## CSS File Organization

Styles are organized in the `/styles` directory:

```
styles/
├── variables.css      # CSS custom properties
├── themes.css         # Theme definitions
├── calendar.css       # Calendar component styles
├── authenticate.css   # Auth form styles
├── buttons.css        # Button component styles
├── modal.css          # Modal dialog styles
├── sidebar.css        # Sidebar styles
├── feedback.css       # Feedback-related styles
├── task_details.css   # Task details modal styles
├── user_detail.css    # User profile styles
├── date_picker.css    # Date picker overrides
└── mini-calendar.css  # Mini calendar styles
```

## CSS Variables (Custom Properties)

Defined in `variables.css`:

```css
:root {
  /* Colors */
  --primary-color: #3b82f6;
  --secondary-color: #6b7280;
  --success-color: #10b981;
  --error-color: #ef4444;
  --warning-color: #f59e0b;

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  /* Typography */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.5rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
```

## Theme System

### ThemeProvider Context
- Manages theme state (light/dark)
- Provides `toggleTheme()` function
- Applies theme classes to document root

### Theme Definitions (`themes.css`)

**Light Theme:**
```css
.light-theme {
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --border-color: #e5e7eb;
}
```

**Dark Theme:**
```css
.dark-theme {
  --bg-primary: #1f2937;
  --bg-secondary: #111827;
  --text-primary: #f9fafb;
  --text-secondary: #d1d5db;
  --border-color: #374151;
}
```

### Theme Application
- Theme classes applied to `<html>` element
- CSS variables update automatically
- Components use CSS variables for theming
- No JavaScript theme logic in components

## Component Styling Patterns

### Utility-First with Tailwind
Most components use Tailwind utility classes:

```tsx
<div className="flex items-center justify-between p-4 bg-white rounded-lg shadow-md">
  <h3 className="text-lg font-semibold text-gray-900">Task Title</h3>
  <button className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600">
    Edit
  </button>
</div>
```

### Custom CSS for Complex Styles
Complex layouts and animations use custom CSS:

```css
/* calendar.css */
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: var(--spacing-sm);
}

.calendar-day {
  aspect-ratio: 1;
  padding: var(--spacing-sm);
  border-radius: var(--border-radius);
  transition: background-color 0.2s ease;
}

.calendar-day:hover {
  background-color: var(--bg-hover);
}
```

### CSS Modules (Future Enhancement)
For component-scoped styles, CSS Modules can be used:

```css
/* ComponentName.module.css */
.container {
  /* Scoped styles */
}
```

## Color Coding System

### Task Types
Tasks are color-coded by type:

```typescript
const typeColors: Record<string, string> = {
  Project: "#90EE90",        
  "Written Exam": "#87CEFA",  
  "Practical Exam": "#FFB6C1"
};
```

### Status Indicators
- **Pending**: Default styling
- **In Progress**: Accent border/color
- **Completed**: Muted styling with checkmark

## Responsive Design

### Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Responsive Utilities
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Responsive grid */}
</div>
```

### Mobile-First Approach
- Base styles for mobile
- Progressive enhancement for larger screens
- Touch-friendly interactive elements

## Accessibility

### Color Contrast
- WCAG AA compliance for text contrast
- Sufficient contrast ratios for interactive elements

### Focus Management
- Visible focus indicators
- Keyboard navigation support
- Screen reader friendly markup

### Semantic HTML
- Proper heading hierarchy
- ARIA labels where needed
- Semantic form elements

## Performance Considerations

### CSS Optimization
- Minimal CSS bundle size
- Efficient selectors
- Avoid CSS-in-JS for static styles

### Loading Strategy
- Critical CSS inlined
- Non-critical styles loaded asynchronously
- Font loading optimization with `next/font`

## Development Workflow

### Adding New Styles
1. Check if Tailwind utilities suffice
2. Add to appropriate `.css` file if custom styles needed
3. Use CSS variables for theming
4. Test across themes and breakpoints
5. Validate accessibility