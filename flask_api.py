from flask import Flask, render_template, request, jsonify
from index import createCommit, get_data_from_github

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    try:
        allData = get_data_from_github(branch="master")
        # print(allData)

        return render_template('home.html', allData=allData)

    except Exception as e:
        # Handle exceptions here, e.g., log the error
        print(f"Error in home route: {str(e)}")
        return render_template('error.html', error_message="An error occurred while fetching data.")


@app.route("/detail/<int:idea_id>", methods=["GET"])
def detail(idea_id):
    try:
        allData = get_data_from_github(branch="master")
        filtered_data = next((i for i in allData if i['id'] == idea_id), None)
        print(filtered_data)

        if not filtered_data:
            data = {
                "isPresent": False,
                "data": filtered_data
            }
            return render_template("detail.html", data=data)

        data = {
            "isPresent": True,
            "data": filtered_data
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

        print(data)

        # Add new idea to the ideas_data list
        # ideas_data.append(data)
        createCommit("newidea", new_idea_data=data)

        return jsonify({"message": "New idea added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/new_suggestion/<int:idea_id>', methods=['POST'])
def new_suggestion(idea_id):
    try:
        data = request.json
        print(data)
        print(idea_id)
        createCommit(typeOfData="newsuggestion", new_suggestion_data=data, idea_id=idea_id)

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
