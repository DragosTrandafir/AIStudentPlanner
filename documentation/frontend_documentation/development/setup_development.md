# Setup and Development Guide

## Prerequisites

Before setting up the frontend, ensure you have:

- **Node.js**: Version 18.x or higher
- **npm**: Version 8.x or higher (comes with Node.js)
- **Backend API**: Running on `http://localhost:8000`

## Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd planner-ai-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Verify installation:**
   ```bash
   npm run build
   ```

## Development

### Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

### Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint for code quality

## Project Structure

```
planner-ai-frontend/
├── app/                    # Next.js App Router pages
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── authenticate/      # Auth components
│   ├── calendar/          # Calendar components
│   ├── modals/           # Modal dialogs
│   └── sidebar/          # Navigation sidebar
├── lib/                   # API functions
├── styles/               # CSS stylesheets
├── types/                # TypeScript definitions
└── utils/                # Utility functions
```

## Configuration

### Environment Variables

Create a `.env.local` file in the root directory:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Development settings
NODE_ENV=development
```

### TypeScript Configuration

The project uses strict TypeScript configuration in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

## Development Workflow

### 1. Feature Development

1. Create a new branch for your feature
2. Implement changes following the component structure
3. Add TypeScript types for new data structures
4. Update styles if needed
5. Test functionality

### 2. Component Creation

When creating new components:

1. **Choose appropriate directory** in `/components`
2. **Use TypeScript** with proper prop types
3. **Follow naming conventions** (PascalCase for components)
4. **Add CSS modules or Tailwind classes**
5. **Export from index file** if applicable

### 3. API Integration

When adding new API calls:

1. Add function to appropriate `/lib` file
2. Include error handling
3. Add TypeScript interfaces for request/response
4. Update API utilities if needed

### 4. Styling

For component styling:

1. Use **Tailwind utilities** when possible
2. Add custom CSS to `/styles` directory
3. Use CSS variables for theming
4. Test in both light and dark themes

## Code Quality

### Linting

The project uses ESLint with Next.js configuration:

```bash
npm run lint
```

### TypeScript Checking

```bash
npx tsc --noEmit
```

### Pre-commit Hooks (Recommended)

Set up husky for pre-commit quality checks:

```bash
npm install --save-dev husky
npx husky init
```

## Testing

### Manual Testing Checklist

- [ ] Authentication flow (login/register)
- [ ] Calendar navigation (month/week/day views)
- [ ] Task creation and editing
- [ ] AI plan generation
- [ ] Theme switching
- [ ] Responsive design on mobile/tablet
- [ ] Error handling for API failures

### Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Deployment

### Build for Production

```bash
npm run build
npm start
```

### Environment Setup

For production deployment:

1. Set `NODE_ENV=production`
2. Configure production API URL
3. Set up proper CORS on backend
4. Configure domain and SSL

### Vercel Deployment

The app is optimized for Vercel deployment:

1. Connect GitHub repository
2. Configure environment variables
3. Deploy automatically on push

## Troubleshooting

### Common Issues

#### Build Errors
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check TypeScript errors: `npx tsc --noEmit`

#### Runtime Errors
- Check browser console for errors
- Verify backend API is running
- Check network tab for failed requests

#### Styling Issues
- Clear browser cache
- Check CSS variable definitions
- Verify Tailwind classes are not purged

### Debug Mode

Enable React DevTools and Redux DevTools for debugging:

```bash
npm install --save-dev @redux-devtools/extension
```

## Contributing

### Code Style

- Use Prettier for code formatting
- Follow TypeScript best practices
- Use meaningful variable and function names
- Add JSDoc comments for complex functions

### Commit Messages

Follow conventional commit format:

```
feat: add new calendar view
fix: resolve authentication bug
docs: update component documentation
```

### Pull Request Process

1. Create feature branch from `main`
2. Implement changes with tests
3. Update documentation if needed
4. Create PR with description
5. Code review and approval
6. Merge to main

## Performance

### Optimization Tips

- Use `React.memo` for expensive components
- Implement lazy loading for routes
- Optimize images and assets
- Monitor bundle size with `npm run build`

### Bundle Analysis

```bash
npm install --save-dev @next/bundle-analyzer
```

Add to `package.json`:

```json
{
  "scripts": {
    "analyze": "ANALYZE=true npm run build"
  }
}
```