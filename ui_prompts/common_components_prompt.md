# Common Components and Styles UI Prompt

Create a set of consistent components and styles to be shared across all pages of the "Ideas For Indians" application.

## Base Styles
1. Colors:
   ```css
   :root {
       --primary-color: #3B82F6;
       --primary-hover: #2563EB;
       --success-color: #10B981;
       --danger-color: #EF4444;
       --background-light: #F3F4F6;
       --background-dark: #1A1A1A;
       --text-light: #4B5563;
       --text-dark: #E5E7EB;
   }
   ```

2. Typography:
   - Font Families:
     - Body: Inter
     - Headings: Poppins
   - Base sizes and weights
   - Line heights and spacing
   - Responsive scaling

3. Spacing System:
   - Consistent padding/margin scale
   - Grid gaps
   - Component spacing
   - Responsive adjustments

## Shared Components
1. Vote Container:
   ```css
   .vote-container {
       display: flex;
       align-items: center;
       background-color: #f3f4f6;
       border-radius: 9999px;
       padding: 0.5rem;
       gap: 0.5rem;
   }
   ```

2. Vote Buttons:
   - Upvote/downvote styling
   - Hover effects
   - Color transitions
   - Score display

3. Navigation Bar:
   - Layout structure
   - Responsive behavior
   - Dark mode support

4. Modal System:
   - Base structure
   - Animation classes
   - Overlay styling
   - Close behaviors

## Dark Mode System
1. Theme Toggle:
   - Button styling
   - Icon transitions
   - Position and responsiveness
   - Local storage integration

2. Color Transitions:
   - Smooth mode switching
   - Component-specific adjustments
   - Text contrast maintenance

3. Dark Variants:
   - Background colors
   - Text colors
   - Border colors
   - Shadow effects

## Animation System
1. Transitions:
   ```css
   .transition-base {
       transition: all 0.3s ease;
   }
   ```

2. Hover Effects:
   - Scale transforms
   - Color changes
   - Shadow adjustments

3. Fade Animations:
   ```css
   @keyframes fadeIn {
       from { opacity: 0; }
       to { opacity: 1; }
   }
   ```

## Button System
1. Primary Button:
   ```css
   .btn-primary {
       background-color: var(--primary-color);
       color: white;
       padding: 0.75rem 1.5rem;
       border-radius: 0.5rem;
       font-weight: 500;
       transition: all 0.3s ease;
   }
   ```

2. Secondary Button:
   - Ghost style
   - Outline style
   - Text style

3. Interactive States:
   - Hover
   - Focus
   - Active
   - Disabled

## Card System
1. Base Card:
   ```css
   .card {
       border-radius: 1rem;
       transition: transform 0.3s ease;
       box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
   }
   ```

2. Card Variations:
   - Elevated
   - Bordered
   - Interactive

## Responsive Utilities
1. Breakpoints:
   ```css
   /* Mobile first approach */
   @media (min-width: 640px) { /* Small */ }
   @media (min-width: 768px) { /* Medium */ }
   @media (min-width: 1024px) { /* Large */ }
   ```

2. Container Sizes:
   - Max widths
   - Padding
   - Margin

## JavaScript Utilities
1. Theme Management:
   - Local storage
   - System preference detection
   - Mode switching

2. Modal Management:
   - Open/close handlers
   - Outside click detection
   - Keyboard events

3. Interactive Features:
   - Button state management
   - Loading states
   - Error handling
   - Form validation 