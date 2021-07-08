## Python Tips Navigator API

This API's data is based off of the [python_tips_lookup](https://github.com/DeeStarks/python_tips_lookup) database.

### Setup

- Install requirements: `pip install -r requirements.txt`
- Add your DB credentials to `.env` file in the base directory - `./python_tips_api/`.
- Create a `.env` file in the base directory and add the required variables:
```
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
```

### Features and Usage

NB: Adding tips only sends data to the database. It does not send data to the web form created by [@python_tip](https://twitter.com/python_tip) because the algorithm written to submit post requests to the form is returning a response from google drive. Funny right? Haha, I know. It has been commented out in the code.

- `GET /tips` - Get all tips
- `GET /tips/<int:tip_id>` - Get a specific tip
- `POST /tips/add` - Create a new tip

    > Object should be in the format:
    > ```json
    > {
    >     "tip": "",
    >     "poster": "",
    >     "poster_email": ""
    > }
    > ```
    > Note: "poster_email" is optional, while "tip" and "poster" is required.
    
- `PUT /tips/update/<int:tip_id>` - Update a specific tip
- `DELETE /tips/delete/<int:tip_id>` - Delete a specific tip
- An algorithm checks to see matches between the tip and the existing tips database. If the matches found are above a 50% threshold against an existing tip, the algorithm will ignore the new tip and return a message to the user.