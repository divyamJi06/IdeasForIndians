from flask import Flask, render_template, request, jsonify
from datetime import datetime
from firebase_config import initialize_firebase, get_db
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

app = Flask(__name__)

# Initialize Firebase
initialize_firebase()
db = get_db()

@app.route("/", methods=["GET"])
def home():
    try:
        # Get all ideas from Firestore
        ideas_ref = db.collection('ideas')
        ideas = ideas_ref.stream()
        
        # Convert to list and add id to each idea
        allData = []
        for doc in ideas:
            idea = doc.to_dict()
            idea['id'] = doc.id
            # Convert Firestore datetime to formatted string
            if isinstance(idea.get('created_at'), (datetime, DatetimeWithNanoseconds)):
                idea['created_at'] = idea['created_at'].strftime('%Y-%m-%d')
            allData.append(idea)
            
        # Sort by score (if exists) or created_at
        allData.sort(key=lambda x: (x.get('score', 0), x.get('created_at', ''), x.get('id', '')), reverse=True)

        return render_template('home.html', allData=allData)

    except Exception as e:
        # Handle exceptions here, e.g., log the error
        print(f"Error in home route: {str(e)}")
        return render_template('error.html', error_message="An error occurred while fetching data.")


@app.route("/detail/<idea_id>", methods=["GET"])
def detail(idea_id):
    try:
        # Get specific idea from Firestore
        idea_doc = db.collection('ideas').document(idea_id).get()

        if not idea_doc.exists:
            data = {
                "isPresent": False,
                "data": None
            }
            return render_template("detail.html", data=data)

        # Get idea data and add id
        idea_data = idea_doc.to_dict()
        idea_data['id'] = idea_doc.id
        
        # Format datetime for display
        if isinstance(idea_data.get('created_at'), (datetime, DatetimeWithNanoseconds)):
            idea_data['created_at'] = idea_data['created_at'].strftime('%Y-%m-%d')
            
        # Format datetime for suggestions
        if idea_data.get('suggestions'):
            for suggestion in idea_data['suggestions']:
                if isinstance(suggestion.get('created_at'), (datetime, DatetimeWithNanoseconds)):
                    suggestion['created_at'] = suggestion['created_at'].strftime('%Y-%m-%d')
        
        data = {
            "isPresent": True,
            "data": idea_data
        }
        return render_template('detail.html', data=data)

    except Exception as e:
        # Handle exceptions here, e.g., log the error
        print(f"Error in detail route: {str(e)}")
        return render_template('error.html', error_message="An error occurred while processing the request.")


# Add an error route for displaying errors
@app.route("/error", methods=["GET"])
def error():
    return render_template('error.html', error_message="An unexpected error occurred.")


@app.route('/<path:invalid_path>')
def handle_invalid_path(invalid_path):
    # Log or handle the unexpected URL as needed
    print(f"Unexpected URL: /{invalid_path}")

    # Render the error.html template
    return render_template('error.html', error_message="Unexpected URL. Please go back to the home page.")


@app.route('/new_idea', methods=['POST'])
def new_idea():
    try:
        data = request.json
        
        # Add default fields
        data['upvotes'] = 0
        data['downvotes'] = 0
        data['score'] = 0
        data['created_at'] = datetime.now()
        data['suggestions'] = []

        # Add new idea to Firestore
        doc_ref = db.collection('ideas').document()
        doc_ref.set(data)
        
        return jsonify({
            "message": "New idea added successfully",
            "id": doc_ref.id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/vote/<idea_id>/<string:vote_type>', methods=['POST'])
def vote_idea(idea_id, vote_type):
    try:
        if vote_type not in ['upvote', 'downvote']:
            return jsonify({"error": "Invalid vote type"}), 400

        # Get idea reference
        idea_ref = db.collection('ideas').document(idea_id)
        idea_doc = idea_ref.get()
        
        if not idea_doc.exists:
            return jsonify({"error": "Idea not found"}), 404

        idea = idea_doc.to_dict()
        
        # Update vote counts
        if vote_type == 'upvote':
            idea['upvotes'] = idea.get('upvotes', 0) + 1
        else:
            idea['downvotes'] = idea.get('downvotes', 0) + 1
        
        idea['score'] = idea['upvotes'] - idea['downvotes']
        
        # Update idea in Firestore
        idea_ref.update({
            'upvotes': idea['upvotes'],
            'downvotes': idea['downvotes'],
            'score': idea['score']
        })

        return jsonify({
            "message": "Vote recorded successfully",
            "upvotes": idea['upvotes'],
            "downvotes": idea['downvotes'],
            "score": idea['score']
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/new_suggestion/<idea_id>', methods=['POST'])
def new_suggestion(idea_id):
    try:
        data = request.json
        data['created_at'] = datetime.now()

        # Get idea reference
        idea_ref = db.collection('ideas').document(idea_id)
        idea_doc = idea_ref.get()
        
        if not idea_doc.exists:
            return jsonify({"error": "Idea not found"}), 404

        idea = idea_doc.to_dict()
        
        # Initialize suggestions list if it doesn't exist
        if 'suggestions' not in idea:
            idea['suggestions'] = []

        # Add new suggestion
        idea['suggestions'].append(data)
        
        # Update suggestions in Firestore
        idea_ref.update({
            'suggestions': idea['suggestions']
        })

        return jsonify({"message": f"New suggestion added to Idea {idea_id}"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/like/<string:type_of_data>/<int:item_id>', methods=['PATCH'])
def like_item(type_of_data, item_id):
    try:
        # Find the item (idea or suggestion) with the specified ID
        item = None
        # for idea in ideas_data:
        #     if idea['id'] == item_id:
        #         item = idea
        #         break
        #     for suggestion in idea['suggestions']:
        #         if suggestion['id'] == item_id:
        #             item = suggestion
        #             break

        if item:
            # Increase the 'likes' count for the item
            item['likes'] += 1

            return jsonify({"message": f"Likes increased for {type_of_data.capitalize()} {item_id}"}), 200
        else:
            return jsonify({"error": f"{type_of_data.capitalize()} with ID {item_id} not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
