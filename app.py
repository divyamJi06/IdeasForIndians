from flask import Flask, render_template, request, jsonify, redirect, url_for
from firebase_config import initialize_firebase, get_db
from datetime import datetime
import os
import json

# Initialize Flask app
app = Flask(__name__)

# Configure app for production
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-key-change-in-production'),
    JSON_SORT_KEYS=False,
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
    TEMPLATES_AUTO_RELOAD=False  # Disable in production
)

# Initialize Firebase
try:
    initialize_firebase()
    db = get_db()
    print("Firebase initialized, db:", db)
except Exception as e:
    print(f"Firebase initialization error: {str(e)}")
    db = None

def format_timestamp(timestamp):
    """Format timestamp for display"""
    if not timestamp:
        return "No date"
    try:
        if isinstance(timestamp, str):
            return timestamp
        return timestamp.strftime("%B %d, %Y")
    except Exception:
        return "Invalid date"

@app.route('/')
def home():
    """Home page route"""
    try:
        # Get all ideas ordered by timestamp
        ideas_ref = db.collection('ideas').order_by('created_at', direction='DESCENDING').stream()
        all_data = []
        
        for idea in ideas_ref:
            idea_data = idea.to_dict()
            idea_data['id'] = idea.id
            
            # Get suggestions count
            suggestions = db.collection('ideas').document(idea.id).collection('suggestions').stream()
            idea_data['suggestions'] = [s.to_dict() for s in suggestions]
            
            # Format timestamp
            idea_data['created_at'] = format_timestamp(idea_data.get('created_at'))
            
            all_data.append(idea_data)
            
        return render_template('home.html', allData=all_data)
    except Exception as e:
        print(f"Error in home route: {str(e)}")
        return render_template('error.html', error_message="Failed to load ideas. Please try again later.")

@app.route('/detail/<idea_id>')
def detail(idea_id):
    """Detail page route"""
    try:
        # Get idea details
        idea_ref = db.collection('ideas').document(idea_id)
        idea = idea_ref.get()
        
        if not idea.exists:
            return render_template('error.html', error_message="Idea not found"), 404
            
        idea_data = idea.to_dict()
        idea_data['id'] = idea.id
        
        # Get suggestions
        suggestions = idea_ref.collection('suggestions').order_by('created_at', direction='DESCENDING').stream()
        idea_data['suggestions'] = []
        
        for suggestion in suggestions:
            suggestion_data = suggestion.to_dict()
            suggestion_data['created_at'] = format_timestamp(suggestion_data.get('created_at'))
            idea_data['suggestions'].append(suggestion_data)
            
        # Format timestamp
        idea_data['created_at'] = format_timestamp(idea_data.get('created_at'))
        
        return render_template('detail.html', data={'isPresent': True, 'data': idea_data})
    except Exception as e:
        print(f"Error in detail route: {str(e)}")
        return render_template('error.html', error_message="Failed to load idea details. Please try again later.")

@app.route('/new_idea', methods=['POST'])
def new_idea():
    """Create new idea endpoint"""
    try:
        data = request.json
        
        if not data or not data.get('title') or not data.get('description'):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Create new idea document
        new_idea_ref = db.collection('ideas').document()
        new_idea_ref.set({
            'title': data['title'],
            'description': data['description'],
            'created_at': datetime.now(),
            'score': 0
        })
        
        return jsonify({'success': True, 'id': new_idea_ref.id})
    except Exception as e:
        print(f"Error creating new idea: {str(e)}")
        return jsonify({'error': 'Failed to create idea'}), 500

@app.route('/new_suggestion/<idea_id>', methods=['POST'])
def new_suggestion(idea_id):
    """Add new suggestion endpoint"""
    try:
        data = request.json
        
        if not data or not data.get('text'):
            return jsonify({'error': 'Missing suggestion text'}), 400
            
        # Verify idea exists
        idea_ref = db.collection('ideas').document(idea_id)
        if not idea_ref.get().exists:
            return jsonify({'error': 'Idea not found'}), 404
            
        # Create new suggestion
        suggestion_ref = idea_ref.collection('suggestions').document()
        suggestion_ref.set({
            'text': data['text'],
            'created_at': datetime.now()
        })
        
        return jsonify({'success': True, 'id': suggestion_ref.id})
    except Exception as e:
        print(f"Error creating new suggestion: {str(e)}")
        return jsonify({'error': 'Failed to add suggestion'}), 500

@app.route('/vote/<idea_id>/<vote_type>', methods=['POST'])
def vote(idea_id, vote_type):
    """Handle voting endpoint"""
    try:
        if vote_type not in ['upvote', 'downvote']:
            return jsonify({'error': 'Invalid vote type'}), 400
            
        # Get idea reference
        idea_ref = db.collection('ideas').document(idea_id)
        idea = idea_ref.get()
        
        if not idea.exists:
            return jsonify({'error': 'Idea not found'}), 404
            
        # Update score
        current_score = idea.to_dict().get('score', 0)
        new_score = current_score + (1 if vote_type == 'upvote' else -1)
        
        idea_ref.update({'score': new_score})
        
        return jsonify({'success': True, 'score': new_score})
    except Exception as e:
        print(f"Error processing vote: {str(e)}")
        return jsonify({'error': 'Failed to process vote'}), 500

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('error.html', error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('error.html', error_message="Internal server error. Please try again later."), 500

if __name__ == '__main__':
    # Run the app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 