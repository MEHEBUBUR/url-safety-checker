# Deploying URL Safety Checker to Heroku

This guide provides step-by-step instructions for deploying the URL Safety Checker to Heroku.

## Prerequisites

- Git installed on your computer
- Heroku account (sign up at [https://signup.heroku.com/](https://signup.heroku.com/))
- Heroku CLI installed (download from [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli))

## Step 1: Prepare Your Application

Your application is already prepared for deployment with:
- `Procfile` - Tells Heroku how to run your application
- `requirements.txt` - Lists all Python dependencies
- Production settings in `app.py`

## Step 2: Login to Heroku

Open a terminal or command prompt and login to Heroku:

```
heroku login
```

Follow the prompts to complete the login process.

## Step 3: Create a Heroku App

Create a new Heroku application:

```
heroku create urlsafetychecker
```

You can replace "urlsafetychecker" with your preferred app name. If you don't specify a name, Heroku will assign a random name.

## Step 4: Initialize Git Repository

If your project is not already a Git repository:

```
git init
git add .
git commit -m "Initial commit"
```

## Step 5: Deploy to Heroku

Push your code to Heroku:

```
git push heroku main
```

If your default branch is named "master" instead of "main", use:

```
git push heroku master
```

## Step 6: Open Your Application

Once deployment is complete, open your application in a web browser:

```
heroku open
```

## Step 7: Monitor Your Application

You can view the logs to monitor your application:

```
heroku logs --tail
```

## Updating Your Application

When you make changes to your application:

1. Commit your changes:
   ```
   git add .
   git commit -m "Description of changes"
   ```

2. Push to Heroku:
   ```
   git push heroku main
   ```

## Troubleshooting

- **Application Error**: Check logs with `heroku logs --tail`
- **Dependencies Issues**: Make sure all dependencies are in `requirements.txt`
- **Port Binding Error**: Ensure your app uses the PORT environment variable

## Additional Resources

- [Heroku Dev Center](https://devcenter.heroku.com/)
- [Flask on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) 