# Ideas For Indians

A platform where users can share business ideas and others can upvote, downvote, and provide suggestions.


### Run the Application
```bash
python app.py
```
The application will be available at `http://localhost:5000`

## Project Structure

```
├── app.py          # Main Flask application
├── firebase_config.py    # Firebase configuration and initialization
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in version control)
└── templates/           # HTML templates
    ├── home.html       # Home page template
    ├── detail.html     # Idea detail page template
    └── error.html      # Error page template
```

## Features

- Share business ideas
- Upvote/downvote ideas
- Add suggestions to ideas
- Real-time updates using Firebase
- Responsive design using Tailwind CSS

## API Endpoints

### Ideas
- `GET /` - Get all ideas
- `GET /detail/<idea_id>` - Get specific idea details
- `POST /new_idea` - Create new idea
- `POST /vote/<idea_id>/<vote_type>` - Vote on an idea

### Suggestions
- `POST /new_suggestion/<idea_id>` - Add suggestion to an idea

## Data Structure

```json
{
  "ideas": {
    "idea_id": {
      "title": "Idea Title",
      "description": "Idea Description",
      "upvotes": 0,
      "downvotes": 0,
      "score": 0,
      "created_at": "2024-04-26T10:00:00",
      "suggestions": [
        {
          "text": "Suggestion text",
          "created_at": "2024-04-26T11:00:00"
        }
      ]
    }
  }
}
```