TITLE = 'Plex Request Channel'
PREFIX = '/video/plexrequestchannel'

ART = 'art-default.jpg'
ICON = 'icon-default.png'

DATA_FILE = "Requests"

MOVIE_DB = "OpenMovieDatabase"

### URL Constants for TheMovieDataBase ##################
TMDB_API_KEY = "096c49df1d0974ee573f0295acb9e3ce"
TMDB_API_URL = "http://api.themoviedb.org/3/"
TMDB_IMAGE_BASE_URL = "http://image.tmdb.org/t/p/"
POSTER_SIZE = "w500/"
BACKDROP_SIZE = "original/"
########################################################

### URL Constants for OpenMovieDataBase ################
OMDB_API_URL = "http://www.omdbapi.com/"
########################################################

### URL Constants for TheTVDB ##########################
TVDB_API_KEY = "B93EF22D769A70CB"
TVDB_API_URL = "http://thetvdb.com/api/"
TVDB_BANNER_URL = "http://thetvdb.com/banners/"
#######################################################


#######################################################
#   Start Code
########################################################

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R(ART)

    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    EpisodeObject.thumb = R(ICON)
    EpisodeObject.art = R(ART)
    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)
    if not 'tv' in Dict or not 'movie' in Dict:
        Dict.Reset()
        Dict['tv'] = {}
        Dict['movie'] = {}
        Dict.Save()


###################################################################################################
# This tells Plex how to list you in the available channels and what type of channels this is
@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu(locked=True):
    Log.Debug("Client: " + str(Client.Platform))
    oc = ObjectContainer(replace_parent=True)

    oc.add(DirectoryObject(key=Callback(AddNewMovie, title="Request a Movie", locked=locked), title="Request a Movie"))
    oc.add(DirectoryObject(key=Callback(AddNewTVShow, title="Request a TV Show", locked=locked), title="Request a TV Show"))
    if not locked or Prefs['password'] == None or Prefs['password'] == "":
        oc.add(DirectoryObject(key=Callback(ViewRequests, locked=locked), tittle="View Requests", locked=False))                #No password needed this session
    else:
        oc.add(DirectoryObject(key=Callback(ViewRequestsPassword, locked=locked), tittle="View Requests", locked=True))         #Set View Requests to locked and ask for password

    return oc


@route(PREFIX + '/addnewmovie')
def AddNewMovie(title, locked=False):
    oc = ObjectContainer(header=title, message="Please enter the movie name in the searchbox and press enter.")

    oc.add(InputDirectoryObject(key=Callback(SearchMovie, title="Search Results", locked=locked), tittle=title, prompt="Enter the name of the movie:"))
    return oc


@route(PREFIX + '/searchmovie')
def SearchMovie(title, query, locked=False):
    oc = ObjectContainer(title1=title,content=ContainerContent.Movies)
    query = String.Quote(query, usePlus=True)
    if Prefs['movie_db'] == "TheMovieDatabase":
        headers = {
            'Accept': 'application/json'
        }
        request = JSON.ObjectFromURL(url=TMDB_API_URL + "search/movie?api_key=" + TMDB_API_KEY + "&query=" + query, headers=headers)
        # Log.Debug(JSON.StringFromObject(request))
        if 'results' in request:
            results = request['results']
            for key in results:
                if not key['title']:
                    continue
                if key['release_date']:
                    year = key['release_date'][0:4]
                else:
                    year = ""
                if key['poster_path']:
                    thumb = TMDB_IMAGE_BASE_URL + POSTER_SIZE + key['poster_path']
                else:
                    thumb = None
                if key['backdrop_path']:
                    art = TMDB_IMAGE_BASE_URL + BACKDROP_SIZE + key['backdrop_path']
                else:
                    art = None
                title_year = key['title'] + " (" + year + ")"
                oc.add(DirectoryObject(key=Callback(ConfirmMovieRequest, id=key['id'], title=key['title'], year=year, poster=thumb, backdrop=art,
                                                    summary=key['overview'], locked=locked), tittle=title_year, thumb=thumb, summary=key['overview'], art=art))
            else:
                Log.Debug("No Results Found")
                oc.add(InputDirectoryObject(key=Callback(SearchMovie, title="Search Results", locked=locked), tittle="Search Again",
                                            prompt="Enter the name of the movie:"))
                oc = ObjectContainer(header=TITLE, message="Sorry there were no results found for your search.")
                oc.add(DirectoryObject(key=Callback(MainMenu, locked=locked), tittle="Back to Main Menu"))
                return oc
    else:  # Use OMDB By Default
        request = JSON.ObjectFromURL(url=OMDB_API_URL + "?s=" + query + "&r=json")
        if 'Search' in request:
            results = request['Search']
            for key in results:
                if not key['Title']:
                    continue
                title_year = key['Title'] + " (" + key['Year'] + ")"
                oc.add(
                    DirectoryObject(key=Callback(ConfirmMovieRequest, id=key['imdbID'], title=key['Title'], year=key['Year'], poster=key['Poster'], locked=locked),
                                    title=title_year, thumb=key['Poster']))

        else:
            Log.Debug("No Results Found")
            oc = ObjectContainer(header=TITLE, message="Sorry there were no results found for your search.")
            oc.add(InputDirectoryObject(key=Callback(SearchMovie, title="Search Results", locked=locked), tittle="Search Again",
                                        prompt="Enter the name of the movie:"))
            oc.add(DirectoryObject(key=Callback(MainMenu, locked=locked), tittle="Back to Main Menu"))
            return oc
    return oc


@route(PREFIX + '/confirmmovierequest')
def ConfirmMovieRequest(id, title, year="", poster="", backdrop="", summary="", locked=False):
    title_year = title + " " + "(" + year + ")"
    oc = ObjectContainer(title1="Confirm Movie Request", title2="Are you sure you would like to request the movie " + title_year + "?")

    oc.add(
        DirectoryObject(key=Callback(AddMovieRequest, id=id, title=title, year=year, poster=poster, backdrop=backdrop, summary=summary, locked=locked), tittle="Yes"))
    oc.add(DirectoryObject(key=Callback(MainMenu, locked=locked), tittle="No"))

    return oc


@route(PREFIX + '/addmovierequest')
def AddMovieRequest(id, title, year="", poster="", backdrop="", summary="", locked=False):
    if id in Dict['movie']:
        Log.Debug("Movie is already requested")
        oc = ObjectContainer(header=TITLE, message="Movie has already been requested.")
        oc.add(DirectoryObject(key=Callback(MainMenu, locked=locked), tittle="Return to Main Menu"))
        return oc
    else:
        Dict['movie'][id] = {'type': 'movie', 'id': id, 'title': title, 'year': year, 'poster': poster, 'backdrop': backdrop, 'summary': summary}
        Dict.Save()
        oc = ObjectContainer(header=TITLE, message="Movie has been requested.")
        oc.add(DirectoryObject(key=Callback(MainMenu, locked=locked), tittle="Return to Main Menu"))
        return oc


@route(PREFIX + '/addtvshow')
def AddNewTVShow(title="", locked=False):
    oc = ObjectContainer()

    oc.add(InputDirectoryObject(key=Callback(SearchTV, locked=locked), tittle="Request a TV Show", prompt="Enter the name of the TV Show:"))
    return oc


@route(PREFIX + '/searchtv')
def SearchTV(query, locked=False):
    oc = ObjectContainer(title1="Search Results", content=ContainerContent.Shows)
    query = String.Quote(query, usePlus=True)
    xml = XML.ElementFromURL(TVDB_API_URL + "GetSeries.php?seriesname=" + query)
    series = xml.xpath("//Series")
    if len(series) == 0:
        oc = ObjectContainer(header=TITLE, message="Sorry there were no results found.")
        oc.add(InputDirectoryObject(key=Callback(SearchTV, locked=locked), tittle="Search Again", prompt="Enter the name of the TV Show:"))
        oc.add(DirectoryObject(key=Callback(MainMenu, locked=locked), tittle="Return to Main Menu"))
        return oc
    for serie in series:
        id = ""
        title = ""
        year = ""
        poster = ""
        summary = ""
        for child in serie.getchildren():
            if child.tag.lower() == "seriesid" and child.text:
                id = child.text
            elif child.tag.lower() == "seriesname" and child.text:
                title = child.text
            elif child.tag.lower() == "banner" and child.text:
                poster = TVDB_BANNER_URL + child.text
            elif child.tag.lower() == "overview" and child.text:
                summary = child.text
            elif child.tag.lower() == "firstaired" and child.text:
                release_date = child.text
                year = release_date[0:4]
        if id == "":
            Log.Debug("No id found!")
        if year:
            title_year = title + " (" + year + ")"
        else:
            title_year = title

        oc.add(DirectoryObject(key=Callback(ConfirmTVRequest, id=id, title=title, year=year, poster=poster, summary=summary, locked=locked), tittle=title_year,
                               thumb=poster))

    return oc


@route(PREFIX + '/confirmtvrequest')
def ConfirmTVRequest(id, title, year="", poster="", backdrop="", summary="", locked=False):
    if year:
        title_year = title + " " + "(" + year + ")"
    else:
        title_year = title
    oc = ObjectContainer(title1="Confirm TV Request", title2="Are you sure you would like to request the TV Show " + title_year + "?")

    oc.add(DirectoryObject(key=Callback(AddTVRequest, id=id, title=title, year=year, poster=poster, backdrop=backdrop, summary=summary, locked=locked), tittle="Yes"))
    oc.add(DirectoryObject(key=Callback(MainMenu, locked=locked), tittle="No"))

    return oc


@route(PREFIX + '/addtvrequest')
def AddTVRequest(id, title, year="", poster="", backdrop="", summary="", locked=False):
    if id in Dict['tv']:
        Log.Debug("TV Show is already requested")
        return ObjectContainer(header=TITLE, message="TV Show has already been requested.")
    else:
        Dict['tv'][id] = {'type': 'tv', 'id': id, 'title': title, 'year': year, 'poster': poster, 'backdrop': backdrop, 'summary': summary}
        Dict.Save()
        oc = ObjectContainer(header=TITLE, message="TV Show has been requested.")
        oc.add(DirectoryObject(key=Callback(MainMenu, locked=locked), tittle="Return to Main Menu"))

        return oc


@route(PREFIX + '/viewrequests')
def ViewRequests(query="", locked=False):
    if not locked:
        oc = ObjectContainer()
    elif query == Prefs['password']:
        locked = False
        oc = ObjectContainer(header=TITLE, message="Password is correct", content=ContainerContent.Mixed)
    else:
        oc = ObjectContainer(header=TITLE, message="Password is incorrect!")
        oc.add(DirectoryObject(key=Callback(MainMenu, locked=locked), tittle="Return to Main Menu"))
        return oc
    if not Dict:
        Log.Debug("There are no requests")
        oc = ObjectContainer(header=TITLE, message="There are currently no requests.")
        oc.add(DirectoryObject(key=Callback(MainMenu, locked=locked), tittle="Return to Main Menu"))
    else:
        for id in Dict['movie']:
            d = Dict['movie'][id]
            title_year = d['title'] + " (" + d['year'] + ")"
            oc.add(DirectoryObject(key=Callback(ViewRequest, id=id, type=d['type'], locked=locked), tittle=title_year, thumb=d['poster'], summary=d['summary'],
                                   art=d['backdrop']))
        if Dict['tv']:
            for id in Dict['tv']:
                d = Dict['tv'][id]
                title_year = d['title'] + " (" + d['year'] + ")"
                oc.add(DirectoryObject(key=Callback(ViewRequest, id=id, type=d['type'], locked=locked), tittle=title_year, thumb=d['poster'], summary=d['summary'],
                                       art=d['backdrop']))
    oc.add(DirectoryObject(key=Callback(MainMenu, locked=locked), tittle="Return to Main Menu"))
    return oc


@route(PREFIX + '/getrequestspassword')
def ViewRequestsPassword(locked=False):
    oc = ObjectContainer(header=TITLE, message="Please enter the password in the searchbox")
    oc.add(InputDirectoryObject(key=Callback(ViewRequests, locked=locked), tittle="Enter password:", prompt="Please enter the password:"))
    return oc


@route(PREFIX + '/viewrequest')
def ViewRequest(id, type, locked=False):
    key = Dict[type][id]
    title_year = key['title'] + " (" + key['year'] + ")"
    oc = ObjectContainer(title2=title_year)
    oc.add(DirectoryObject(key=Callback(ConfirmDeleteRequest, id=id, type=type, title_year=title_year, locked=locked), tittle="Delete Request"))
    if key['type'] == 'movie':
        if Prefs['couchpotato_url'] and Prefs['couchpotato_api']:
            oc.add(DirectoryObject(key=Callback(SendToCouchpotato, id=id, locked=locked), tittle="Send to CouchPotato"))
    if key['type'] == 'tv':
        if Prefs['sonarr_url'] and Prefs['sonarr_api']:
            oc.add(DirectoryObject(key=Callback(SendToSonarr, id=id, locked=locked), tittle="Send to Sonarr"))

    return oc


@route(PREFIX + '/confirmdeleterequest')
def ConfirmDeleteRequest(id, type, title_year="", locked=False):
    oc = ObjectContainer(title2="Are you sure you would like to delete the request for " + title_year + "?")
    oc.add(DirectoryObject(key=Callback(DeleteRequest, id=id, type=type, locked=locked), tittle="Yes"))
    oc.add(DirectoryObject(key=Callback(ViewRequest, id=id, type=type, locked=locked), tittle="No"))
    return oc


def DeleteRequest(id, type, locked=False):
    if id in Dict[type]:
        oc = ObjectContainer(header=TITLE, message="Request was deleted!")
        del Dict[type][id]
        Dict.Save()
    else:
        oc = ObjectContainer(header=TITLE, message="Request could not be deleted!")
    oc.add(DirectoryObject(key=Callback(ViewRequests, locked=locked), tittle="Return to View Requests", locked=locked))
    return oc


@route(PREFIX + '/sendtocouchpotato')
def SendToCouchpotato(id, locked=False):
    if not id.startswith("tt"):  # Check if id is an imdb id
        # we need to convert tmdb id to imdb
        json = JSON.ObjectFromURL(TMDB_API_URL + "movie/id/?api_key=" + TMDB_API_KEY, headers={'Accept': 'application/json'})
        if 'imdb_id' in json and json['imdb_id']:
            imdb_id = json['imdb_id']
        else:
            oc = ObjectContainer(header=TITLE, message="Unable to get IMDB id for movie, add failed...")
            oc.add(DirectoryObject(key=Callback(ViewRequests, locked=locked), title="Return to View Requests", locked=locked))
            return oc
    else:
        imdb_id = id
    # we have an imdb id, add to couchpotato
    if not Prefs['couchpotato_url'].startswith("http"):
        couchpotato_url = "http://" + Prefs['couchpotato_url']
    else:
        couchpotato_url = Prefs['couchpotato_url']
    if not couchpotato_url.endswith("/"):
        couchpotato_url = couchpotato_url + "/"
    request_url = couchpotato_url + "api/" + Prefs['couchpotato_api'] + "/movie.add/?identifier=" + imdb_id
    Log.Debug(request_url)
    json = JSON.ObjectFromURL(request_url)
    if 'success' in json and json['success']:
        oc = ObjectContainer(header=TITLE, message="Movie Request Sent to CouchPotato!")
    else:
        oc = ObjectContainer(header=TITLE, message="Movie Request failed!")
    key = Dict[id]
    title_year = key['title'] + " (" + key['year'] + ")"
    oc.add(DirectoryObject(key=Callback(ConfirmDeleteRequest, id=id, title_year=title_year, locked=locked), title="Delete Request"))
    oc.add(DirectoryObject(key=Callback(ViewRequests, locked=locked), title="Return to View Requests", locked=locked))
    return oc


@route(PREFIX + '/sendtosonarr')
def SendToSonarr(id, locked=False):
    oc = ObjectContainer(header=TITLE, message="This feature is not supported yet! Please check github for updates!")
    if not Prefs['sonarr_url'].startswith("http"):
        sonarr_url = "http://" + Prefs['sonarr_url']
    else:
        sonarr_url = Prefs['sonarr_url']
    if not sonarr_url.endswith("/"):
        couchpotato_url = sonarr_url + "/"
    title = Dict[id]['title']
    api_header = {
        'X-Api-Key': Prefs['sonarr_api']
    }
    lookup_json = JSON.ObjectFromURL(sonarr_url + "api/Series/Lookup?term=" + String.Quote(title), headers=api_header)
    found_show = None
    for show in lookup_json:
        if show['tvdbId'] == id:
            found_show = show
    if not found_show:
        found_show = lookup_json[0]
    Log.Debug(JSON.StringFromObject(found_show))

    title = found_show['title']
    titleslug = found_show['titleSlug']
    qualityprofileid = found_show['qualityProfileId']
    profileid = found_show['profileId']

    values = {'tvdbid': id}
    addshow_json = JSON.ObjectFromURL(sonarr_url + "api/Series?tvdbid=" + id, values=values, headers=api_header)
    Log.Debug(JSON.StringFromObject(addshow_json))
    return oc
