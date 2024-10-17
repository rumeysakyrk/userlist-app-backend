User List - Flask Backend

This is a backend project for a user detail tracking platform built using Flask and PostgreSQL. The application is designed to display users’ general information and detailed views including their posts (with comments), albums (with photos), and a task list.

Project Structure

This project includes the following main features:

	•	User List: Displays general information about users.
	•	User Detail Page: Shows user posts, albums, and task lists.
	•	Database: PostgreSQL is used for managing users, posts, comments, albums, photos, and tasks.

Bonus Features

	•	Postman Collections: Two Postman collections are included:
	1.	User API Collection: Covers all user-related endpoints.
	2.	Task API Collection: Includes endpoints for managing task lists.

Prerequisites

To set up the project locally, you will need the following:

	•	Python 3.8+: Download and install Python
	•	PostgreSQL: Install PostgreSQL
	•	Flask: Install Flask and related dependencies with pip
	•	Postman: Download Postman

Installation

	1.	Clone the repository:

git clone https://github.com/rumeysakyrk/userlist-app-backend.git
cd userlist-app-backend


	2.	Install dependencies:

pip install -r requirements.txt


	3.	Set up the PostgreSQL database and run migrations (make sure PostgreSQL is running):

flask db init
flask db migrate
flask db upgrade


	4.	Run the development server:

flask run


	5.	Access the API locally at http://127.0.0.1:5000.

Postman Collection

You can test the API using the provided Postman collections:

	•	User API Collection: Includes endpoints for user listing, user details, posts, comments, albums, and photos.
	•	Task API Collection: Includes endpoints for managing user tasks.

To use the collections:

	1.	Open Postman.
	2.	Import the collections from the postman-collections/ directory in the project.
 Postman screenshoots:

<img width="1055" alt="postman" src="https://github.com/user-attachments/assets/6b04e131-b60f-47ad-923d-2c48e63216b2">
<img width="1055" alt="postman-1" src="https://github.com/user-attachments/assets/b65129b6-1383-4b90-826e-af0d662354aa">



Contributing

Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.

License

This project is licensed under the MIT License.

