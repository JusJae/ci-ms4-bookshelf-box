# Bookshelf Box (Books Subscription Service )

![Bookshelf Box Logo](media/bookshelf_box_logo.png)

> [Live Page](https://bookshelf-box.onrender.com/)

Welcome to Bookshelf Box, your personalized book subscription service! Whether you're an avid reader or looking to discover new genres, Bookshelf Box offers a convenient way to receive curated selections of books delivered directly to your door.

---

### User Stories

1. #### Account Management

 • As a new user, I want to register for an account so that I can access the product log app.
 • As a registered user, I want to log in to the application so that I can manage my product list.
 • As a registered user, I want to reset my password in case I forget it.

1. #### Product Management

 • As a user, I want to add a new product to my list, including its image, so that I can keep track of my products.
 • As a user, I want to view all my products in a list or grid view so that I can easily navigate through them.
 • As a user, I want to update the details of a product, including changing its image, to keep my product information current.
 • As a user, I want to delete a product from my list when I no longer need it.

1. #### Search and Filter

 • As a user, I want to search for a product by its name to quickly find specific products.
 • As a user, I want to filter products by categories to view products of a specific type.
 • As a user, I want to sort products by the date they were added to see recent additions first.

1. #### Navigation and Layout

 • As a user, I want a responsive layout so that I can access the application effectively on both desktop and mobile devices.
 • As a user, I want a fixed bottom footer with relevant links and information.
 • As a user, I want a navigation menu to quickly move between different sections of the application.

1. #### Accessibility

 • As a user with visual impairments, I want the application to be screen-reader friendly so that I can navigate and use the app effectively.
 • As a user with motor impairments, I want to navigate the application using keyboard shortcuts.

1. #### Media Management

 • As a user, I want my uploaded product images to be stored securely and load fast.
 • As a user, I want the application to only accept valid image files to ensure consistency and safety.

1. #### Error Handling and Feedback

 • As a user, I want to receive clear error messages when something goes wrong so that I understand what happened and how to proceed.
 • As a user, I want to receive feedback when my actions (like adding a product) are successful.

---

### Database

### Schema Design

The project was initially created to have the following apps and relationships.

<details>
<summary>Entity Relationship Diagram</summary>

![ER Diagram](media/er_diagram.png)

</details>

---
---

## Design

### Typography

Roboto | Montserrat | san-serif

---

### Colour Scheme

<details>
<summary>Palette</summary>

![Colour scheme](media/color_palette.png)
</details>

The original palette scheme that was intended to be used on this project but as design went on deviated to use the following colors.

- primary-color: #2678b8

- secondary-color: #b66426

---

### Wireframes

Wireframes were designed at the start of this project to map out the site but the site has slightly changed since its original conception to simplify the layout and add different elements and remove unnecessary elements for current features such as a music player.

In addition to not having originally planned to have a custom 404 page but adding it in during the project.

#### Mobile view

<details>
<summary>Mobile View Wireframes</summary>

![Wireframe Mobile Pages](/media/mobile_wireframe.png)

</details>

---

## Features

### Logo and Navigation Bar

- The navbar featured on all pages is fully responsive and changes to a toggler (hamburger menu) on smaller screens and includes links to all pages.

### Footer

- Featured on all pages with social media links and copyright.

### User Login

- Gives a description of the home workout company and the trainer that provides the exercises.

### Books

- A table for all the products that the user has logged in to the application.

### Search Books

- A way for users to search the books list and find a desired book from different categories.

### Subscription

- Provides the user with information about the company including phone number, email and social media links.

### Box Content

- Provides a way for the user to see the subscription options that they have put into their box for them to review before going to the checkout to complete payment.

### Checkout

- Provides a page to allow the user to enter their delivery details and full name and email address in order to create the subscription and then enter their payment details to complete the purchase.

### Future Features

- Subscription Box Reviews
- Password reset
- Image upload not from link

---
---

## Technologies Used

- Python
- Django
- CSS
- HTML
- SQL

- Amazon AWS S3:
    Used for static files and media files storage in production.

- Bootstrap v5.3:
    Bootstrap has been used for overall responsiveness of the website, and for the layout to include navigation, cards, and footer within the relevant sections of the website.

- Visual Studio Code:
    Used as the IDE application with Git for version control of this project.

- GitHub:
    GitHub has been used to create a repository to host the project and receive updated commits from Visual Studio Code.

- Figma:
    Used to create the wireframes for the site to help with the basic structure and layout.

- Coolors:
    This online colour palette selector tool was used to see what colours would work well on the site.

- ChatGPT:
    Used to design the logo.

- Freepik:
    Used throughout the site as copyright and royalty-free stock images and videos.

- Google Fonts:
    The fonts were selected from and imported to style the text on the site.

- Font Awesome:
    Font Awesome was used to apply icons in the Exercises page and Footer section.

- SendGrid API:
    Used for email sending when in production.

- Supabase:
    Used as the managed PostgreSQL database host in production.

- Render:
    Used as the cloud platform to deploy and host the web application.

---
---

## Testing

[MS4 Testing](/testing.md)

---
---

## Deployment

This project was originally deployed to [Heroku](https://www.heroku.com/) using a free relational database from [ElephantSQL](https://www.elephantsql.com/) during the Code Institute Web Application Development course. Following the closure of ElephantSQL and changes to Heroku's free tier, the project has since been migrated and is now deployed to [Render](https://render.com/) using a managed PostgreSQL database from [Supabase](https://supabase.com/).

The deployment process is explained in four parts: setting up the database, configuring AWS S3, setting up SendGrid, and deploying to Render.

### Supabase

1. Go to [supabase.com](https://supabase.com/) and sign in or create a free account.
2. Click **New Project** and fill in the following:
    - **Name:** `bookshelf-box`
    - **Database Password:** Create a strong password and save it securely.
    - **Region:** `EU West 2 (London)`
3. Click **Create Project** and wait approximately 2 minutes for it to initialise.
4. Once ready, click **Connect** at the top of the dashboard.
5. Select the **Session Pooler** connection string. It will look like:

    ```
    postgresql://postgres.[ref]:[YOUR-PASSWORD]@aws-0-eu-west-2.pooler.supabase.com:5432/postgres
    ```

6. Replace `[YOUR-PASSWORD]` with the password set in step 2 and save this URL — you will need it for your environment variables.

### AWS S3

1. Sign in to the [AWS Management Console](https://aws.amazon.com/console/).
2. Go to the S3 service and click **Create bucket**.
3. Name your bucket and choose a region, then click **Create bucket**.
4. Configure the bucket for public access:
    - Go to the **Permissions** tab.
    - Edit **Block public access** settings and uncheck **Block all public access**.
    - Save changes.
5. Configure the bucket for static website hosting:
    - Under **Properties > Static website hosting**, enable it.
    - Set `index.html` as the index document.
    - Save the changes.
6. Set up CORS policy under **Permissions > CORS**:

    ```json
    [
        {
            "AllowedHeaders": ["Authorization"],
            "AllowedMethods": ["GET"],
            "AllowedOrigins": ["*"],
            "ExposeHeaders": []
        }
    ]
    ```

7. Set up a bucket policy:
    - Under **Permissions > Bucket Policy**, click **Generate Bucket Policy**.
    - Choose S3 Bucket Policy as the Type of Policy.
    - Enter `*` for Principal and your bucket's ARN.
    - Add Statement, Generate Policy, copy the JSON and paste it into the Edit Bucket Policy field.
    - Save the changes.
8. Configure the Access Control List (ACL):
    - Under **Access Control List**, for Everyone (public access), tick **List**.
    - Accept the warning and save changes.

#### Setting up AWS IAM

1. From the IAM dashboard, select **User Groups**:
    - Create a new group (e.g., `manage-bookshelf-box`).
    - Click through without adding a policy and create the group.
2. Create and attach a policy:
    - Go to **Policies > Create policy**.
    - Under the JSON tab, click **Import managed policy** and choose `AmazonS3FullAccess`.
    - Edit the resource to include your bucket's ARN:

        ```json
        "Resource": [
            "arn:aws:s3:::bookshelf-box",
            "arn:aws:s3:::bookshelf-box/*"
        ]
        ```

    - Give the policy a name (e.g., `bookshelf-box-policy`) and create it.
3. Attach the policy to the user group:
    - Go back to **User Groups**, choose the group created above.
    - Under **Permissions > Add permissions**, attach the policy just created.
4. Create an IAM user:
    - Under **Users**, create a new user (e.g., `bookshelf-box-admin-user`).
    - Select **Programmatic access**.
    - Add the user to the group created above.
    - Download the `.csv` file containing the access key and secret access key. **This file will NOT be available to download again.**

#### Connecting Django to S3

1. Packages are already included in `requirements.txt`:

    ```
    boto3
    django-storages
    ```

2. In your Render environment variables (see Render section below), add:
    - `AWS_ACCESS_KEY_ID`
    - `AWS_SECRET_ACCESS_KEY`
    - `USE_AWS` set to `True`
3. In your S3 bucket, create a folder called `media` and upload any required media files, ensuring they are publicly accessible under Permissions.

### SendGrid

1. Sign up for a free account at [SendGrid](https://sendgrid.com/).
2. Navigate to **Settings > API Keys > Create API Key**.
3. Name your API key, assign it full access, and click **Create & View** to see your key. Copy it for later use.
4. The `sendgrid` package is already included in `requirements.txt`.
5. Add `SENDGRID_API_KEY` and `DEFAULT_FROM_EMAIL` to your Render environment variables (see below).

### Local Development

1. Clone the repository:

    ```shell
    git clone https://github.com/YOUR-USERNAME/ci-ms4-bookshelf-box.git
    cd ci-ms4-bookshelf-box
    ```

2. Create and activate a virtual environment:

    ```shell
    python3.11 -m venv .venv
    source .venv/bin/activate
    ```

3. Install dependencies:

    ```shell
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root with the following:

    ```
    SECRET_KEY=your-secret-key-here
    DEBUG=True
    DATABASE_URL=your-supabase-session-pooler-url
    STRIPE_PUBLIC_KEY=pk_test_...
    STRIPE_SECRET_KEY=sk_test_...
    STRIPE_WH_SECRET=whsec_...
    SENDGRID_API_KEY=SG....
    DEFAULT_FROM_EMAIL=hello@yourdomain.com
    DEVELOPMENT=True
    ```

    > ⚠️ Never commit your `.env` file to GitHub. Make sure `.env` is listed in your `.gitignore`.

5. Run migrations:

    ```shell
    python manage.py migrate
    ```

6. Load books data:

    ```shell
    python manage.py import_books books/fixtures/ms4_books_dataset_170.csv
    ```

7. Load subscription options:

    ```shell
    python manage.py load_subscription_options subscriptions/fixtures/subscription_options.json
    ```

8. Create a superuser:

    ```shell
    python manage.py createsuperuser
    ```

9. Run the development server:

    ```shell
    python manage.py runserver
    ```

### Render

1. Ensure the following files exist in your project root:

    **`build.sh`**

    ```bash
    #!/usr/bin/env bash
    set -o errexit

    pip install -r requirements.txt
    python manage.py collectstatic --no-input
    python manage.py migrate
    python manage.py import_books books/fixtures/ms4_books_dataset_170.csv
    python manage.py load_subscription_options subscriptions/fixtures/subscription_options.json
    ```

2. Log in to [Render](https://render.com/) and click **New > Web Service**.
3. Connect your GitHub repository and select the correct repo.
4. Configure the service settings:

    | Setting | Value |
    |---|---|
    | **Environment** | Python |
    | **Build Command** | `./build.sh` |
    | **Start Command** | `gunicorn bookshelf_box.wsgi:application` |

5. Add the following environment variables under **Environment**:

    | Key | Value |
    |---|---|
    | `DATABASE_URL` | Your Supabase Session Pooler URI |
    | `SECRET_KEY` | Your Django secret key |
    | `DEBUG` | `False` |
    | `STRIPE_PUBLIC_KEY` | Your Stripe public key |
    | `STRIPE_SECRET_KEY` | Your Stripe secret key |
    | `STRIPE_WH_SECRET` | Your Stripe webhook secret |
    | `AWS_ACCESS_KEY_ID` | Your AWS access key |
    | `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |
    | `USE_AWS` | `True` |
    | `SENDGRID_API_KEY` | Your SendGrid API key |
    | `DEFAULT_FROM_EMAIL` | Your verified sender email |

6. Click **Create Web Service**. Render will automatically build and deploy your app.
7. Once deployed, open the **Shell** tab in Render and create a superuser:

    ```shell
    python manage.py createsuperuser
    ```

8. Click **Open App** to view your live site.

---
---

## Credits

### Books Dataset

by Santosh Kumar from [Kaggle](https://www.kaggle.com/datasets/kuchhbhi/treding-book-dataset?resource=download)

**Data Source:** The book data in this dataset was scraped from the [Books to Scrape](https://books.toscrape.com/) website. This source provides a diverse collection of books from various genres, making it an excellent resource for data analysis and research within the literary domain.

**Original Data Columns (Total 12 Columns):**

1. **Title:** The title of the book.
2. **Category:** The category or genre to which each book belongs.
3. **Image:** URLs or references to images associated with the books.
4. **Rating:** The rating or review score of the book.
5. **Description:** A brief description or summary of the book's content.
6. **UPC (Universal Product Code):** A unique product identifier for each book.
7. **Product Type:** The type or format of the book.
8. **Price (excl. tax):** The price of the book without taxes.
9. **Price (incl. tax):** The price of the book including taxes.
10. **Tax:** The tax amount associated with the book.
11. **Availability:** Information about the book's availability for purchase.
12. **Number of Reviews:** The number of reviews provided by readers.

**Used Data Columns**

1. **Title:** The title of the book.
2. **Category:** Categories used - Children's, Nonfiction, Fiction, Horror, Fantasy, Young Adult, Classics.
3. **Image**
4. **Rating**
5. **Description**
6. **Price (incl. tax)**
7. **Availability**
8. **Number of Reviews**

### Images & Videos

[Freepik](https://www.freepik.com/)

[UnSplash](https://www.unsplash.com)

### Code

- Components on the site courtesy of [Bootstrap 5.3](https://getbootstrap.com/docs/4.6/):
  - Navigation Bar Toggle Dropdown Menu

---
---

## Acknowledgements

Thanks to the following people for your help and support in completing this site for the Milestone Project 4 in completion of the Web Application Developmental Diploma delivered by the Code Institute.

- Mentor - Dick Vlad...
- Slack CI Community

_This is a fabricated company for the purposes of this project._

 #readme, #ms4, #ci
