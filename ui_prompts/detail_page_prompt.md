# Detail Page UI Prompt

Create a detailed view page for individual ideas with the following specifications:

## Core Features
1. Navigation Bar:
   - Logo/Site name on the left
   - "Back to Ideas" link on the right
   - Dark mode toggle (fixed position bottom-right)

2. Idea Detail Section:
   - Title (large, prominent)
   - Full description
   - Creation date
   - Number of suggestions
   - Vote system (upvote/downvote with score)
   - Responsive layout (stack on mobile)

3. Suggestions Section:
   - "Add Suggestion" button at the top
   - List of suggestions with:
     - Suggestion text
     - Creation date
     - Clean separation between items
   - Empty state message when no suggestions

4. New Suggestion Modal:
   - Textarea for suggestion
   - Submit and cancel buttons
   - Close on outside click/escape key

## Styling Requirements
1. Color Scheme:
   - Match home page theme
   - Primary: #3B82F6 (blue)
   - Primary Hover: #2563EB
   - Dark mode compatible

2. Typography:
   - Inter for body text
   - Poppins for headings
   - Hierarchical type scale
   - Responsive sizing

3. Components:
   - Card-based layout
   - Consistent spacing
   - Smooth transitions
   - Hover effects
   - Shadow effects

4. Dark Mode:
   - Consistent with home page
   - Appropriate contrast
   - Smooth transitions

## Technical Requirements
1. Dependencies:
   - Tailwind CSS
   - Font Awesome icons
   - Google Fonts (Inter & Poppins)

2. Responsive Design:
   - Mobile-first approach
   - Stack layouts on smaller screens
   - Maintain readability at all sizes
   - Flexible content areas

3. Interactive Features:
   - Voting system
   - Modal system
   - Form handling
   - Loading states
   - Error handling

4. Accessibility:
   - Semantic HTML
   - ARIA labels
   - Keyboard navigation
   - Focus management
   - Screen reader friendly

## User Experience
1. Layout:
   - Clear visual hierarchy
   - Comfortable reading width
   - Proper spacing
   - Responsive adjustments

2. Interactions:
   - Smooth transitions
   - Clear feedback
   - Loading indicators
   - Error states

3. Suggestions:
   - Easy to read
   - Clear chronological order
   - Visual separation
   - Easy to add new

4. Navigation:
   - Clear way back to home
   - Persistent theme toggle
   - Smooth transitions between states

## Error States
1. Idea Not Found:
   - Clear error message
   - Link back to home
   - Friendly messaging
   - Appropriate styling 