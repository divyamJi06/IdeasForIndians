# UI Prompts for Ideas For Indians

## Application Overview

Ideas For Indians is a collaborative platform designed to foster innovation and problem-solving within the Indian community. The application allows users to:

1. **Share Ideas**
   - Post innovative ideas for solving various challenges
   - Provide detailed descriptions of proposed solutions
   - Track community engagement through votes and suggestions

2. **Community Interaction**
   - Upvote/downvote ideas to show support or concern
   - Add constructive suggestions to existing ideas
   - View and sort ideas based on popularity
   - Engage in meaningful discussions around each idea

3. **Core Features**
   - User-friendly idea submission system
   - Voting mechanism for community feedback
   - Suggestion system for collaborative improvement
   - Dark/light mode for comfortable viewing
   - Responsive design for all devices
   - Real-time updates for votes and suggestions

The platform aims to create a space where Indians can collectively work on solutions to various challenges, from social issues to technological innovations, fostering a culture of collaborative problem-solving.

## UI Prompt Structure

This directory contains detailed UI prompts for generating the frontend of the Ideas For Indians application using LLMs. These prompts are designed to create a consistent, modern, and accessible user interface.

## Structure

1. `home_page_prompt.md`
   - Specifications for the main landing page
   - Ideas grid layout
   - New idea creation modal
   - Voting system

2. `detail_page_prompt.md`
   - Individual idea view
   - Suggestions section
   - New suggestion modal
   - Back navigation

3. `common_components_prompt.md`
   - Shared styles and components
   - Color system
   - Typography
   - Animation system
   - Dark mode implementation

## How to Use

1. **Order of Implementation**
   - Start with `common_components_prompt.md` to establish base styles
   - Implement `home_page_prompt.md` for the main interface
   - Finally, implement `detail_page_prompt.md` for individual ideas

2. **Using with LLMs**
   - Feed each prompt to your preferred LLM
   - Request HTML, CSS, and JavaScript code
   - Ensure all requirements are met
   - Verify accessibility compliance

3. **Customization**
   - Modify color schemes in common components
   - Adjust breakpoints for your needs
   - Customize animations and transitions
   - Add new components as needed

## Key Features

- Modern, responsive design
- Dark mode support
- Accessibility compliance
- Interactive components
- Consistent styling
- Mobile-first approach

## Dependencies

- Tailwind CSS
- Font Awesome
- Google Fonts (Inter & Poppins)

## Best Practices

1. **Consistency**
   - Use the defined color system
   - Follow typography guidelines
   - Maintain component patterns

2. **Accessibility**
   - Include ARIA labels
   - Ensure keyboard navigation
   - Maintain color contrast
   - Support screen readers

3. **Performance**
   - Optimize animations
   - Lazy load components
   - Minimize dependencies
   - Use appropriate image formats

4. **Responsive Design**
   - Test all breakpoints
   - Ensure mobile usability
   - Verify touch targets
   - Check content readability

## Testing

- Verify dark mode functionality
- Test responsive layouts
- Check all interactive features
- Validate accessibility
- Cross-browser testing 