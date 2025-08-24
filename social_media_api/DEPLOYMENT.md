Social Media API Deployment Guide
Prerequisites

Heroku account
Heroku CLI installed
AWS account for S3 storage
Git installed
Python 3.13.0

Setup Instructions

Clone the repository: git clone https://github.com/Alx_DjangoLearnLab/social_media_api.git

Install dependencies: pip install -r requirements.txt

Set up AWS S3 bucket for media storage

Create Heroku app: heroku create your-app-name

Set environment variables:
heroku config:set SECRET_KEY="your-secure-secret-key"
heroku config:set DEBUG=False
heroku config:set AWS_ACCESS_KEY_ID="your-aws-key-id"
heroku config:set AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
heroku config:set AWS_STORAGE_BUCKET_NAME="your-bucket-name"
heroku config:set AWS_S3_REGION_NAME="us-east-1"


Add PostgreSQL: heroku addons:create heroku-postgresql:hobby-dev

Collect static files: python manage.py collectstatic

Deploy: git push heroku main

Run migrations: heroku run python manage.py migrate


Live URL

Deployed at: https://your-app-name.herokuapp.com/

Maintenance

Monitor logs: heroku logs --tail
Update dependencies regularly: pip install -r requirements.txt --upgrade
Check Heroku Dashboard for performance metrics
Backup database periodically: heroku pg:backups:capture

Testing

Test all endpoints using Postman with the live URL
Verify authentication, posts, comments, follows, likes, and notifications
Ensure media files are correctly served from S3
Check HTTPS redirection and security headers

Troubleshooting

If static files fail to load, verify STATICFILES_STORAGE and run collectstatic
If database errors occur, check DATABASE_URL and run migrations
For media file issues, verify AWS credentials and bucket permissions
