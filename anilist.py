import requests
from collections import Counter;

url = 'https://graphql.anilist.co'

def search_anime(search) :
    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (id: $id, search: $search, type: ANIME) {
                id
                title {
                    romaji
                    english
                }
            }
        }
    }
    '''
    variables = {
        'search': search,
        'page': 1,
        'perPage': 3
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.json().get('data').get('Page').get('media')

def search_users_query(page, mediaId) :
    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $mediaId: Int) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            mediaList (id: $id, mediaId: $mediaId, type: ANIME) {
                userId
                score(format: POINT_10_DECIMAL)
            }
        }
    }
    '''
    variables = {
        'page': page,
        'perPage': 50,
        'mediaId': mediaId
    }
    return requests.post(url, json={'query': query, 'variables': variables})

def get_anime_from_id(id) :
    query = '''
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
            title {
                english
            }
        }
    }
    '''
    variables = {
        'id': id
    }
    return requests.post(url, json={'query': query, 'variables': variables})

def get_top_anime_query(userId) :
    query = '''
    query ($userId: Int) {
        MediaListCollection (userId: $userId, type: ANIME) {
            lists {
                entries {
                    mediaId
                    score(format: POINT_10_DECIMAL)
                }
            
            }
        }
    }
    '''
    variables = {
        'userId': userId #886565
    }
    return requests.post(url, json={'query': query, 'variables': variables})

def aggregate_users(users, mediaId, anime) :
    topAnime = [];
    for user in users :
        response = get_top_anime_query(user)
        entries = response.json().get('data').get('MediaListCollection').get('lists')[0].get('entries')
        for media in entries :
            if(float(media.get('score')) > 9 and media.get('mediaId') != mediaId):
                topAnime.append(media.get('mediaId'))
    if(len(topAnime) == 0) :
        print("It seems like these user(s) haven't rated any other anime highly. Perhaps try again with a more common rating.")
        rate(mediaId, anime)
    else :
        occurence_count = Counter(topAnime)
        return occurence_count.most_common(1)[0][0]

users = [];
def search_users(iteration, mediaId, rating) :
    response = search_users_query(iteration, mediaId);
    mediaList = response.json().get('data').get('Page').get('mediaList')
    for media in mediaList :
        if(float(media.get('score')) == rating) :
            users.append(media.get('userId'))

    # if(len(users) < 10 and iteration < 3 and response.json().get('data').get('Page').get('pageInfo').get('hasNextPage')):
    #     search_users(iteration + 1, mediaId, rating)
    return users

def search_enough_users(mediaId, rating, anime) :
    users = search_users(1, mediaId, rating)
    print ("I found " + str(len(users)) + " user(s) who also rated " + anime + " " + str(rating) + " out of 10.")
    if(len(users) <= 0) :
        print ("Unfortunately, that's not enough users to make an accurate recommendation. Perhaps try again with a more common rating.")
        rate(mediaId, anime)
    else :
        print ("\nNow, I'll search for an anime that these user(s) commonly rated highly.")
        rec = aggregate_users(users, mediaId, anime)
        recName = get_anime_from_id(rec).json().get('data').get('Media').get('title').get('english')
        print("Thanks for your patience. According to my calculations, this is an anime that you will probably enjoy: " + recName)

def rate(id, anime) :
    rating = input("Great! How would you rate this anime from 1 to 10? ")
    try :
        rating = float(rating)
        if(rating < 1 or rating > 10 or len(str(rating).split('.', 1)[1]) != 1) :
            raise ValueError
        print("Okay, let me search for users who also rated " + anime + " " + str(rating) + " out of 10.")
        search_enough_users(id, rating, anime)
    except ValueError:
        print("Please enter a number between 1 and 10, with only one decimal point.")
        rate(id, anime)


def start() :
    search = input("Let's start with the anime you'd like to rate. What's its name? ")
    searchOutput = search_anime(search)
    if(len(searchOutput) == 0) :
        print("Sorry, I couldn't find that anime. Make sure it is searchable on AniList.")
        start()
    else :
        yesNo = input("I see. Just to be sure, you're talking about " + searchOutput[0].get('title').get('english') + ", right? Yes or no? ")
        if(yesNo.lower() == "yes" or yesNo.lower() == "y"):
            rate(searchOutput[0].get('id'), searchOutput[0].get('title').get('english'))
        else :
            print("Alright, try again, making sure it's searchable on AniList.")
            start()

print("\nWelcome to my anime recommendation program powered by the AniList API!")
print("Based off what you rate a certain anime, I'll search for users with the same taste and recommend you a new anime.\n")
try :
    start()
    print("\nThank you for using my program! If you're unsatisfied with this recommendation, try again with different prompts. Happy watching!")
except :
    print("Sorry, something went wrong. The rate limit for the AniList API is 90 requests per minute. You can wait for one minute or try a more common anime or rating.")



