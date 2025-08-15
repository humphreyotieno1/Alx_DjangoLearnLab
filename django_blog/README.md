# Blog Post Management Features

## Overview
The blog post management system allows users to perform CRUD operations (Create, Read, Update, Delete) on blog posts. Authenticated users can create, edit, and delete their own posts, while all users can view posts.

## Features
1. **List Posts**: Displays all posts with titles, content snippets, and author information at `/posts/`.
2. **View Post Details**: Shows the full content of a single post at `/posts/<id>/`.
3. **Create Posts**: Authenticated users can create posts at `/posts/new/`.
4. **Edit Posts**: Authors can edit their posts at `/posts/<id>/edit/`.
5. **Delete Posts**: Authors can delete their posts at `/posts/<id>/delete/`.

## Implementation Details
- **Models**: The `Post` model (`blog/models.py`) includes `title`, `content`, `published_date`, and `author` (linked to `User`).
- **Views**: Class-based views (`PostListView`, `PostDetailView`, `PostCreateView`, `PostUpdateView`, `PostDeleteView`) in `blog/views.py` handle CRUD operations.
- **Forms**: `PostForm` (`blog/forms.py`) validates `title` and `content`, with the `author` set programmatically.
- **Templates**: Located in `blog/templates/blog/`:
  - `post_list.html`: Lists all posts.
  - `post_detail.html`: Shows a single post.
  - `post_form.html`: Handles create/edit forms.
  - `post_confirm_delete.html`: Confirms deletion.
- **URLs**: Defined in `blog/urls.py` with intuitive paths.
- **Permissions**:
  - `LoginRequiredMixin` restricts create/edit/delete to authenticated users.
  - `UserPassesTestMixin` ensures only the post’s author can edit/delete.
  - List and detail views are public.

## Setup Instructions
1. Ensure dependencies are installed: `pip install django`.
2. Apply migrations: `python manage.py makemigrations && python manage.py migrate`.
3. Run the server: `python manage.py runserver`.
4. Access `/posts/` to view posts, or log in to create/edit/delete.

## Testing Instructions
1. **List Posts**: Visit `/posts/` to see all posts. Log in to see the "Create New Post" link.
2. **View Details**: Click a post title to view its full content.
3. **Create Post**: Log in, go to `/posts/new/`, and submit a post. Test invalid inputs (e.g., short title).
4. **Edit Post**: As the author, visit `/posts/<id>/edit/`. Try as a non-author to confirm access is denied.
5. **Delete Post**: As the author, visit `/posts/<id>/delete/`. Confirm deletion redirects to `/posts/`.
6. **Security**: Verify CSRF tokens in forms and that unauthenticated users are redirected to `/login/`.

## Notes
- The `author` field is automatically set to the logged-in user during post creation/editing.
- Media files (e.g., profile pictures) are served via `MEDIA_URL` and `MEDIA_ROOT`.
- CSS styling is applied from `blog/static/blog/css/styles.css`.