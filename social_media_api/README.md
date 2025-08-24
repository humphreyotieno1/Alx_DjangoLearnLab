# Social Media API

## Setup Instructions
1. Clone the repository: `git clone https://github.com/Alx_DjangoLearnLab/social_media_api.git`
2. Install requirements: `pip install -r requirements.txt`
3. Apply migrations: `python manage.py makemigrations && python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Run server: `python manage.py runserver`

## API Endpoints

### Authentication
- POST /api/register/ - Register a new user
- POST /api/login/ - Login and receive auth token
- GET /api/profile/ - View user profile (requires authentication)

### Posts and Comments
- GET/POST /api/posts/ - List or create posts
- GET/PUT/DELETE /api/posts/<id>/ - Retrieve, update, or delete a specific post
- GET/POST /api/comments/ - List or create comments
- GET/PUT/DELETE /api/comments/<id>/ - Retrieve, update, or delete a specific comment

### Follow System
- POST /api/follow/<user_id>/ - Follow a user
- POST /api/unfollow/<user_id>/ - Unfollow a user
- GET /api/feed/ - Get posts from followed users

### Likes and Notifications
- POST /api/posts/<id>/like/ - Like a post
- POST /api/posts/<id>/unlike/ - Unlike a post
- GET /api/notifications/ - View notifications
- POST /api/notifications/ - Mark notifications as read

## Testing
- Use Postman to test endpoints
- All endpoints requiring authentication need an Authorization header: `Token <token>`
- Example Postman collection provided in `tests/postman_collection.json`

## Models
- CustomUser: Extended user model with bio, profile_picture, and followers
- Post: Contains author, title, content, and timestamps
- Comment: Links to post and author with content and timestamps
- Like: Tracks post likes by users
- Notification: Generic notifications for various user actions