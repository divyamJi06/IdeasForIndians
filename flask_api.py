from flask import Flask, request, jsonify

from index import createCommit

app = Flask(__name__)

# Sample data structure to store ideas and suggestions
@app.route("/")
def home():
    return "Working fine", 200

@app.route('/new_idea', methods=['POST'])
def new_idea():
    try:
        data = request.json

        print(data)

        # Add new idea to the ideas_data list
        # ideas_data.append(data)
        createCommit("newidea",new_idea_data = data)

        return jsonify({"message": "New idea added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/new_suggestion/<int:idea_id>', methods=['POST'])
def new_suggestion(idea_id):
    try:
        data = request.json
        print(data)
        print(idea_id)
        createCommit(typeOfData= "newsuggestion", new_suggestion_data = data, idea_id=idea_id)


        if idea_id:
            # Add new suggestion to the idea's suggestions list

            return jsonify({"message": f"New suggestion added to Idea {idea_id}"}), 201
        else:
            return jsonify({"error": f"Idea with ID {idea_id} not found"}), 404

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
