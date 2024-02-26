# Anime Recommendation Program
Anime recommendation program powered by the [AniList API](https://anilist.gitbook.io/anilist-apiv2-docs/). It takes in an anime and a rating, finds users who rated that anime the same, and recommends a new anime based off the most common highly rated anime among those users.

# How to run
Download `anilist.py`

Navigate to the working directory of `anilist.py`

Run the python script with the command `python3 anilist.py`
> If you don't have Python 3 installed, install [here](https://www.python.org/downloads/).

That's it!

# Auth
To use this program, no authentication is required. AniList does support OAuth if you need to make changes to AniList data. Read more [here](https://anilist.gitbook.io/anilist-apiv2-docs/overview/oauth).

# Notes
The AniList API runs on GraphQL queries. 

Searching for highly rated anime means the user rated it greater than 9/10.

The rate limit for this API is 90 requests per minute, which is very low. So, the user data to crowdsource from had to be limited severly.

The program queries users starting from the earliest user IDs, capping at 50 currently. 

Lines 117 and 118 are commented out, but they support the functionality to query more users when there aren't enough to aggregate. With the rate limit, allowing this causes many prompts to fail, but feel free to play around with it.

# Resources
[AniList GraphQL Documentation](https://anilist.github.io/ApiV2-GraphQL-Docs/)

[Rate Limiting Information](https://anilist.gitbook.io/anilist-apiv2-docs/overview/rate-limiting)

# Contact
Feel free to ask me questions; I found it difficult to familiarize myself with the API with little resources.

Email: madelinezhang4832@gmail.com
