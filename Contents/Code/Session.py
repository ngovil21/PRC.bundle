# coding=utf-8

from DumbTools import DumbKeyboard, MESSAGE_OVERLAY_CLIENTS

import re,urllib2,ssl
import traceback

# Override Plex L, F functions
from LocalePatch import L, F

TITLE = 'Plex Request Channel'
PREFIX = '/video/plexrequestchannel'

ART = 'art-default.jpg'
ICON = 'plexrequestchannel.png'

VERSION = "0.8.0"
BRANCH = "MASTER"
CHANGELOG_URL = "https://raw.githubusercontent.com/ngovil21/PlexRequestChannel.bundle/master/CHANGELOG"

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
########################################################

### Notification Constants #############################
PUSHBULLET_API_URL = "https://api.pushbullet.com/v2/"
PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"
PUSHOVER_API_KEY = "ajMtuYCg8KmRQCNZK2ggqaqiBw2UHi"
PUSHALOT_API_URL = "https://pushalot.com/api/sendmessage"
########################################################

TV_SHOW_OBJECT_FIX_CLIENTS = ["Android", "Plex for Android"]

COMMON_MEDIA_PROBLEMS = ["Subtitles Missing", "Audio Problems", "Media Would Not Start", "File Not Available"]

LANGUAGE_ABBREVIATIONS = {
    "English": "en",
    "Espanol": "es",
    "Francais": "fr",
    "Deutsch": "de",
    "Italiano": "it",
    "Chinese": "zh",
    "Nederlands": "nl",
    "Svenska": "sv",
    "Norsk": "no",
    "Dansk": "da",
    "Suomeksi": "fi",
    "Polski": "pl",
    "Magyar": "hu",
    "Greek": "el",
    "Turkish": "tr",
    "Russian": "ru",
    "Hebrew": "he",
    "Japanese": "ja",
    "Portuguese": "pt",
    "Czech": "cs",
    "Slovenian": "sl",
    "Croatian": "hr",
    "Korean": "ko"
}


class Session:
    def __init__(self, session_id):
        self.locked = True
        try:
            HTTP.Request("127.0.0.1:32400/library")
        except:
            pass
        Route.Connect(PREFIX + '/%s/mainmenu' % session_id, self.SMainMenu)
        Route.Connect(PREFIX + '/%s/register' % session_id, self.Register)
        Route.Connect(PREFIX + '/%s/switchkeyboard' % session_id, self.SwitchKeyboard)
        Route.Connect(PREFIX + '/%s/registername' % session_id, self.RegisterName)
        Route.Connect(PREFIX + '/%s/addnewmovie' % session_id, self.AddNewMovie)
        Route.Connect(PREFIX + '/%s/searchmovie' % session_id, self.SearchMovie)
        Route.Connect(PREFIX + '/%s/confirmmovierequest' % session_id, self.ConfirmMovieRequest)
        Route.Connect(PREFIX + '/%s/addmovierequest' % session_id, self.AddMovieRequest)
        Route.Connect(PREFIX + '/%s/addnewtvshow' % session_id, self.AddNewTVShow)
        Route.Connect(PREFIX + '/%s/searchtv' % session_id, self.SearchTV)
        Route.Connect(PREFIX + '/%s/confirmtvrequest' % session_id, self.ConfirmTVRequest)
        Route.Connect(PREFIX + '/%s/addtvrequest' % session_id, self.AddTVRequest)
        Route.Connect(PREFIX + '/%s/addnewmusic' % session_id, self.AddNewMusic)
        Route.Connect(PREFIX + '/%s/newmusicsearch' % session_id, self.NewMusicSearch)
        Route.Connect(PREFIX + '/%s/searchmusic' % session_id, self.SearchMusic)
        Route.Connect(PREFIX + '/%s/confirmmusicrequest' % session_id, self.ConfirmMusicRequest)
        Route.Connect(PREFIX + '/%s/addmusicrequest' % session_id, self.AddMusicRequest)
        Route.Connect(PREFIX + '/%s/viewrequests' % session_id, self.ViewRequests)
        Route.Connect(PREFIX + '/%s/viewmovierequests' % session_id, self.ViewMovieRequests)
        Route.Connect(PREFIX + '/%s/viewtvrequests' % session_id, self.ViewTVRequests)
        Route.Connect(PREFIX + '/%s/viewmusicrequests' % session_id, self.ViewMusicRequests)
        Route.Connect(PREFIX + '/%s/viewrequestspassword' % session_id, self.ViewRequestsPassword)
        Route.Connect(PREFIX + '/%s/confirmdeleterequests' % session_id, self.ConfirmDeleteRequests)
        Route.Connect(PREFIX + '/%s/clearrequests' % session_id, self.ClearRequests)
        Route.Connect(PREFIX + '/%s/viewrequest' % session_id, self.ViewRequest)
        Route.Connect(PREFIX + '/%s/confirmdeleterequest' % session_id, self.ConfirmDeleteRequest)
        Route.Connect(PREFIX + '/%s/deleterequest' % session_id, self.DeleteRequest)
        Route.Connect(PREFIX + '/%s/sendtocouchpotato' % session_id, self.SendToCouchpotato)
        Route.Connect(PREFIX + '/%s/managecouchpotato' % session_id, self.ManageCouchpotato)
        Route.Connect(PREFIX + '/%s/managecouchpotatomovie' % session_id, self.ManageCouchPotatoMovie)
        Route.Connect(PREFIX + '/%s/deletecouchpotatomovie' % session_id, self.DeleteCouchPotatoMovie)
        Route.Connect(PREFIX + '/%s/sendtosonarr' % session_id, self.SendToSonarr)
        Route.Connect(PREFIX + '/%s/managesonarr' % session_id, self.ManageSonarr)
        Route.Connect(PREFIX + '/%s/managesonarrshow' % session_id, self.ManageSonarrShow)
        Route.Connect(PREFIX + '/%s/managesonarrseason' % session_id, self.ManageSonarrSeason)
        Route.Connect(PREFIX + '/%s/sonarrmonitorshow' % session_id, self.SonarrMonitorShow)
        Route.Connect(PREFIX + '/%s/sonarrshowexists' % session_id, self.SonarrShowExists)
        Route.Connect(PREFIX + '/%s/sendtosickbeard' % session_id, self.SendToSickbeard)
        Route.Connect(PREFIX + '/%s/managesickbeard' % session_id, self.ManageSickbeard)
        Route.Connect(PREFIX + '/%s/managesickbeardshow' % session_id, self.ManageSickbeardShow)
        Route.Connect(PREFIX + '/%s/managesickbeardseason' % session_id, self.ManageSickbeardSeason)
        Route.Connect(PREFIX + '/%s/sickbeardmonitorshow' % session_id, self.SickbeardMonitorShow)
        Route.Connect(PREFIX + '/%s/sickbeardshowexists' % session_id, self.SickbeardShowExists)
        Route.Connect(PREFIX + '/%s/sendtoheadphones' % session_id, self.SendToHeadphones)
        Route.Connect(PREFIX + '/%s/managechannel' % session_id, self.ManageChannel)
        Route.Connect(PREFIX + '/%s/manageusers' % session_id, self.ManageUsers)
        Route.Connect(PREFIX + '/%s/manageuser' % session_id, self.ManageUser)
        Route.Connect(PREFIX + '/%s/renameuser' % session_id, self.RenameUser)
        Route.Connect(PREFIX + '/%s/registerusername' % session_id, self.RegisterUserName)
        Route.Connect(PREFIX + '/%s/blockuser' % session_id, self.BlockUser)
        Route.Connect(PREFIX + '/%s/sonarruser' % session_id, self.SonarrUser)
        Route.Connect(PREFIX + '/%s/deleteuser' % session_id, self.DeleteUser)
        Route.Connect(PREFIX + '/%s/resetdict' % session_id, self.ResetDict)
        Route.Connect(PREFIX + '/%s/changelog' % session_id, self.Changelog)
        Route.Connect(PREFIX + '/%s/toggledebug' % session_id, self.ToggleDebug)
        Route.Connect(PREFIX + '/%s/reportproblem' % session_id, self.ReportProblem)
        Route.Connect(PREFIX + '/%s/navigatemedia' % session_id, self.NavigateMedia)
        Route.Connect(PREFIX + '/%s/reportproblemmedia' % session_id, self.ReportProblemMedia)
        Route.Connect(PREFIX + '/%s/reportproblemmediaother' % session_id, self.ReportProblemMediaOther)
        Route.Connect(PREFIX + '/%s/reportgeneralproblem' % session_id, self.ReportGeneralProblem)
        Route.Connect(PREFIX + '/%s/confirmreportproblem' % session_id, self.ConfirmReportProblem)
        Route.Connect(PREFIX + '/%s/notifyproblem' % session_id, self.NotifyProblem)
        Route.Connect(PREFIX + '/%s/showmessage' % session_id, self.ShowMessage)
        self.token = Request.Headers.get("X-Plex-Token", "")
        self.is_admin = checkAdmin(self.token)
        self.platform = Client.Platform
        self.product = Client.Product
        self.use_dumb_keyboard = isClient(DumbKeyboard.CLIENTS)
        Log.Debug("Platform: " + str(self.platform))
        Log.Debug("Product: " + str(self.product))
        Log.Debug("Accept-Language: " + str(Request.Headers.get('Accept-Language')))

    # @handler(PREFIX, TITLE, art=ART, thumb=ICON)
    def SMainMenu(self, message=None, title1=TITLE, title2="Main Menu"):
        oc = ObjectContainer(replace_parent=True, title1=title1, title2=title2, view_group="List")

        if isClient(MESSAGE_OVERLAY_CLIENTS):
            oc.message = message
        if self.is_admin:
            Log.Debug("User is Admin")
        if self.is_admin:
            if self.token in Dict['register']:  # Do not save admin token in the register
                del Dict['register'][self.token]
        elif Dict['register'] and (self.token not in Dict['register'] or not Dict['register'][self.token]['nickname']):
            return self.Register()
        elif self.token not in Dict['register']:
            Dict['register'][self.token] = {'nickname': "", 'requests': 0}
            Dict.Save()
        register_date = Datetime.FromTimestamp(Dict['register_reset'])
        if (register_date + Datetime.Delta(days=7)) < Datetime.Now():
            resetRegister()
        if self.use_dumb_keyboard:  # Clients in this list do not support InputDirectoryObjects
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchMovie, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Request a Movie"),
                         message=L("Enter the name of the Movie"))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchTV, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Request a TV Show"),
                         message=L("Enter the name of the TV Show"))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchMusic, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Request an Album"),
                         message=L("Enter the name of the Album"))
        elif Client.Product == "Plex Web":  # Plex Web does not create a popup input directory object, so use an intermediate menu
            if Prefs['movierequests']:
                oc.add(DirectoryObject(key=Callback(self.AddNewMovie, title=L("Request a Movie")),
                                       title=L("Request a Movie")))
            if Prefs['tvrequests']:
                oc.add(DirectoryObject(key=Callback(self.AddNewTVShow), title=L("Request a TV Show")))
            if Prefs['musicrequests']:
                oc.add(DirectoryObject(key=Callback(self.NewMusicSearch, searchtype="release", searchstr="Album"),
                                       title=L("Request an Album")))
        else:  # All other clients
            if Prefs['movierequests']:
                oc.add(InputDirectoryObject(key=Callback(self.SearchMovie), title=L("Request a Movie"),
                                            prompt=L("Enter the name of the Movie")))
            if Prefs['tvrequests']:
                oc.add(InputDirectoryObject(key=Callback(self.SearchTV), title=L("Request a TV Show"),
                                            prompt=L("Enter the name of the TV Show")))
            if Prefs['musicrequests']:
                oc.add(InputDirectoryObject(key=Callback(self.SearchMusic, searchtype="release", searchstr="Album"),
                                            title=L("Request an Album"),
                                            prompt=L("Enter the name of the Album"),
                                            thumb=R('search.png')))

        if Prefs['usersviewrequests'] or self.is_admin:
            if not self.locked or Prefs['password'] is None or Prefs['password'] == "":
                if self.locked:
                    self.locked = False
                oc.add(DirectoryObject(key=Callback(self.ViewRequests),
                                       title=L("View Requests")))  # No password needed this session
            else:
                oc.add(DirectoryObject(key=Callback(self.ViewRequestsPassword),
                                       title=L("View Requests")))  # Set View Requests to locked and ask for password
        else:
            oc.add(DirectoryObject(key=Callback(self.ViewRequests, token_hash=Hash.SHA1(self.token)),
                                   title=L("View My Requests")))
        if Prefs['couchpotato_api'] and (self.is_admin or self.token in Dict['sonarr_users']):
            oc.add(DirectoryObject(key=Callback(self.ManageCouchpotato), title=F("managesickbeard", "Couchpotato")))
        if Prefs['sonarr_api'] and (self.is_admin or self.token in Dict['sonarr_users']):
            oc.add(DirectoryObject(key=Callback(self.ManageSonarr), title=F("managesickbeard", "Sonarr")))
        if Prefs['sickbeard_api'] and (self.is_admin or self.token in Dict['sonarr_users']):
            oc.add(DirectoryObject(key=Callback(self.ManageSickbeard),
                                   title=F("managesickbeard", str(Prefs['sickbeard_fork']))))
        oc.add(DirectoryObject(key=Callback(self.ReportProblem), title=L("Report a Problem")))
        if self.is_admin:
            oc.add(DirectoryObject(key=Callback(self.ManageChannel), title=L("Manage Channel")))
        elif not Dict['register'][self.token]['nickname']:
            oc.add(DirectoryObject(
                key=Callback(self.Register,
                             message=L("Entering your name will let the admin know who you are when making requests.")),
                title=L("Register Device")))
        oc.add(DirectoryObject(key=Callback(self.SwitchKeyboard),
                               title=L(
                                   'Switch to Device Keyboard' if self.use_dumb_keyboard else 'Switch to Alternate Keyboard')))

        return oc

    def Register(self, message=None):
        url = "https://plex.tv"
        try:
            xml = XML.ObjectFromURL(url, headers={'X-Plex-Token': self.token})
            plexTVUser = xml.get("myPlexUsername")
            Log.Debug("PlexTV Username: " + plexTVUser)
            self.RegisterName(query=plexTVUser)
            return self.SMainMenu(message=L("Your username has been registered."), title1=L("Main Menu"),
                                  title2=L("Registered"))
        except:
            Log.Debug("PlexTV Username: N/A")
        if message is None:
            message = L("Unrecognized device. The admin would like you to register it.")
        if Client.Product == "Plex Web":
            message += L("Enter your name in the searchbox and press enter.")
        if isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(header=TITLE, message=message)
        else:
            Log.Debug("Client does support message overlays")
            oc = ObjectContainer(title1=L("Unrecognized Device"), title2=L("Please register"))
        if self.use_dumb_keyboard:
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            # oc.add(DirectoryObject(key=Callback(Keyboard, callback=RegisterName, parent_call=Callback(MainMenu,)), title="Enter your name or nickname"))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.RegisterName, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Enter your name or nickname"))
        else:
            oc.add(InputDirectoryObject(key=Callback(self.RegisterName), title=L("Enter your name or nickname"),
                                        prompt=L("Enter your name or nickname")))
        return oc

    def RegisterName(self, query=""):
        if not query:
            return self.Register(message=L("You must enter a name. Try again."))
        Dict['register'][self.token] = {'nickname': query, 'requests': 0}
        Dict.Save()
        return self.SMainMenu(message=L("Your device has been registered."), title1=L("Main Menu"),
                              title2=L("Registered"))

    def SwitchKeyboard(self):
        self.use_dumb_keyboard = not self.use_dumb_keyboard
        return self.SMainMenu("Keyboard has been changed")

    def AddNewMovie(self, title=None):
        if title is None:
            title = L("Request a Movie")
        Log.Debug("Client does support message overlays")
        oc = ObjectContainer(title2="Enter Movie")
        if Prefs['weekly_limit'] and int(Prefs['weekly_limit'] > 0) and not self.is_admin:
            if self.token in Dict['register'] and Dict['register'][self.token]['requests'] >= int(
                    Prefs['weekly_limit']):
                return self.SMainMenu(message=F("weeklylimit", Prefs['weekly_limit']),
                                      title1=L("Main Menu"), title2=L("Weekly Limit"))
        if Client.Product == "Plex Web":
            oc = ObjectContainer(header=TITLE,
                                 message=L("Please enter the movie name in the searchbox and press enter."))
            oc.add(DirectoryObject(key=Callback(self.AddNewMovie, title=title),
                                   title=L("Please enter the movie name in the searchbox and press enter.")))
        if self.use_dumb_keyboard:
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            # oc.add(DirectoryObject(key=Callback(Keyboard, callback=SearchMovie, parent_call=Callback(MainMenu,)), title=title, thumb=R('search.png')))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchMovie, parent_call=Callback(self.SMainMenu),
                         dktitle=title,
                         message=L("Enter the name of the Movie"), dkthumb=R('search.png'))
        else:
            oc.add(
                InputDirectoryObject(key=Callback(self.SearchMovie), title=L('title'),
                                     prompt=L("Enter the name of the Movie:"),
                                     thumb=R('search.png')))
        return oc

    def SearchMovie(self, query=""):
        oc = ObjectContainer(title1=L("Search Results"), title2=query, content=ContainerContent.Shows,
                             view_group="Details")
        query = String.Quote(query, usePlus=True)
        if Prefs['weekly_limit'] and int(Prefs['weekly_limit']) > 0 and not self.is_admin:
            if Dict['register'].get(self.token, None) and Dict['register'][self.token]['requests'] >= int(
                    Prefs['weekly_limit']):
                return self.SMainMenu(message=F("weeklylimit", Prefs['weekly_limit']),
                                      title1=L("Main Menu"), title2=L("Weekly Limit"))
        if self.token in Dict['blocked']:
            return self.SMainMenu(message=L("Sorry you have been blocked."), title1=L("Main Menu"),
                                  title2=L("User Blocked"))
        if Prefs['movie_db'] == "TheMovieDatabase":
            headers = {
                'Accept': 'application/json'
            }
            request = JSON.ObjectFromURL(
                url=TMDB_API_URL + "search/movie?api_key=" + TMDB_API_KEY + "&language=" + LANGUAGE_ABBREVIATIONS.get(
                    Prefs["search_language"],
                    "en") + "&query=" + query,
                headers=headers)
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
                    title_year = key['title']
                    title_year += (" (" + key['year'] + ")" if key.get('year', None) else "")
                    oc.add(TVShowObject(
                        key=Callback(self.ConfirmMovieRequest, movie_id=key['id'], source='TMDB', title=key['title'],
                                     year=year, poster=thumb,
                                     backdrop=art,
                                     summary=key['overview']), rating_key=key['id'], title=title_year, thumb=thumb,
                        summary=key['overview'], art=art))
            else:
                if isClient(MESSAGE_OVERLAY_CLIENTS):
                    oc = ObjectContainer(header=TITLE, message=L("Sorry there were no results found for your search."))
                else:
                    oc = ObjectContainer(title2=L("No results"))
                Log.Debug("No Results Found")
                if self.use_dumb_keyboard:
                    Log.Debug("Client does not support Input. Using DumbKeyboard")
                    # oc.add(DirectoryObject(key=Callback(Keyboard, callback=SearchMovie, parent_call=Callback(MainMenu,)), title="Search Again",
                    #                        thumb=R('search.png')))
                    DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchMovie, parent_call=Callback(self.SMainMenu),
                                 dktitle=L("Search Again"),
                                 message=L("Enter the name of the Movie"), dkthumb=R('search.png'))
                else:
                    oc.add(InputDirectoryObject(key=Callback(self.SearchMovie), title=L("Search Again"),
                                                prompt=L("Enter the name of the Movie:")))
                oc.add(
                    DirectoryObject(key=Callback(self.SMainMenu), title=L("Back to Main Menu"), thumb=R('return.png')))
                return oc
        else:  # Use OMDB By Default
            request = JSON.ObjectFromURL(url=OMDB_API_URL + "?s=" + query + "&r=json")
            if 'Search' in request:
                results = request['Search']
                for key in results:
                    if not key['Title']:
                        continue
                    if 'type' in key and not (key['type'] == "movie"):  # only show movie results
                        continue
                    title_year = key['Title']
                    title_year += (" (" + key['Year'] + ")" if key.get('Year', None) else "")
                    if key['Poster']:
                        thumb = key['Poster']
                    else:
                        thumb = R('no-poster.jpg')
                    oc.add(TVShowObject(
                        key=Callback(self.ConfirmMovieRequest, movie_id=key['imdbID'], title=key['Title'],
                                     source='IMDB', year=key['Year'],
                                     poster=key['Poster']), rating_key=key['imdbID'], title=title_year, thumb=thumb))
            else:
                Log.Debug("No Results Found")
                if isClient(MESSAGE_OVERLAY_CLIENTS):
                    oc = ObjectContainer(header=TITLE, message=L("Sorry there were no results found for your search."))
                else:
                    oc = ObjectContainer(title2="No results")
                if self.use_dumb_keyboard:
                    Log.Debug("Client does not support Input. Using DumbKeyboard")
                    # oc.add(DirectoryObject(key=Callback(Keyboard, callback=SearchMovie, parent_call=Callback(MainMenu,)), title="Search Again",
                    #                        thumb=R('search.png')))
                    DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchMovie, parent_call=Callback(self.SMainMenu),
                                 dktitle=L("Search Again"),
                                 message="Enter the name of the Movie", dkthumb=R('search.png'))
                else:
                    oc.add(InputDirectoryObject(key=Callback(self.SearchMovie), title=L("Search Again"),
                                                prompt=L("Enter the name of the Movie:"),
                                                thumb=R('search.png')))
                oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"),
                                       thumb=R('return.png')))
                return oc
        if self.use_dumb_keyboard:
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            # oc.add(DirectoryObject(key=Callback(Keyboard, callback=SearchMovie, parent_call=Callback(MainMenu,)), title="Search Again",
            #                        thumb=R('search.png')))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchMovie, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Search Again"),
                         message="Enter the name of the Movie", dkthumb=R('search.png'))
        else:
            oc.add(InputDirectoryObject(key=Callback(self.SearchMovie), title=L("Search Again"),
                                        prompt=L("Enter the name of the Movie:"), thumb=R('search.png')))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
        return oc

    def ConfirmMovieRequest(self, movie_id, title, source='', year="", poster="", backdrop="", summary=""):
        title_year = title + " (" + year + ")" if year else title
        if isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(title1=L("Confirm Movie Request"), title2=title_year + "?", header=TITLE,
                                 message=F("requestmovie", title_year))
        else:
            oc = ObjectContainer(title1=L("Confirm Movie Request"), title2=title_year + "?")
        found_match = False
        try:
            local_search = XML.ElementFromURL(url="http://127.0.0.1:32400/search?local=1&query=" + String.Quote(title),
                                              headers=Request.Headers)
            if local_search:
                videos = local_search.xpath("//Video")
                for video in videos:
                    if video.attrib['title'] == title and video.attrib['year'] == year and video.attrib[
                        'type'] == 'movie':
                        Log.Debug("Possible match found: " + str(video.attrib['ratingKey']))
                        summary = "(In Library: " + video.attrib['librarySectionTitle'] + ") " + (
                            video.attrib['summary'] if video.attrib['summary'] else "")
                        oc.add(TVShowObject(
                            key=Callback(self.SMainMenu, message=L("Movie already in library."), title1=L("In Library"),
                                         title2=title),
                            rating_key=video.attrib['ratingKey'], title="+ " + title, summary=summary,
                            thumb=video.attrib['thumb']))
                        found_match = True
                        break
        except:
            pass
        if found_match:
            if isClient(MESSAGE_OVERLAY_CLIENTS) or 'Samsung' in Client.Product or 'Samsung' in Client.Platform:
                oc.message = L(
                    "Movie appears to already exist in the library. Are you sure you would still like to request it?")
            else:
                oc.title1 = L("Movie Already Exists")
        if not found_match and Client.Platform in TV_SHOW_OBJECT_FIX_CLIENTS:  # If an android, add an empty first item because it gets truncated for some reason
            oc.add(DirectoryObject(key=None, title=""))
        if not found_match and Client.Product == "Plex Web":  # If Plex Web then add an item with the poster
            oc.add(TVShowObject(
                key=Callback(self.ConfirmMovieRequest, movie_id=movie_id, title=title, source=source, year=year,
                             poster=poster, backdrop=backdrop,
                             summary=summary), rating_key=movie_id, thumb=poster, summary=summary, title=title_year))
        oc.add(DirectoryObject(
            key=Callback(self.AddMovieRequest, movie_id=movie_id, source=source, title=title, year=year, poster=poster,
                         backdrop=backdrop,
                         summary=summary), title=L("Add Anyways") if found_match else L("Yes"), thumb=R('check.png')))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("No"), thumb=R('x-mark.png')))

        return oc

    def AddMovieRequest(self, movie_id, title, source='', year="", poster="", backdrop="", summary=""):
        if movie_id in Dict['movie']:
            Log.Debug("Movie is already requested")
            return self.SMainMenu(message=L("Movie has already been requested"), title1=title,
                                  title2=L("Already Requested"))
        else:
            user = "Admin" if self.is_admin else ""
            if self.token in Dict['register']:
                Dict['register'][self.token]['requests'] = Dict['register'][self.token]['requests'] + 1
                user = userFromToken(self.token)
            title_year = title
            title_year += (" (" + year + ")" if year else "")
            Dict['movie'][movie_id] = {'type': 'movie', 'id': movie_id, 'source': source, 'title': title, 'year': year,
                                       'title_year': title_year,
                                       'poster': poster, 'backdrop': backdrop, 'summary': summary, 'user': user,
                                       'token_hash': Hash.SHA1(self.token),
                                       'automated': False}
            Dict.Save()
            if Prefs['couchpotato_autorequest']:
                self.SendToCouchpotato(movie_id)
            notifyRequest(req_id=movie_id, req_type='movie')
            return self.SMainMenu(message=L("Movie has been requested"), title1=L("Main Menu"),
                                  title2=L("Movie Requested"))

    # TVShow Functions
    def AddNewTVShow(self, title=None):
        if title is None:
            title = L("Request a TV Show")
        if Prefs['weekly_limit'] and int(Prefs['weekly_limit'] > 0) and not self.is_admin:
            if self.token in Dict['register'] and Dict['register'][self.token]['requests'] >= int(
                    Prefs['weekly_limit']):
                return self.SMainMenu(message=F("weeklylimit", Prefs['weekly_limit']),
                                      title1=L("Main Menu"), title2=L("Weekly Limit"))
        if self.token in Dict['blocked']:
            return self.SMainMenu(message=L("Sorry you have been blocked."),
                                  title1=L("Main Menu"), title2=L("User Blocked"))
        if Client.Product == "Plex Web":
            oc = ObjectContainer(header=TITLE,
                                 message=L("Please enter the name of the TV Show in the search box and press enter."))
            oc.add(DirectoryObject(key=Callback(self.AddNewTVShow, title=title),
                                   title=L("Please enter the name of the TV Show in the search box and press enter.")))
        else:
            oc = ObjectContainer(title2=title)
        if self.use_dumb_keyboard:
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            # oc.add(DirectoryObject(key=Callback(Keyboard, callback=SearchTV, parent_call=Callback(MainMenu,)), title="Request a TV Show",
            #                        thumb=R('search.png')))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchTV, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Request a TV Show"),
                         message=L("Enter the name of the TV Show"), dkthumb=R('search.png'))
        else:
            oc.add(InputDirectoryObject(key=Callback(self.SearchTV), title=L("Request a TV Show"),
                                        prompt=L("Enter the name of the TV Show"),
                                        thumb=R('search.png')))
        return oc

    def SearchTV(self, query):
        if Prefs['weekly_limit'] and int(Prefs['weekly_limit'] > 0) and not self.is_admin:
            if self.token in Dict['register'] and Dict['register'][self.token]['requests'] >= int(
                    Prefs['weekly_limit']):
                return self.SMainMenu(message=F("weeklylimit", Prefs['weekly_limit']),
                                      title1=L("Main Menu"), title2=L("Weekly Limit"))
        oc = ObjectContainer(title1=L("Search Results"), title2=query, content=ContainerContent.Shows,
                             view_group="Details")
        query = String.Quote(query, usePlus=True)
        xml = XML.ElementFromURL(
            TVDB_API_URL + "GetSeries.php?seriesname=" + query + "&language=" + LANGUAGE_ABBREVIATIONS.get(
                Prefs["search_language"], "en"))
        series = xml.xpath("//Series")
        if len(series) == 0:
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc = ObjectContainer(header=TITLE, message=L("Sorry there were no results found for your search."))
            else:
                oc = ObjectContainer(title2=L("No results"))
            if self.use_dumb_keyboard:
                Log.Debug("Client does not support Input. Using DumbKeyboard")
                # oc.add(DirectoryObject(key=Callback(Keyboard, callback=SearchTV, parent_call=Callback(MainMenu,)), title="Search Again",
                #                        thumb=R('search.png')))
                DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchTV, parent_call=Callback(self.SMainMenu),
                             dktitle=L("Search Again"),
                             message=L("Enter the name of the TV Show"), dkthumb=R('search.png'))
            else:
                oc.add(InputDirectoryObject(key=Callback(self.SearchTV), title=L("Search Again"),
                                            prompt=L("Enter the name of the TV Show:"),
                                            thumb=R('search.png')))
            oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
            return oc
        count = 0
        for serie in series:
            series_id = ""
            title = ""
            year = ""
            poster = ""
            summary = ""
            for child in serie.getchildren():
                if child.tag.lower() == "seriesid" and child.text:
                    series_id = child.text
                elif child.tag.lower() == "seriesname" and child.text:
                    title = child.text
                elif child.tag.lower() == "banner" and child.text and not poster:
                    poster = TVDB_BANNER_URL + child.text
                elif child.tag.lower() == "overview" and child.text:
                    summary = child.text
                elif child.tag.lower() == "firstaired" and child.text:
                    release_date = child.text
                    year = release_date[0:4]
                elif child.tag.lower() == "poster" and child.text:
                    poster = TVDB_BANNER_URL + child.text
            if count < 11:  # Let's look for the actual poster for only the first 10 tv shows to reduce api hits
                try:
                    serie_page = XML.ElementFromURL(TVDB_API_URL + TVDB_API_KEY + "/series/" + series_id)
                    poster_text = serie_page.xpath("//Series/poster/text()")
                    if poster_text:
                        poster = TVDB_BANNER_URL + poster_text[0]
                except Exception as e:
                    if Dict['debug']:
                        Log.Error(str(traceback.format_exc()))
                        # raise e
                    Log.Debug(e)
                count += 1
            if series_id == "":
                Log.Debug("No id found!")
            if year:
                title_year = title + " (" + year + ")"
            else:
                title_year = title
            if poster:
                thumb = poster
            else:
                thumb = R('no-poster.jpg')
            oc.add(
                TVShowObject(
                    key=Callback(self.ConfirmTVRequest, series_id=series_id, source='TVDB', title=title, year=year,
                                 poster=poster, summary=summary,
                                 ),
                    rating_key=series_id, title=title_year, summary=summary, thumb=thumb))
        if self.use_dumb_keyboard:
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            # oc.add(
            # DirectoryObject(key=Callback(Keyboard, callback=SearchTV, parent_call=Callback(MainMenu,)), title="Search Again", thumb=R('search.png')))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchTV, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Search Again"),
                         message=L("Enter the name of the TV Show"), dkthumb=R('search.png'))
        else:
            oc.add(InputDirectoryObject(key=Callback(self.SearchTV), title=L("Search Again"),
                                        prompt=L("Enter the name of the TV Show"),
                                        thumb=R('search.png')))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
        return oc

    def ConfirmTVRequest(self, series_id, title, source="", year="", poster="", backdrop="", summary=""):
        title_year = title + " " + "(" + year + ")" if year else title

        if isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(title1="Confirm TV Request", title2=F("confirmtvrequest", title_year),
                                 header=TITLE, message=F("requesttv", title_year))
        else:
            oc = ObjectContainer(title1=L("Confirm TV Request"), title2=title_year + "?")

        found_match = False
        try:
            local_search = XML.ElementFromURL(url="http://127.0.0.1:32400/search?local=1&query=" + String.Quote(title),
                                              headers=Request.Headers)
            if local_search:
                videos = local_search.xpath("//Directory")
                for video in videos:
                    video_attr = video.attrib
                    if video_attr['title'] == title and video_attr['year'] == year and video_attr['type'] == 'show':
                        Log.Debug("Possible match found: " + str(video_attr['ratingKey']))
                        summary = "(In Library: " + video_attr['librarySectionTitle'] + ") " + (
                            video_attr['summary'] if video_attr['summary'] else "")
                        oc.add(
                            TVShowObject(
                                key=Callback(self.SMainMenu, message=L("TV Show already in library."),
                                             title1=L("In Library"), title2=title),
                                rating_key=video_attr['ratingKey'], title="+ " + title, summary=summary,
                                thumb=video_attr['thumb']))
                        found_match = True
                        break
        except:
            pass
        if found_match:
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc.message = L(
                    "TV Show appears to already exist in the library. Are you sure you would still like to request it?")
            else:
                oc.title1 = L("Show Already Exists")

        if not found_match and Client.Platform in TV_SHOW_OBJECT_FIX_CLIENTS:  # If an android, add an empty first item because it gets truncated for some reason
            oc.add(DirectoryObject(key=None, title=""))
        if not found_match and Client.Product == "Plex Web":  # If Plex Web then add an item with the poster
            oc.add(TVShowObject(
                key=Callback(self.ConfirmTVRequest, series_id=series_id, title=title, source=source, year=year,
                             poster=poster, backdrop=backdrop,
                             summary=summary), rating_key=series_id, thumb=poster, summary=summary, title=title_year))
        oc.add(DirectoryObject(
            key=Callback(self.AddTVRequest, series_id=series_id, source=source, title=title, year=year, poster=poster,
                         backdrop=backdrop,
                         summary=summary,
                         ), title=L("Add Anyways") if found_match else L("Yes"), thumb=R('check.png')))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("No"), thumb=R('x-mark.png')))

        return oc

    def AddTVRequest(self, series_id, title, source='', year="", poster="", backdrop="", summary=""):
        if series_id in Dict['tv']:
            Log.Debug("TV Show is already requested")
            return self.SMainMenu(message=L("TV Show has already been requested"), title1=title,
                                  title2=L("Already Requested"))
        else:
            user = "Admin" if self.is_admin else ""
            if self.token in Dict['register']:
                Dict['register'][self.token]['requests'] = Dict['register'][self.token]['requests'] + 1
                user = userFromToken(self.token)
            Dict['tv'][series_id] = {'type': 'tv', 'id': series_id, 'source': source, 'title': title, 'year': year,
                                     'poster': poster,
                                     'backdrop': backdrop, 'summary': summary, 'user': user,
                                     'token_hash': Hash.SHA1(self.token), 'automated': False}
            Dict.Save()
            notifyRequest(req_id=series_id, req_type='tv')
            if Prefs['sonarr_autorequest'] and Prefs['sonarr_url'] and Prefs['sonarr_api']:
                return self.SendToSonarr(tvdbid=series_id,
                                         callback=Callback(self.SMainMenu, message=L("TV Show has been requested"),
                                                           title1=title,
                                                           title2=L("Requested")))
            if Prefs['sickbeard_autorequest'] and Prefs['sickbeard_url'] and Prefs['sickbeard_api']:
                return self.SendToSickbeard(tvdbid=series_id,
                                            callback=Callback(self.SMainMenu, message=L("TV Show has been requested"),
                                                              title1=title,
                                                              title2=L("Requested")))
            return self.SMainMenu(message=L("TV Show has been requested"), title1=title, title2=L("Requested"))

            # TVShow Functions

    def AddNewMusic(self, title=None):
        if title is None:
            title = L("Request Music")
        if Prefs['weekly_limit'] and int(Prefs['weekly_limit'] > 0) and not self.is_admin:
            if self.token in Dict['register'] and Dict['register'][self.token]['requests'] >= int(
                    Prefs['weekly_limit']):
                return self.SMainMenu(message=F("weeklylimit", Prefs['weekly_limit']),
                                      title1=L("Main Menu"), title2=L("Weekly Limit"))
        if self.token in Dict['blocked']:
            return self.SMainMenu(message=L("Sorry you have been blocked."),
                                  title1=L("Main Menu"), title2=L("User Blocked"))
        oc = ObjectContainer()
        if Client.Product == "Plex Web":
            oc.add(DirectoryObject(key=Callback(self.NewMusicSearch, searchtype="artist", searchstr="Artist"),
                                   title=L("Search Artist")))
            oc.add(DirectoryObject(key=Callback(self.NewMusicSearch, searchtype="release", searchstr="Album"),
                                   title=L("Search Album")))
            oc.add(DirectoryObject(key=Callback(self.NewMusicSearch, searchtype="recording", searchstr="Song"),
                                   title=L("Search Song")))
        elif self.use_dumb_keyboard:
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            # oc.add(DirectoryObject(key=Callback(Keyboard, callback=SearchTV, parent_call=Callback(MainMenu,)), title="Request a TV Show",
            #                        thumb=R('search.png')))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchMusic, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Search Artist"),
                         message=L("Enter the name of the Artist"), dkthumb=R('search.png'), searchtype="artist")
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchMusic, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Search Album"),
                         message=L("Enter the name of the Album"), dkthumb=R('search.png'), searchtype="release")
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchMusic, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Search Song"),
                         message=L("Enter the name of the Song"), dkthumb=R('search.png'), searchtype="recording")
        else:
            oc.add(InputDirectoryObject(key=Callback(self.SearchMusic, searchtype="artist", searchstr="Artist"),
                                        title=L("Search Artist"),
                                        prompt=L("Enter the name of the artist"),
                                        thumb=R('search.png')))
            oc.add(InputDirectoryObject(key=Callback(self.SearchMusic, searchtype="release", searchstr="Album"),
                                        title=L("Search Album"),
                                        prompt=L("Enter the name of the album"),
                                        thumb=R('search.png')))
            oc.add(InputDirectoryObject(key=Callback(self.SearchMusic, searchtype="recording", searchstr="Song"),
                                        title=L("Search Song"),
                                        prompt=L("Enter the name of the song"),
                                        thumb=R('search.png')))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
        return oc

    def NewMusicSearch(self, searchtype, searchstr):
        if Prefs['weekly_limit'] and int(Prefs['weekly_limit'] > 0) and not self.is_admin:
            if self.token in Dict['register'] and Dict['register'][self.token]['requests'] >= int(
                    Prefs['weekly_limit']):
                return self.SMainMenu(message=F("weeklylimit", Prefs['weekly_limit']),
                                      title1=L("Main Menu"), title2=L("Weekly Limit"))
        if self.token in Dict['blocked']:
            return self.SMainMenu(message=L("Sorry you have been blocked."),
                                  title1=L("Main Menu"), title2=L("User Blocked"))
        if Client.Product == "Plex Web":
            oc = ObjectContainer(header=TITLE,
                                 message=F("Please enter the name of the %s in the searchbox and press enter.",
                                           searchstr))
            oc.add(DirectoryObject(key=Callback(self.NewMusicSearch, searchtype=searchtype, searchstr=searchstr),
                                   title=F("Please enter the %s in the searchbox and press enter.", searchstr)))
        else:
            oc = ObjectContainer(title2=searchstr)
        if self.use_dumb_keyboard:
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchMusic, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Request Music"),
                         message=L("Enter the name of the " + searchtype), dkthumb=R('search.png'),
                         searchtype=searchtype)
        else:
            oc.add(InputDirectoryObject(key=Callback(self.SearchMusic, searchtype=searchtype), title=L("Request Music"),
                                        prompt=L("Enter the name of the " + searchstr),
                                        thumb=R('search.png')))
        return oc

    def SearchMusic(self, query, searchtype="release", searchstr="Album"):
        if Prefs['weekly_limit'] and int(Prefs['weekly_limit'] > 0) and not self.is_admin:
            if self.token in Dict['register'] and Dict['register'][self.token]['requests'] >= int(
                    Prefs['weekly_limit']):
                return self.SMainMenu(message=F("weeklylimit", Prefs['weekly_limit']),
                                      title1=L("Main Menu"), title2=L("Weekly Limit"))
        oc = ObjectContainer(title1=L("Search Results"), title2=query, content=ContainerContent.Shows,
                             view_group="Details")
        query = String.Quote(query, usePlus=True)
        url = "http://musicbrainz.org/ws/2/%s/?query=%s&fmt=json" % (searchtype, query)
        try:
            results = JSON.ObjectFromURL(url)
        except:
            Log.Debug(str(traceback.format_exc()))
            return oc
        searches = results.get("releases")
        for e in searches:
            e_id = e.get('id')
            if not e_id:
                Log("No id - Skipped")
                continue
            e_score = e.get('score', "0")
            if 'title' in e:
                e_name = e.get('title', None)
            else:
                e_name = e.get('name', "")
            e_date = e.get('date', None)
            e_image = None
            # ToDo: Get image for first 10 results
            title = e_name
            if e_date:
                title += " (" + e_date[:4] + ")"
            title += " +" + e_score
            # if searchtype == "artist":
            #     if count < 10:
            #         try:
            #             properties_page = JSON.ObjectFromURL("http://musicbrainz.org/ws/2/%s/%s?inc=url-rels&fmt=json" % (searchtype, e_id))
            #             if 'relations' in properties_page:
            #                 for r in properties_page['relations']:
            #                     if r.get('type') == "image":
            #                         e_image = r.get('url', {}).get('resource', None)
            #         except:
            #             pass
            #     oc.add(ArtistObject(key=Callback(self.ConfirmMusicRequest, searchtype=searchtype, music_id=e_id, music_name=e_name, music_image=e_image), rating_key=e_id, title=title, thumb=e_image))
            # elif searchtype == "release":
            e_image = "http://coverartarchive.org/%s/%s/front-500" % (searchtype, e_id)
            oc.add(ArtistObject(
                key=Callback(self.ConfirmMusicRequest, searchtype=searchtype, music_id=e_id, music_name=e_name,
                             music_date=e_date, music_image=e_image),
                rating_key=e_id, title=title, thumb=e_image))
            # elif searchtype == "recording":
            #     oc.add(SongObject(
            #         key=Callback(self.ConfirmMusicRequest, searchtype=searchtype, music_id=e_id, music_name=e_name, music_date=e_date, music_image=e_image),
            #         rating_key=e_id, title=title, thumb=e_image))
        if self.use_dumb_keyboard:
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            # oc.add(
            # DirectoryObject(key=Callback(Keyboard, callback=SearchTV, parent_call=Callback(MainMenu,)), title="Search Again", thumb=R('search.png')))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.SearchMusic, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Search Again"),
                         message=L("Enter the name of the " + searchtype), dkthumb=R('search.png'),
                         searchtype=searchtype)
        else:
            oc.add(InputDirectoryObject(key=Callback(self.SearchMusic, searchtype=searchtype), title=L("Search Again"),
                                        prompt=L("Enter the name of the " + searchtype),
                                        thumb=R('search.png')))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
        return oc

    def ConfirmMusicRequest(self, searchtype, music_id, music_name, music_date=None, music_image=None):
        if isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(title1="Confirm Music Request", title2=F("confirmmusicrequest", music_name),
                                 header=TITLE, message=F("requestmusic", music_name))
        else:
            oc = ObjectContainer(title1=L("Confirm Movie Request"), title2=music_name + "?")

        oc.add(DirectoryObject(
            key=Callback(self.AddMusicRequest, searchtype=searchtype, music_id=music_id, music_name=music_name,
                         music_date=music_date, music_image=music_image), title=L("Yes"), thumb=R('check.png')))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("No"), thumb=R('x-mark.png')))

        return oc

    def AddMusicRequest(self, searchtype, music_id, music_name, music_date=None, music_image=None):
        title = music_name
        if music_date:
            title += " (" + music_date + ")"
        if music_id in Dict['music']:
            Log.Debug("Music has already been requested")
            return self.SMainMenu(message=L("Music has already been requested"), title1=music_name,
                                  title2=L("Already Requested"))
        else:
            user = "Admin" if self.is_admin else ""
            if self.token in Dict['register']:
                Dict['register'][self.token]['requests'] = Dict['register'][self.token]['requests'] + 1
                user = userFromToken(self.token)
        Dict['music'][music_id] = {'type': 'music', 'id': music_id, 'source': 'musicbrainz', 'title': music_name,
                                   'date': music_date, 'year': music_date[:4], 'poster': music_image,
                                   'user': user, 'token_hash': Hash.SHA1(self.token), 'automated': False}
        Dict.Save()

        notifyRequest(req_id=music_id, req_type='music')

        return self.SMainMenu(message=L("Music has been requested"), title1=title, title2=L("Requested"))

    # Request Functions
    def ViewRequests(self, query="", token_hash=None, message=None):
        oc = ObjectContainer(title2=message)
        if not self.locked:
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc.header = TITLE
                oc.message = message
        elif query == Prefs['password']:
            self.locked = False
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc = ObjectContainer(header=TITLE, message=L("Password is correct"), content=ContainerContent.Mixed)
            else:
                oc = ObjectContainer(title2="Password correct")
        elif not token_hash:
            return self.SMainMenu(message=L("Password incorrect"), title1=L("Main Menu"),
                                  title2=L("Password incorrect"))
        oc.add(DirectoryObject(key=Callback(self.ViewMovieRequests, token_hash=token_hash),
                               title=L("View Movie Requests")))
        oc.add(DirectoryObject(key=Callback(self.ViewTVRequests, token_hash=token_hash),
                               title=L("View TV Requests")))
        oc.add(DirectoryObject(key=Callback(self.ViewMusicRequests, token_hash=token_hash),
                               title=L("View Music Requests")))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R("return.png")))
        return oc

    def ViewRequestsPassword(self):
        oc = ObjectContainer(header=TITLE, message=L("Please enter the password in the searchbox"))
        if self.use_dumb_keyboard:
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            # oc.add(DirectoryObject(key=Callback(Keyboard, callback=ViewRequests, parent_call=Callback(MainMenu,)), title="Enter password:"))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.ViewRequests, parent_call=Callback(self.SMainMenu),
                         dktitle=L("Enter Password"),
                         message=L("Enter password"), dksecure=True)
        else:
            oc.add(InputDirectoryObject(key=Callback(self.ViewRequests), title=L("Enter password"),
                                        prompt=L("Enter password:")))
        return oc

    def ViewMovieRequests(self, token_hash=None):
        oc = ObjectContainer()
        if not Dict['movie']:
            Log.Debug("There are no Movie requests")
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc.message = L("There are currently no movie requests.")
            else:
                oc = ObjectContainer(title1=L("View Movie Requests"), title2=L("No Movie Requests"))
            oc.add(DirectoryObject(key=Callback(self.ViewRequests), title=L("View Requests Menu")))
            oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
            return oc
        else:
            requests = Dict['movie']
            for req_id in sorted(requests, key=lambda k: requests[k]['title']):
                d = requests[req_id]
                if token_hash and token_hash != d.get('token_hash'):
                    continue
                title_year = d['title']
                title_year += (" (" + d['year'] + ")" if d.get('year', None) else "")
                if d.get('automated', False):
                    title_year = "+ " + title_year
                thumb = d.get('poster', R('no-poster.jpg'))
                summary = "(Requested by " + (d.get('user') if d.get('user') else 'Unknown') + ")   " + (
                    d.get('summary', "") if d.get("summary") else "")
                oc.add(TVShowObject(
                    key=Callback(self.ViewRequest, req_id=req_id, req_type=d['type'], token_hash=token_hash),
                    rating_key=req_id,
                    title=title_year, thumb=thumb, summary=summary, art=d.get('backdrop', None)))
            oc.add(DirectoryObject(key=Callback(self.ViewRequests, token_hash=token_hash),
                                   title=L("Return to Requests Menu"),
                                   thumb=R('return.png')))
            oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
            if len(oc) > 1 and self.is_admin:
                oc.add(DirectoryObject(key=Callback(self.ConfirmDeleteRequests, type='movie'),
                                       title=L("Clear All Movie Requests"),
                                       thumb=R('trash.png')))
            return oc

    def ViewTVRequests(self, token_hash=None):
        oc = ObjectContainer()
        if not Dict['tv']:
            Log.Debug("There are no tv requests")
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc.message = L("There are currently no TV requests.")
            else:
                oc = ObjectContainer(title1=L("View TV Requests"), title2=L("No TV Requests"))
            oc.add(DirectoryObject(key=Callback(self.ViewRequests), title=L("View Requests Menu")))
            oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
            return oc
        else:
            requests = Dict['tv']
            for req_id in sorted(requests, key=lambda k: requests[k]['title']):
                d = requests[req_id]
                if token_hash and token_hash != d.get('token_hash'):
                    continue
                title_year = d['title']
                title_year += (" (" + d['year'] + ")" if d.get('year', None) else "")
                if d.get('automated', False):
                    title_year = "+ " + title_year
                thumb = d.get('poster', R('no-poster.jpg'))
                summary = "(Requested by " + (d.get('user') if d.get('user') else 'Unknown') + ")   " + (
                    d.get('summary', "") if d.get("summary") else "")
                oc.add(TVShowObject(
                    key=Callback(self.ViewRequest, req_id=req_id, req_type=d['type'], token_hash=token_hash),
                    rating_key=req_id,
                    title=title_year, thumb=thumb, summary=summary, art=d.get('backdrop', None)))
            oc.add(DirectoryObject(key=Callback(self.ViewRequests, token_hash=token_hash),
                                   title=L("Return to Requests Menu"),
                                   thumb=R('return.png')))
            oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
            if len(oc) > 1 and self.is_admin:
                oc.add(DirectoryObject(key=Callback(self.ConfirmDeleteRequests, type='tv'),
                                       title=L("Clear All TV Requests"), thumb=R('trash.png')))
            return oc

    def ViewMusicRequests(self, token_hash=None):
        oc = ObjectContainer()
        if not Dict['music']:
            Log.Debug("There are no music requests")
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc.message = L("There are currently no Music requests.")
            else:
                oc = ObjectContainer(title1=L("View Music Requests"), title2=L("No Music Requests"))
            oc.add(DirectoryObject(key=Callback(self.ViewRequests), title=L("View Requests Menu")))
            oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
            return oc
        else:
            requests = Dict['music']
            for req_id in sorted(requests, key=lambda k: requests[k]['title']):
                d = requests[req_id]
                if token_hash and token_hash != d.get('token_hash'):
                    continue
                title_year = d['title']
                title_year += (" (" + d['year'] + ")" if d.get('year', None) else "")
                if d.get('automated', False):
                    title_year = "+ " + title_year
                thumb = d.get('poster', R('no-poster.jpg'))
                summary = "(Requested by " + (d.get('user') if d.get('user') else 'Unknown') + ")   "
                oc.add(ArtistObject(
                    key=Callback(self.ViewRequest, req_id=req_id, req_type=d['type'], token_hash=token_hash),
                    rating_key=req_id,
                    title=title_year, thumb=thumb, summary=summary, art=d.get('backdrop', None)))
            oc.add(DirectoryObject(key=Callback(self.ViewRequests, token_hash=token_hash),
                                   title=L("Return to Requests Menu"),
                                   thumb=R('return.png')))
            oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
            if len(oc) > 1 and self.is_admin:
                oc.add(DirectoryObject(key=Callback(self.ConfirmDeleteRequests, type='music'),
                                       title=L("Clear All Music Requests"), thumb=R('trash.png')))
            return oc

    def ConfirmDeleteRequests(self, type):
        oc = ObjectContainer(title2=L("Are you sure you would like to clear all requests?"))
        if Client.Platform in TV_SHOW_OBJECT_FIX_CLIENTS:  # If on android, add an empty first item because it gets truncated for some reason
            oc.add(DirectoryObject(key=None, title=""))
        oc.add(DirectoryObject(key=Callback(self.ClearRequests, type=type), title=L("Yes"), thumb=R('check.png')))
        oc.add(DirectoryObject(key=Callback(self.ViewRequests), title=L("No"), thumb=R('x-mark.png')))
        return oc

    def ClearRequests(self, type):
        if not self.is_admin:
            return self.SMainMenu(L("Only an admin can manage the channel!"), title1=L("Main Menu"),
                                  title2=L("Admin only"))
        Dict[type] = {}
        Dict.Save()
        return self.ViewRequests(message=L("All " + type + " have been cleared"))

    def ViewRequest(self, req_id, req_type, token_hash=None):
        key = Dict[req_type][req_id]
        title_year = key['title']
        title_year += " (" + key.get("year") + ")" if not re.search(" \(/d/d/d/d\)", key['title']) and key['year'] else \
            key['title']  # If there is already a year in the title, just use title
        summary = " (Requested by " + (key.get('user') if key.get('user') else 'Unknown') + ")   " + (
            key.get('summary', "") if key.get('summary') else "")
        oc = ObjectContainer(title2=title_year)
        if Client.Platform in TV_SHOW_OBJECT_FIX_CLIENTS:  # If an android, add an empty first item because it gets truncated for some reason
            oc.add(DirectoryObject(key=None, title=""))
        if Client.Product == "Plex Web":  # If Plex Web then add an item with the poster
            oc.add(TVShowObject(key=Callback(self.ViewRequest, req_id=req_id, req_type=req_type, token_hash=token_hash),
                                rating_key=req_id,
                                thumb=key.get('poster', None),
                                summary=summary, title=title_year))

        Log.Debug("Req Type: " + req_type + "  Key Type: " + key['type'] + "  Req ID: " + req_id)
        if self.is_admin or key.get('token_hash') == Hash.SHA1(self.token):
            oc.add(DirectoryObject(
                key=Callback(self.ConfirmDeleteRequest, req_id=req_id, req_type=req_type, title_year=title_year,
                             token_hash=token_hash),
                title=L("Delete Request"), thumb=R('x-mark.png')))
        if key['type'] == 'movie' and (self.is_admin or Prefs['usersviewrequests']):
            if Prefs['couchpotato_url'] and Prefs['couchpotato_api']:
                oc.add(DirectoryObject(key=Callback(self.SendToCouchpotato, movie_id=req_id),
                                       title=F("sendto", "CouchPotato"),
                                       thumb=R('couchpotato.png')))
        if key['type'] == 'tv' and (self.is_admin or Prefs['usersviewrequests']):
            if Prefs['sonarr_url'] and Prefs['sonarr_api']:
                oc.add(DirectoryObject(key=Callback(self.SendToSonarr, tvdbid=req_id,
                                                    callback=Callback(self.ViewRequest, req_id=req_id, req_type='tv',
                                                                      token_hash=token_hash)),
                                       title=F("sendto", "Sonarr"), thumb=R('sonarr.png')))
            if Prefs['sickbeard_url'] and Prefs['sickbeard_api']:
                oc.add(DirectoryObject(key=Callback(self.SendToSickbeard, tvdbid=req_id,
                                                    callback=Callback(self.ViewRequest, req_id=req_id, req_type='tv',
                                                                      token_hash=token_hash)),
                                       title=F("sendto", Prefs['sickbeard_fork']),
                                       thumb=R(Prefs['sickbeard_fork'].lower() + '.png')))
        if key['type'] == 'music' and (self.is_admin or Prefs['usersviewrequests']):
            if Prefs['headphones_url'] and Prefs['headphones_api']:
                oc.add(DirectoryObject(key=Callback(self.SendToHeadphones, music_id=req_id),
                                       title=F("sendto", "Headphones"),
                                       thumb=R('headphones.png')))
        if req_type == 'movie':
            oc.add(DirectoryObject(key=Callback(self.ViewMovieRequests, token_hash=token_hash),
                                   title=L("Return to Movie Requests"), thumb=R('return.png')))
        elif req_type == 'tv':
            oc.add(DirectoryObject(key=Callback(self.ViewTVRequests, token_hash=token_hash),
                                   title=L("Return to TV Requests"), thumb=R('return.png')))
        elif req_type == 'music':
            oc.add(DirectoryObject(key=Callback(self.ViewMusicRequests, token_hash=token_hash),
                                   title=L("Return to Music Requests"), thumb=R('return.png')))
        return oc

    def ConfirmDeleteRequest(self, req_id, req_type, title_year="", token_hash=None):
        oc = ObjectContainer(title2=F("confirmdelete", title_year))
        if Client.Platform in TV_SHOW_OBJECT_FIX_CLIENTS:  # If an android, add an empty first item because it gets truncated for some reason
            oc.add(DirectoryObject(key=None, title=""))
        oc.add(
            DirectoryObject(key=Callback(self.DeleteRequest, req_id=req_id, req_type=req_type, token_hash=token_hash),
                            title=L("Yes"),
                            thumb=R('check.png')))
        oc.add(DirectoryObject(key=Callback(self.ViewRequest, req_id=req_id, req_type=req_type, token_hash=token_hash),
                               title=L("No"),
                               thumb=R('x-mark.png')))
        return oc

    def DeleteRequest(self, req_id, req_type, token_hash=None):
        if req_id in Dict[req_type]:
            message = L("Request was deleted")
            del Dict[req_type][req_id]
            Dict.Save()
        else:
            message = L("Request could not be deleted")
        return self.ViewRequests(token_hash=token_hash, message=message)

    # CouchPotato Functions
    def SendToCouchpotato(self, movie_id):
        if movie_id not in Dict['movie']:
            return MessageContainer(L("Error"), L("The movie id was not found in the database"))
        movie = Dict['movie'][movie_id]
        if 'source' in movie and movie['source'].upper() == 'TMDB':  # Check if id source is tmdb
            # we need to convert tmdb id to imdb
            json = JSON.ObjectFromURL(TMDB_API_URL + "movie/" + movie_id + "?api_key=" + TMDB_API_KEY,
                                      headers={'Accept': 'application/json'})
            if 'imdb_id' in json and json['imdb_id']:
                imdb_id = json['imdb_id']
            else:
                if isClient(MESSAGE_OVERLAY_CLIENTS):
                    oc = ObjectContainer(header=TITLE, message=L("Unable to get IMDB id for movie, add failed..."))
                else:
                    oc = ObjectContainer(title1="CouchPotato", title2=L("Send Failed"))
                oc.add(DirectoryObject(key=Callback(self.ViewRequests), title=L("Return to View Requests")))
                return oc
        else:  # Assume we have an imdb_id by default
            imdb_id = movie_id
        # we have an imdb id, add to couchpotato
        if not Prefs['couchpotato_url'].startswith("http"):
            couchpotato_url = "http://" + Prefs['couchpotato_url']
        else:
            couchpotato_url = Prefs['couchpotato_url']
        if not couchpotato_url.endswith("/"):
            couchpotato_url += "/"
        values = {'identifier': imdb_id}
        if Prefs['couchpotato_profile']:
            cat = JSON.ObjectFromURL(couchpotato_url + "api/" + Prefs['couchpotato_api'] + "/profile.list/")
            if cat['success']:
                for key in cat['list']:
                    if key['label'] == Prefs['couchpotato_profile']:
                        values['profile_id'] = key['_id']
            else:
                Log.Debug("Unable to open up Couchpotato Profile List")
        if Prefs['couchpotato_category']:
            cat = JSON.ObjectFromURL(couchpotato_url + "api/" + Prefs['couchpotato_api'] + "/category.list/")
            if cat['success']:
                for key in cat['categories']:
                    if key['label'] == Prefs['couchpotato_category']:
                        values['category_id'] = key['_id']
            else:
                Log.Debug("Unable to open up Couchpotato Category List")
        try:
            json = JSON.ObjectFromURL(couchpotato_url + "api/" + Prefs['couchpotato_api'] + "/movie.add/",
                                      values=values)
            if 'success' in json and json['success']:
                if isClient(MESSAGE_OVERLAY_CLIENTS):
                    oc = ObjectContainer(header=TITLE, message=L("Movie Request Sent to CouchPotato!"))
                else:
                    oc = ObjectContainer(title1="Couchpotato", title2=L("Success"))
                Dict['movie'][movie_id]['automated'] = True
                Dict.Save()
            else:
                if isClient(MESSAGE_OVERLAY_CLIENTS):
                    oc = ObjectContainer(header=TITLE, message=L("CouchPotato Send Failed!"))
                else:
                    oc = ObjectContainer(title1="CouchPotato", title2=L("Send Failed"))
        except:
            if Dict['debug']:
                Log.Error(str(traceback.format_exc()))
                # raise e
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc = ObjectContainer(header=TITLE, message=L("CouchPotato Send Failed!"))
            else:
                oc = ObjectContainer(title1="CouchPotato", title2=L("Send Failed"))
        key = Dict['movie'][movie_id]
        title_year = key['title']
        title_year += (" (" + key['year'] + ")" if key.get('year', None) else "")
        if self.is_admin:
            oc.add(DirectoryObject(
                key=Callback(self.ConfirmDeleteRequest, req_id=movie_id, req_type='movie', title_year=title_year),
                title=L("Delete Request")))
        oc.add(DirectoryObject(key=Callback(self.ViewMovieRequests), title=L("Return to Movie Requests")))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu")))
        return oc

    def ManageCouchpotato(self):
        if not Prefs['couchpotato_url'].startswith("http"):
            couchpotato_url = "http://" + Prefs['couchpotato_url']
        else:
            couchpotato_url = Prefs['couchpotato_url']
        if not couchpotato_url.endswith("/"):
            couchpotato_url += "/"
        try:
            movie_list = JSON.ObjectFromURL(couchpotato_url + "api/" + Prefs['couchpotato_api'] + "/movie.list",
                                            values=dict(status="active"))
        except Exception as e:
            if Dict['debug']:
                Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug(e.message)
            return MessageContainer(header=TITLE, message=L("Error loading CouchPotato"))

        oc = ObjectContainer(title2="Manage Couchpotato")

        if movie_list['success'] and not movie_list['empty']:
            for movie in movie_list['movies']:
                title = movie.get('title')
                movie_id = movie.get('_id')
                title_year = title
                movie_info = movie.get('info', {})
                year = movie_info.get('year')
                imdb_id = movie_info.get('imdb', "0")
                poster = movie_info.get('images', {}).get('poster')
                if poster:
                    poster = poster[0]
                summary = movie_info.get('plot')
                title_year += " (" + str(year) + ")" if year else ""
                oc.add(TVShowObject(key=Callback(self.ManageCouchPotatoMovie, movie_id=movie_id, title=title),
                                    rating_key=imdb_id, title=title_year,
                                    thumb=poster, summary=summary))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu")))

        return oc

    def ManageCouchPotatoMovie(self, movie_id, title=""):
        oc = ObjectContainer(title1=L("Manage Couchpotato"), title2=title)
        oc.add(
            DirectoryObject(key=Callback(self.DeleteCouchPotatoMovie, movie_id=movie_id),
                            title=L("Delete from Couchpotato"), thumb=R('trash.png')))
        oc.add(DirectoryObject(key=Callback(self.ManageCouchpotato), title=L("Return to Manage Couchpotato"),
                               thumb=R('return.png')))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
        return oc

    def DeleteCouchPotatoMovie(self, movie_id):
        if not Prefs['couchpotato_url'].startswith("http"):
            couchpotato_url = "http://" + Prefs['couchpotato_url']
        else:
            couchpotato_url = Prefs['couchpotato_url']
        if not couchpotato_url.endswith("/"):
            couchpotato_url += "/"
        try:
            movie_delete = JSON.ObjectFromURL(couchpotato_url + "api/" + Prefs['couchpotato_api'] + "/movie.delete",
                                              values=dict(id=movie_id, delete_from="wanted"))
        except Exception as e:
            if Dict['debug']:
                Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug(e.message)
            return MessageContainer(header=TITLE, message=L("Error loading CouchPotato"))

        if movie_delete['success']:
            return self.ManageCouchpotato()
        else:
            return MessageContainer(header=TITLE, message=L("Could not delete movie from Couchpotato"))

    # Sonarr Methods
    def SendToSonarr(self, tvdbid, callback=None):
        if not Prefs['sonarr_url'].startswith("http"):
            sonarr_url = "http://" + Prefs['sonarr_url']
        else:
            sonarr_url = Prefs['sonarr_url']
        if not sonarr_url.endswith("/"):
            sonarr_url += "/"
        title = Dict['tv'][tvdbid]['title']
        api_header = {
            'X-Api-Key': Prefs['sonarr_api']
        }
        series_id = self.SonarrShowExists(tvdbid)
        if series_id:
            Dict['tv'][tvdbid]['automated'] = True
            Dict.Save()
            return self.ManageSonarrShow(series_id=series_id, callback=callback)
        lookup_json = JSON.ObjectFromURL(sonarr_url + "api/Series/Lookup?term=tvdbid:" + tvdbid, headers=api_header)
        found_show = None
        for show in lookup_json:
            if show['tvdbId'] == series_id:
                found_show = show
        if not found_show:
            found_show = lookup_json[0]

        profile_json = JSON.ObjectFromURL(sonarr_url + "api/Profile", headers=api_header)
        profile_id = 1
        for profile in profile_json:
            if profile['name'] == Prefs['sonarr_profile']:
                profile_id = profile['id']
                break
        rootFolderPath = ""
        if Prefs['sonarr_path']:
            rootFolderPath = Prefs['sonarr_path']
        else:
            root = JSON.ObjectFromURL(sonarr_url + "api/Rootfolder", headers=api_header)
            if root:
                rootFolderPath = root[0]['path']

        #Log.Debug(str(found_show))

        Log.Debug("Profile id: " + str(profile_id))
        options = {'title': found_show['title'], 'tvdbId': found_show['tvdbId'], 'tvRageId': found_show['tvRageId'],
                   'imdbId': found_show['imdbId'], 'cleanTitle': found_show['cleanTitle'], 'images': found_show['images'],
                   'qualityProfileId': int(profile_id), 'titleSlug': found_show['titleSlug'], 'rootFolderPath': rootFolderPath,
                   'seasons': found_show['seasons'], 'monitored': True, 'seasonFolder': Prefs['sonarr_seasonfolder']}

        add_options = {'ignoreEpisodesWithFiles': False,
                       'ignoreEpisodesWithoutFiles': False,
                       'searchForMissingEpisodes': True
                       }

        if Prefs['sonarr_monitor'] == 'manual':
            add_options['ignoreEpisodesWithFiles'] = True
            add_options['ignoreEpisodesWithoutFiles'] = True
        elif Prefs['sonarr_monitor'] == 'all':
            for season in options['seasons']:
                season['monitored'] = True
        elif Prefs['sonarr_monitor'] == 'future':
            add_options['ignoreEpisodesWithFiles'] = True
            add_options['ignoreEpisodesWithoutFiles'] = True
        elif Prefs['sonarr_monitor'] == 'latest':
            options['seasons'][len(options['seasons']) - 1]['monitored'] = True
        elif Prefs['sonarr_monitor'] == 'first':
            options['season'][1]['monitored'] = True
        elif Prefs['sonarr_monitor'] == 'missing':
            add_options['ignoreEpisodesWithFiles'] = True
        elif Prefs['sonarr_monitor'] == 'existing':
            add_options['ignoreEpisodesWithoutFiles'] = True
        elif Prefs['sonarr_monitor'] == 'none':
            options['monitored'] = False
        options['addOptions'] = add_options
        values = JSON.StringFromObject(options)
        try:
            #Log.Debug("Options: " + str(options))
            HTTP.Request(sonarr_url + "api/Series", data=values, headers=api_header)
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc = ObjectContainer(header=TITLE, message=L("Show has been sent to Sonarr"))
            else:
                oc = ObjectContainer(title1="Sonarr", title2=L("Success"))
            Log.Debug("Setting series automated to true")
            Dict['tv'][tvdbid]['automated'] = True
            Dict.Save()
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug("Options: " + str(options))
            Log.Debug(e.message)
            Log.Debug("Response Status: " + str(Response.Status))
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc = ObjectContainer(header=TITLE, message=L("Could not send show to Sonarr!"))
            else:
                oc = ObjectContainer(title1="Sonarr", title2=L("Send Failed"))
        if Prefs['sonarr_monitor'] == "manual":
            Thread.Sleep(1)
            series_id = self.SonarrShowExists(tvdbid)
            if series_id:
                return self.ManageSonarrShow(series_id, title=title, callback=callback)
        if self.is_admin:
            oc.add(DirectoryObject(
                key=Callback(self.ConfirmDeleteRequest, req_id=series_id, req_type='tv', title_year=title),
                title=L("Delete Request"), thumb=R('trash.png')))
        if callback:
            oc.add(DirectoryObject(key=callback, title=L("Return"), thumb=R('return.png')))
        else:
            oc.add(DirectoryObject(key=Callback(self.ViewTVRequests), title=L("Return to TV Requests"),
                                   thumb=R('return.png')))
            oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"),
                                   thumb=R('plexrequestchannel.png')))
        return oc

    def ManageSonarr(self):
        oc = ObjectContainer(title1=TITLE, title2="Manage Sonarr")
        if not Prefs['sonarr_url'].startswith("http"):
            sonarr_url = "http://" + Prefs['sonarr_url']
        else:
            sonarr_url = Prefs['sonarr_url']
        if sonarr_url.endswith("/"):
            sonarr_url = sonarr_url[:-1]
        api_header = {
            'X-Api-Key': Prefs['sonarr_api']
        }
        try:
            shows = JSON.ObjectFromURL(sonarr_url + "/api/Series", headers=api_header)
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug(e.message)
            return MessageContainer(header=TITLE, message=L("Error retrieving Sonarr Shows"))
        for show in shows:
            poster = None
            for image in show['images']:
                if image['coverType'] == 'poster':
                    try:
                        poster = sonarr_url + "/api" + image['url'][image['url'].find('/MediaCover/'):] + "&apikey=" + \
                                 Prefs['sonarr_api']
                    except Exception:
                        Log.Error(str(traceback.format_exc()))  # raise e
            oc.add(TVShowObject(key=Callback(self.ManageSonarrShow, series_id=show['id'], title=show['title']),
                                rating_key=show.get('tvdbId', 0),
                                title=show['title'], thumb=poster, summary=show.get('overview', "")))
        oc.objects.sort(key=lambda obj: obj.title.lower())
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu")))
        return oc

    def ManageSonarrShow(self, series_id, title="", callback=None, message=None):
        if not Prefs['sonarr_url'].startswith("http"):
            sonarr_url = "http://" + Prefs['sonarr_url']
        else:
            sonarr_url = Prefs['sonarr_url']
        if sonarr_url.endswith("/"):
            sonarr_url = sonarr_url[:-1]
        api_header = {
            'X-Api-Key': Prefs['sonarr_api']
        }
        try:
            show = JSON.ObjectFromURL(sonarr_url + "/api/Series/" + str(series_id), headers=api_header)
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug(e.message)
            return MessageContainer(header=TITLE, message=F("errorsonarrshow", title))
        if isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(title1=L("Manage Sonarr Show"), title2=show['title'],
                                 header=TITLE if message else None, message=message)
        else:
            oc = ObjectContainer(title1=L("Manage Sonarr Show"), title2=show['title'])
        if callback:
            oc.add(DirectoryObject(key=callback, title=L("Return"), thumb=None))
        else:
            oc.add(DirectoryObject(key=Callback(self.ManageSonarr), title="Return to Shows"))
        oc.add(
            DirectoryObject(key=Callback(self.SonarrMonitorShow, series_id=series_id, seasons='all', callback=callback),
                            title=L("Monitor All Seasons"), thumb=None))
        # Log.Debug(show['seasons'])
        for season in show['seasons']:
            season_number = int(season['seasonNumber'])
            mark = "* " if season['monitored'] else ""
            oc.add(DirectoryObject(
                key=Callback(self.ManageSonarrSeason, series_id=series_id, season=season_number, callback=callback),
                title=mark + (L("Season ") + str(season_number) if season_number > 0 else "Specials"),
                thumb=None))
        return oc

    def ManageSonarrSeason(self, series_id, season, message=None, callback=None):
        if not Prefs['sonarr_url'].startswith("http"):
            sonarr_url = "http://" + Prefs['sonarr_url']
        else:
            sonarr_url = Prefs['sonarr_url']
        if sonarr_url.endswith("/"):
            sonarr_url = sonarr_url[:-1]
        api_header = {
            'X-Api-Key': Prefs['sonarr_api']
        }

        episodes = JSON.ObjectFromURL(sonarr_url + "/api/Episode/?seriesId=" + str(series_id), headers=api_header)

        if isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(title1=L("Manage Season"), title2=L("Season ") + str(season),
                                 header=TITLE if message else None, message=message)
        else:
            oc = ObjectContainer(title1=L("Manage Season"), title2=L("Season ") + str(season))
        if callback:
            oc.add(DirectoryObject(key=callback, title=L("Return")))
        oc.add(DirectoryObject(key=Callback(self.ManageSonarrShow, series_id=series_id, callback=callback),
                               title=L("Return to Seasons")))
        oc.add(DirectoryObject(
            key=Callback(self.SonarrMonitorShow, series_id=series_id, seasons=str(season), callback=callback),
            title=L("Monitor Season and Search"), thumb=None))
        # data = JSON.StringFromObject({'seriesId': series_id})

        # Log.Debug(JSON.StringFromObject(episodes))
        for episode in episodes:
            if not episode['seasonNumber'] == int(season):
                continue
            marked = "* " if episode['monitored'] else ""
            oc.add(
                DirectoryObject(
                    key=Callback(self.SonarrMonitorShow, series_id=series_id, seasons=str(season),
                                 episodes=str(episode['id']), callback=callback),
                    title=marked + str(episode.get('episodeNumber', "##")) + ". " + episode.get('title', ""),
                    summary=(episode.get('overview', None)), thumb=None))
        return oc

    def SonarrMonitorShow(self, series_id, seasons, episodes='all', callback=None):
        if not Prefs['sonarr_url'].startswith("http"):
            sonarr_url = "http://" + Prefs['sonarr_url']
        else:
            sonarr_url = Prefs['sonarr_url']
        if sonarr_url.endswith("/"):
            sonarr_url = sonarr_url[:-1]
        api_header = {
            'X-Api-Key': Prefs['sonarr_api']
        }
        try:
            show = JSON.ObjectFromURL(sonarr_url + "/api/series/" + series_id, headers=api_header)
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug(e.message)
            return MessageContainer(header=TITLE, message=F("errorsonarrshow", str(series_id)))
        if seasons == 'all':
            for s in show['seasons']:
                s['monitored'] = True
            data = JSON.StringFromObject(show)
            data2 = JSON.StringFromObject({'name': 'SeriesSearch', 'seriesId': int(series_id)})
            try:
                HTTP.Request(url=sonarr_url + "/api/series/", data=data, headers=api_header,
                             method='PUT')  # Post Series to monitor
                HTTP.Request(url=sonarr_url + "/api/command", data=data2,
                             headers=api_header)  # Search for all episodes in series
                return self.ManageSonarrShow(series_id=series_id, title=show['title'], callback=callback,
                                             message=L("Series sent to Sonarr"))
            except Exception as e:
                if Dict['debug']:
                    Log(str(show))
                Log.Error(str(traceback.format_exc()))  # raise e
                Log.Debug("Sonarr Monitor failed: " + str(Response.Status) + " - " + e.message)
                return MessageContainer(header=Title, message=L("Error sending show to Sonarr"))
        elif episodes == 'all':
            season_list = seasons.split()
            for s in show['seasons']:
                if str(s['seasonNumber']) in season_list:
                    s['monitored'] = True
            data = JSON.StringFromObject(show)
            try:
                HTTP.Request(sonarr_url + "/api/series", data=data, headers=api_header,
                             method='PUT')  # Post seasons to monitor
                for s in season_list:  # Search for each chosen season
                    data2 = JSON.StringFromObject(
                        {'name': 'SeasonSearch', 'seriesId': int(series_id), 'seasonNumber': int(s)})
                    HTTP.Request(sonarr_url + "/api/command", headers=api_header, data=data2)
                return self.ManageSonarrShow(series_id=series_id, callback=callback,
                                             message=L("Season(s) sent sent to Sonarr"))
            except Exception as e:
                if Dict['debug']:
                    Log.Debug(str(data))
                Log.Error(str(traceback.format_exc()))  # raise e
                Log.Debug("Sonarr Monitor failed: " + e.message)
                return MessageContainer(header=Title, message=L("Error sending season to Sonarr"))
        else:
            episode_list = episodes.split()
            try:
                for e in episode_list:
                    episode = JSON.ObjectFromURL(sonarr_url + "/api/Episode/" + str(e), headers=api_header)
                    episode['monitored'] = True
                    data = JSON.StringFromObject(episode)
                    HTTP.Request(sonarr_url + "/api/Episode/" + str(e), data=data, headers=api_header, method='PUT')
                data2 = JSON.StringFromObject({'name': "EpisodeSearch", 'episodeIds': episode_list})
                HTTP.Request(sonarr_url + "/api/command", headers=api_header, data=data2)
                return self.ManageSonarrSeason(series_id=series_id, season=seasons, callback=callback,
                                               message=L("Episode sent to Sonarr"))
            except Exception as e:
                Log.Error(str(traceback.format_exc()))  # raise e
                Log.Debug("Sonarr Monitor failed: " + e.message)
                return MessageContainer(header=Title, message=L("Error sending episode to Sonarr"))
                # return self.MainMenu()

    def SonarrShowExists(self, tvdbid):
        if not Prefs['sonarr_url'].startswith("http"):
            sonarr_url = "http://" + Prefs['sonarr_url']
        else:
            sonarr_url = Prefs['sonarr_url']
        if not sonarr_url.endswith("/"):
            sonarr_url += "/"
        api_header = {
            'X-Api-Key': Prefs['sonarr_api']
        }
        series = JSON.ObjectFromURL(sonarr_url + "api/Series", headers=api_header)
        for show in series:
            if show['tvdbId'] == int(tvdbid) and show['id']:
                return show['id']
        return False

    # Sickbeard Functions
    def SendToSickbeard(self, tvdbid, callback=None):
        if not Prefs['sickbeard_url'].startswith("http"):
            sickbeard_url = "http://" + Prefs['sickbeard_url']
        else:
            sickbeard_url = Prefs['sickbeard_url']
        if not sickbeard_url.endswith("/"):
            sickbeard_url += "/"
        title = Dict['tv'][tvdbid]['title']

        if self.SickbeardShowExists(tvdbid):
            Dict['tv'][tvdbid]['automated'] = True
            Dict.Save()
            return self.ManageSickbeardShow(series_id=tvdbid, callback=callback)

        data = dict(cmd='show.addnew', tvdbid=tvdbid)
        use_sickrage = (Prefs['sickbeard_fork'] == 'SickRage')

        if Prefs['sickbeard_location']:
            data['location'] = Prefs['sickbeard_location']
        if Prefs['sickbeard_status']:
            data['status'] = "ignored" if Prefs['sickbeard_status'] == "manual" else Prefs['sickbeard_status']
        if Prefs['sickbeard_initial']:
            data['initial'] = Prefs['sickbeard_initial']
        if Prefs['sickbeard_archive']:
            data['archive'] = Prefs['sickbeard_archive']
        if Prefs['sickbeard_language'] or use_sickrage:
            data['lang'] = Prefs['sickbeard_language'] if Prefs[
                'sickbeard_language'] else "en"  # SickRage requires lang set

        if use_sickrage:
            data['anime'] = False  # SickRage requires anime set

        # Log.Debug(str(data))

        try:
            resp = JSON.ObjectFromURL(sickbeard_url + "api/" + Prefs['sickbeard_api'], values=data,
                                      method='GET' if use_sickrage else 'POST')
            if 'result' in resp and resp['result'] == "success":
                if isClient(MESSAGE_OVERLAY_CLIENTS):
                    oc = ObjectContainer(header=TITLE, message=F("sickbeardshowadded", Prefs['sickbeard_fork']))
                else:
                    oc = ObjectContainer(title1=Prefs['sickbeard_fork'], title2=L("Success"))
                Dict['tv'][tvdbid]['automated'] = True
                Dict.Save()
            else:
                if isClient(MESSAGE_OVERLAY_CLIENTS):
                    oc = ObjectContainer(header=TITLE, message=resp['message'])
                else:
                    oc = ObjectContainer(title1=Prefs['sickbeard_fork'], title2=L("Error"))
        except Exception as e:
            if Dict['debug']:
                Log.Debug(str(data))
            Log.Error(str(traceback.format_exc()))  # raise e
            oc = ObjectContainer(header=TITLE, message=F("sickbeardfail", Prefs['sickbeard_fork']))
            Log.Debug(e.message)
        # Thread.Sleep(2)
        if Prefs['sickbeard_status'] == "manual":  # and SickbeardShowExists(tvdbid):
            count = 0
            while count < 5:
                if self.SickbeardShowExists(tvdbid):
                    return self.ManageSickbeardShow(tvdbid, title=title, callback=callback)
                Thread.Sleep(1)
                Log.Debug("Slept for " + str(count) + " seconds")
                count += 1
        if self.is_admin:
            oc.add(
                DirectoryObject(key=Callback(self.ConfirmDeleteRequest, series_id=tvdbid, type='tv', title_year=title),
                                title=L("Delete Request")))
        oc.add(DirectoryObject(key=Callback(self.ViewTVRequests), title=L("Return to TV Requests")))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu")))
        return oc

    def ManageSickbeard(self):
        oc = ObjectContainer(title1=TITLE, title2="Manage " + Prefs['sickbeard_fork'])
        if not Prefs['sickbeard_url'].startswith("http"):
            sickbeard_url = "http://" + Prefs['sickbeard_url']
        else:
            sickbeard_url = Prefs['sickbeard_url']
        if not sickbeard_url.endswith("/"):
            sickbeard_url += "/"
        data = dict(cmd='shows')
        use_sickrage = (Prefs['sickbeard_fork'] == "SickRage")
        try:
            resp = JSON.ObjectFromURL(sickbeard_url + "api/" + Prefs['sickbeard_api'], values=data,
                                      method='GET' if use_sickrage else 'POST')
            Log.Debug(str(JSON.StringFromObject(resp)))
            if 'result' in resp and resp['result'] == "success":
                for show_id in resp['data']:
                    poster = sickbeard_url + "api/" + Prefs['sickbeard_api'] + "/?cmd=show.getposter&tvdbid=" + show_id
                    oc.add(TVShowObject(
                        key=Callback(self.ManageSickbeardShow, series_id=show_id,
                                     title=resp['data'][show_id].get('show_name', ""),
                                     callback=Callback(self.ManageSickbeard)),
                        rating_key=show_id, title=resp['data'][show_id].get('show_name', ""), thumb=poster))
        except Exception as e:
            if Dict['debug']:
                Log.Debug(str(data))
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug(e.message)
            return MessageContainer(header=TITLE, message=F("sickbeardshowserror", Prefs['sickbeard_fork']))
        oc.objects.sort(key=lambda obj: obj.title.lower())
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu")))
        return oc

    def ManageSickbeardShow(self, series_id, title="", callback=None, message=None):
        if not Prefs['sickbeard_url'].startswith("http"):
            sickbeard_url = "http://" + Prefs['sickbeard_url']
        else:
            sickbeard_url = Prefs['sickbeard_url']
        if not sickbeard_url.endswith("/"):
            sickbeard_url += "/"
        data = dict(cmd='show.seasonlist', tvdbid=series_id)
        use_sickrage = (Prefs['sickbeard_fork'] == "SickRage")
        try:
            resp = JSON.ObjectFromURL(sickbeard_url + "api/" + Prefs['sickbeard_api'], values=data,
                                      method='GET' if use_sickrage else 'POST')
            if 'result' in resp and resp['result'] == "success":
                pass
            else:
                Log.Debug(JSON.StringFromObject(resp))
                return MessageContainer(header=TITLE,
                                        message="Error retrieving " + Prefs['sickbeard_fork'] + " Show: " + (
                                            title if title else str(series_id)))
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug(e.message)
            return MessageContainer(header=TITLE,
                                    message="Error retrieving " + Prefs['sickbeard_fork'] + " Show: " + (
                                        title if title else str(series_id)))
        if isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(title1="Manage " + Prefs['sickbeard_fork'] + " Show", title2=title,
                                 header=TITLE if message else None,
                                 message=message)
        else:
            oc = ObjectContainer(title1="Manage " + Prefs['sickbeard_fork'] + " Show", title2=title)
        if callback:
            oc.add(DirectoryObject(key=callback, title="Go Back", thumb=None))
        else:
            oc.add(DirectoryObject(key=Callback(self.ManageSickbeard), title="Return to Shows"))
        oc.add(DirectoryObject(
            key=Callback(self.SickbeardMonitorShow, series_id=series_id, seasons='all', callback=callback),
            title=L("Monitor All Seasons"), thumb=None))
        # Log.Debug(show['seasons'])
        for season in resp['data']:
            oc.add(DirectoryObject(
                key=Callback(self.ManageSickbeardSeason, series_id=series_id, season=season, callback=callback),
                title=L("Season ") + str(season) if season > 0 else "Specials", thumb=None))
        oc.add(
            DirectoryObject(key=Callback(self.ManageSickbeardShow, series_id=series_id, title=title, callback=callback),
                            title="Refresh"))
        return oc

    def ManageSickbeardSeason(self, series_id, season, message=None, callback=None):
        if not Prefs['sickbeard_url'].startswith("http"):
            sickbeard_url = "http://" + Prefs['sickbeard_url']
        else:
            sickbeard_url = Prefs['sickbeard_url']
        if not sickbeard_url.endswith("/"):
            sickbeard_url += "/"
        data = dict(cmd='show.seasons', tvdbid=series_id, season=season)
        use_sickrage = (Prefs['sickbeard_fork'] == "SickRage")
        try:
            resp = JSON.ObjectFromURL(sickbeard_url + "api/" + Prefs['sickbeard_api'], values=data,
                                      method='GET' if use_sickrage else 'POST')
            if 'result' in resp and resp['result'] == "success":
                pass
            else:
                Log.Debug(JSON.StringFromObject(resp))
                return MessageContainer(header=TITLE,
                                        message="Error retrieving " + Prefs['sickbeard_fork'] + " Show ID: " + str(
                                            series_id) + " Season " + str(
                                            season))
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug(e.message)
            return MessageContainer(header=TITLE,
                                    message="Error retrieving " + Prefs['sickbeard_fork'] + " Show ID: " + str(
                                        series_id) + " Season " + str(season))
        if isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(title1=L("Manage Season"), title2=L("Season ") + str(season),
                                 header=TITLE if message else None, message=message)
        else:
            oc = ObjectContainer(title1=L("Manage Season"), title2=L("Season ") + str(season))
        if callback:
            oc.add(DirectoryObject(key=callback, title=L("Return")))
        oc.add(DirectoryObject(key=Callback(self.ManageSickbeardShow, series_id=series_id, callback=callback),
                               title=L("Return to Seasons")))
        oc.add(DirectoryObject(
            key=Callback(self.SickbeardMonitorShow, series_id=series_id, seasons=str(season), callback=callback),
            title=L("Get All Episodes"), thumb=None))
        for e in sorted(resp['data'], key=lambda s: int(s)):
            episode = resp['data'][e]
            marked = "* " if episode.get('status') == "Wanted" or episode.get('status') == "Downloaded" else ""
            oc.add(
                DirectoryObject(key=Callback(self.SickbeardMonitorShow, series_id=series_id, seasons=season, episodes=e,
                                             callback=callback),
                                title=marked + e + ". " + episode.get('name', ""),
                                summary=(episode.get('status', None)), thumb=None))
        return oc

    def SickbeardMonitorShow(self, series_id, seasons, episodes='all', callback=None):
        if not Prefs['sickbeard_url'].startswith("http"):
            sickbeard_url = "http://" + Prefs['sickbeard_url']
        else:
            sickbeard_url = Prefs['sickbeard_url']
        if not sickbeard_url.endswith("/"):
            sickbeard_url += "/"
        use_sickrage = (Prefs['sickbeard_fork'] == "SickRage")
        if seasons == 'all':
            data = dict(cmd='show.seasons', tvdbid=series_id)
            try:
                resp = JSON.ObjectFromURL(sickbeard_url + "api/" + Prefs['sickbeard_api'], values=data,
                                          method='GET' if use_sickrage else 'POST')  # Search for all episodes in series
                if 'result' in resp and resp['result'] == "success":
                    for s in resp['data']:
                        try:
                            data2 = dict(cmd='episode.setstatus', tvdbid=series_id, season=s, status="wanted")
                            JSON.ObjectFromURL(sickbeard_url + "api/" + Prefs['sickbeard_api'], values=data2,
                                               method='GET' if use_sickrage else 'POST')
                        except:
                            if Dict['debug']:
                                Log.Debug(str(resp))
                            Log.Error(str(traceback.format_exc()))  # raise e
                            Log.Debug("Error changing season status for (%s - S%s" % (series_id, s))
                else:
                    Log.Debug(JSON.StringFromObject(resp))
                    return MessageContainer(header=TITLE, message="Error retrieving from " + Prefs[
                        'sickbeard_fork'] + " TVDB id: " + series_id)
                return self.ManageSickbeardShow(series_id=series_id, title="", callback=callback,
                                                message="Series sent to " + Prefs['sickbeard_fork'])
            except Exception as e:
                Log.Error(str(traceback.format_exc()))  # raise e
                Log.Debug(
                    Prefs['sickbeard_fork'] + " Status change failed: " + str(Response.Status) + " - " + e.message)
                return MessageContainer(header=Title, message="Error sending series to " + Prefs['sickbeard_fork'])
        elif episodes == 'all':
            season_list = seasons.split()
            try:
                for s in season_list:
                    data = dict(cmd='episode.setstatus', tvdbid=series_id, season=s, status="wanted")
                    JSON.ObjectFromURL(sickbeard_url + "api/" + Prefs['sickbeard_api'], values=data,
                                       method='GET' if use_sickrage else 'POST')
                return self.ManageSickbeardShow(series_id=series_id, callback=callback,
                                                message="Season(s) sent sent to " + Prefs['sickbeard_fork'])
            except Exception as e:
                Log.Error(str(traceback.format_exc()))  # raise e
                Log.Debug(Prefs['sickbeard_fork'] + " Status Change failed: " + e.message)
                return MessageContainer(header=TITLE, message="Error sending season to " + Prefs['sickbeard_fork'])
        else:
            episode_list = episodes.split()
            try:
                for e in episode_list:
                    data = dict(cmd='episode.setstatus', tvdbid=series_id, season=seasons, episode=e, status="wanted")
                    JSON.ObjectFromURL(sickbeard_url + "api/" + Prefs['sickbeard_api'], values=data,
                                       method='GET' if use_sickrage else 'POST')
                return self.ManageSickbeardSeason(series_id=series_id, season=seasons, callback=callback,
                                                  message="Episode(s) sent to " + Prefs['sickbeard_fork'])
            except Exception as e:
                Log.Error(str(traceback.format_exc()))  # raise e
                Log.Debug(Prefs['sickbeard_fork'] + " Status Change failed: " + e.message)
                return MessageContainer(header=TITLE, message="Error sending episode to " + Prefs['sickbeard_fork'])
                # return self.MainMenu()

    def SickbeardShowExists(self, tvdbid):
        if not Prefs['sickbeard_url'].startswith("http"):
            sickbeard_url = "http://" + Prefs['sickbeard_url']
        else:
            sickbeard_url = Prefs['sickbeard_url']
        if not sickbeard_url.endswith("/"):
            sickbeard_url += "/"
        data = dict(cmd='shows')
        use_sickrage = (Prefs['sickbeard_fork'] == "SickRage")
        try:
            resp = JSON.ObjectFromURL(sickbeard_url + "api/" + Prefs['sickbeard_api'], values=data,
                                      method='GET' if use_sickrage else 'POST')
            # Log.Debug(JSON.StringFromObject(resp))
            if 'result' in resp and resp['result'] == "success":
                if str(tvdbid) in resp['data']:
                    Log.Debug("TVDB id " + str(tvdbid) + " exists")
                    return True
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug(e.message)
        Log.Debug("TVDB id " + str(tvdbid) + " does not exist")
        return False

    def SendToHeadphones(self, music_id):
        if not Prefs['headphones_url'].startswith("http"):
            headphones_url = "http://" + Prefs['headphones_url']
        else:
            headphones_url = Prefs['headphones_url']
        if not headphones_url.endswith("/"):
            headphones_url += "/"
        try:
            data = {'apikey': Prefs['headphones_api'],
                    'cmd': 'addAlbum',
                    'id': str(music_id)
                    }
            resp = HTTP.Request(
                headphones_url + "api/?apikey=" + Prefs['headphones_api'] + "&cmd=addAlbum&id=" + str(music_id))
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc = ObjectContainer(header=TITLE, message=L("Album was added to Headphones"))
            else:
                oc = ObjectContainer(title1=Headphones, title2=L("Success"))
            Log.Debug(str(resp))
            Dict['music'][music_id]['automated'] = True
            Dict.Save()
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug(e.message)
            Log.Debug("Could not add " + str(music_id) + " to Headphones")
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc = ObjectContainer(header=TITLE, message=L("Album was not added to Headphones"))
            else:
                oc = ObjectContainer(title1=Headphones, title2=L("Failure"))
        title = Dict['music'][music_id].get('title')
        if self.is_admin:
            oc.add(DirectoryObject(key=Callback(self.ConfirmDeleteRequest, req_id=music_id, type='music',
                                                title_year=title), title=L("Delete Request"), ))
        oc.add(DirectoryObject(key=Callback(self.ViewMusicRequests), title=L("Return to Music Requests")))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu")))
        return oc

    # ManageChannel Functions
    def ManageChannel(self, message=None, title1=TITLE, title2="Manage Channel"):
        if not self.is_admin:
            return self.SMainMenu(L("Only an admin can manage the channel!"), title1=L("Main Menu"),
                                  title2=L("Admin only"))
        if message and isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(header=TITLE, message=message)
        else:
            oc = ObjectContainer(title1=L("Manage"), title2=message)
        oc.add(DirectoryObject(key=Callback(self.ManageUsers), title=L("Manage Users")))
        oc.add(
            DirectoryObject(key=Callback(self.ToggleDebug), title=F("toggledebug", "Off" if Dict['debug'] else "On")))
        oc.add(PopupDirectoryObject(key=Callback(self.ResetDict), title=L("Reset Dictionary Settings")))
        oc.add(DirectoryObject(key=Callback(self.Changelog), title=L("Changelog")))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu")))
        return oc

    def ManageUsers(self, message=None):
        if not self.is_admin:
            return self.SMainMenu(L("Only an admin can manage the channel!"), title1=L("Main Menu"),
                                  title2=L("Admin only"))
        if not message or isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(header=TITLE, message=message)
        else:
            oc = ObjectContainer(title1=L("Manage Users"), title2=message)
        if len(Dict['register']) > 0:
            for toke in Dict['register']:
                user = userFromToken(toke)
                oc.add(
                    DirectoryObject(key=Callback(self.ManageUser, toke=toke),
                                    title=user + ": " + str(Dict['register'][toke]['requests'])))
        oc.add(DirectoryObject(key=Callback(self.ManageChannel), title=L("Return to Manage Channel")))
        return oc

    def ManageUser(self, toke, message=None):
        if not self.is_admin:
            return self.SMainMenu(L("Only an admin can manage the channel!"), title1=L("Main Menu"),
                                  title2=L("Admin only"))
        user = userFromToken(toke)
        if isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(title1=L("Manage User"), title2=user, message=message)
        else:
            oc = ObjectContainer(title1=L("Manage User"), title2=message)
        oc.add(DirectoryObject(key=Callback(self.ManageUser, toke=toke),
                               title=user + " has made " + str(Dict['register'][toke]['requests']) + " requests."))
        oc.add(DirectoryObject(key=Callback(self.RenameUser, toke=toke), title="Rename User"))
        tv_auto = ""
        # if Prefs['sonarr_api']:
        #     tv_auto = "Sonarr"
        # elif Prefs['sickbeard_api']:
        #     tv_auto = Prefs['sickbeard_fork']
        if toke in Dict['sonarr_users']:
            oc.add(DirectoryObject(key=Callback(self.SonarrUser, toke=toke, setter='False'),
                                   title=F("removetvmanage", tv_auto)))
        elif Prefs['sonarr_api'] or Prefs['sickbeard_api'] or Prefs['couchpotato_api']:
            oc.add(DirectoryObject(key=Callback(self.SonarrUser, toke=toke, setter='True'),
                                   title=F("allowtvmanage", tv_auto)))
        if toke in Dict['blocked']:
            oc.add(DirectoryObject(key=Callback(self.BlockUser, toke=toke, setter='False'), title=L("Unblock User")))
        else:
            oc.add(DirectoryObject(key=Callback(self.BlockUser, toke=toke, setter='True'), title=L("Block User")))
        oc.add(
            PopupDirectoryObject(key=Callback(self.DeleteUser, toke=toke, confirmed='False'), title=L("Delete User")))
        oc.add(DirectoryObject(key=Callback(self.ManageChannel), title=L("Return to Manage Channel")))

        return oc

    def RenameUser(self, toke, message=""):
        if not self.is_admin:
            return self.SMainMenu(L("Only an admin can manage the channel!"), title1=L("Main Menu"),
                                  title2=L("Admin only"))
        if Client.Product == "Plex Web":
            message += (" " if message else "") + L("Enter the user name in the searchbox and press enter")
        if isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(header=TITLE, message=message)
        else:
            oc = ObjectContainer(title1=TITLE, title2=L("Register User Name"))
        if self.use_dumb_keyboard:
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=RegisterUserName,
                         parent_call=Callback(self.ManageUser, toke=toke),
                         dktitle=L(L("Enter the user's name")),
                         message=L("Enter the user's name"), toke=toke)
            # return MessageContainer(header=TITLE, message="You must use a keyboard enabled client (Plex Web) to use this feature")
        else:
            oc.add(
                InputDirectoryObject(key=Callback(self.RegisterUserName, toke=toke), title=L("Enter the user's name"),
                                     prompt=L("Enter the user's name")))
        return oc

    def RegisterUserName(self, query="", toke=""):
        if not self.is_admin:
            return self.SMainMenu(L("Only an admin can manage the channel!"), title1=L("Main Menu"),
                                  title2=L("Admin only"))
        if not query:
            return self.RegisterUser(toke, message=L("You must enter a name. Try again."))
        Dict['register'][toke]['nickname'] = query
        Dict.Save()
        return self.ManageUser(toke=toke, message=L("Username has been set"))

    def BlockUser(self, toke, setter):
        if setter == 'True':
            if toke in Dict['blocked']:
                return self.ManageUser(toke=toke, message=L("User is already blocked."))
            else:
                Dict['blocked'].append(toke)
                Dict.Save()
                return self.ManageUser(toke == toke, message="User has been blocked.")
        elif setter == 'False':
            if toke in Dict['blocked']:
                Dict['blocked'].remove(toke)
                Dict.Save()
                return self.ManageUser(toke=toke, message="User has been unblocked.")
        return self.ManageUser(toke=toke)

    def SonarrUser(self, toke, setter):
        tv_auto = ""
        if Prefs['sonarr_api']:
            tv_auto = "Sonarr"
        elif Prefs['sickbeard_api']:
            tv_auto = "Sickbeard"
        if setter == 'True':
            if toke in Dict['sonarr_users']:
                return self.ManageUser(toke=toke, message="User already in " + tv_auto + " list")
            else:
                Dict['sonarr_users'].append(toke)
                Dict.Save()
                return self.ManageUser(toke=toke, message="User is now allowed to manage " + tv_auto)
        else:
            if toke in Dict['sonarr_users']:
                Dict['sonarr_users'].remove(toke)
                Dict.Save()
                return self.ManageUser(toke=toke, message="User can no longer manage " + tv_auto)
        return self.ManageUser(toke=toke)

    def DeleteUser(self, toke, confirmed='False'):
        if not self.is_admin:
            return self.SMainMenu("Only an admin can manage the channel!", title1="Main Menu", title2="Admin only")
        oc = ObjectContainer(title1=L("Confirm Delete User?"), title2=Dict['register'][toke]['nickname'])
        if confirmed == 'False':
            oc.add(DirectoryObject(key=Callback(self.DeleteUser, toke=toke, confirmed='True'), title=L("Yes")))
            oc.add(DirectoryObject(key=Callback(self.ManageUser, toke=toke), title=L("No")))
        elif confirmed == 'True':
            Dict['register'].pop(toke, None)
            Dict.Save()
            return self.ManageUsers(message=L("User registration has been deleted."))
        return oc

    def ResetDict(self, confirm='False'):
        if not self.is_admin:
            return self.SMainMenu("Only an admin can manage the channel!", title1="Main Menu", title2="Admin only")
        if confirm == 'False':
            if isClient(MESSAGE_OVERLAY_CLIENTS):
                oc = ObjectContainer(header=TITLE,
                                     message=L(
                                         "Are you sure you would like to clear all saved info? This will clear all requests and user information."))
            else:
                oc = ObjectContainer(title1=L("Reset Info"), title2=L("Confirm"))
            oc.add(DirectoryObject(key=Callback(self.ResetDict, confirm='True'), title=L("Yes")))
            oc.add(DirectoryObject(key=Callback(self.ManageChannel), title=L("No")))
            return oc
        elif confirm == 'True':
            Dict.Reset()
            Dict['tv'] = {}
            Dict['movie'] = {}
            Dict['register'] = {}
            Dict['register_reset'] = Datetime.TimestampFromDatetime(Datetime.Now())
            Dict['blocked'] = []
            Dict['sonarr_users'] = []
            Dict['debug'] = False
            Dict.Save()
            return self.ManageChannel(message=L("Dictionary has been reset!"))

        return MessageContainer(header=TITLE, message="Unknown response")

    def Changelog(self):
        oc = ObjectContainer(title1=TITLE, title2=L("Changelog"))
        clog = HTTP.Request(CHANGELOG_URL)
        changes = clog.content
        changes = changes.splitlines()
        oc.add(DirectoryObject(key=Callback(self.Changelog), title="Current Version: " + str(VERSION),
                               thumb=R('plexrequestchannel.png')))
        for change in changes[:10]:
            csplit = change.split("-")
            title = csplit[0].strip() + " - v" + csplit[1].strip()
            oc.add(DirectoryObject(key=Callback(self.ShowMessage, header=title, message=change), title=title,
                                   summary=csplit[2].strip(),
                                   thumb=R('plexrequestchannel.png')))
        oc.add(DirectoryObject(key=Callback(self.ManageChannel), title=L("Return to Manage Channel"),
                               thumb=R('return.png')))
        return oc

    def ToggleDebug(self):
        if Dict['debug']:
            Dict['debug'] = False
        else:
            Dict['debug'] = True
        Dict.Save()
        return self.ManageChannel(message="Debug is " + ("on" if Dict['debug'] else "off"))

    def ShowMessage(self, header, message):
        return MessageContainer(header=header, message=message)

    def ReportProblem(self):
        oc = ObjectContainer(title1=TITLE, title2=L("Report a Problem"))
        oc.add(DirectoryObject(key=Callback(self.NavigateMedia), title=L("Report Problem with Media")))
        if self.use_dumb_keyboard:  # Clients in this list do not support InputDirectoryObjects
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            # oc.add(
            #     DirectoryObject(key=Callback(Keyboard, callback=self.ConfirmReportProblem, parent=ReportProblem, title="Report General Problem",
            #                                  message="What is the problem?"), title="Report General Problem"))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.ConfirmReportProblem,
                         parent_call=Callback(self.ReportProblem),
                         dktitle=L("Report General Problem"),
                         message=L("What is the problem?"))
        elif Client.Product == "Plex Web":  # Plex Web does not create a popup input directory object, so use an intermediate menu
            oc.add(DirectoryObject(key=Callback(self.ReportGeneralProblem), title=L("Report General Problem")))
        else:  # All other clients
            oc.add(
                InputDirectoryObject(key=Callback(self.ConfirmReportProblem), title=L("Report General Problem"),
                                     prompt=L("What is the problem?")))
        return oc

    def NavigateMedia(self, path=None):
        if not path:
            path = "/library/sections"
            parent = None
        else:
            parent = path[:path.rfind("/") - 1]
        # headers = {'X-Plex-Token': self.token}
        try:
            page = XML.ElementFromURL("http://127.0.0.1:32400" + path, headers=Request.Headers)
        except:
            Log.Error(str(traceback.format_exc()))  # raise e
            return MessageContainer(header=TITLE, message="Unable to navigate path!")
        container = page.xpath("/MediaContainer")[0]
        view_group = container.get('viewGroup', 'secondary')
        if 'parentKey' in container.attrib:
            parent = container.attrib.get("parentKey", None)
        elif 'librarySectionID' in container.attrib:
            parent = "/library/sections/" + container.attrib['librarySectionID']
        title = container.attrib.get('title1', "")
        oc = ObjectContainer(title1="Report Problem", title2=title)
        if parent:
            oc.add(DirectoryObject(key=Callback(self.NavigateMedia, path=parent), title=L("Go Up One"),
                                   thumb=R('return.png')))
        else:
            oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("Return to Main Menu"), thumb=R('return.png')))
        dirs = page.xpath("//Directory")
        if len(dirs) > 0:
            for d in dirs:
                type = d.attrib.get('type', None)
                if type == 'show' and 'filters' not in d.attrib:
                    oc.add(
                        TVShowObject(key=Callback(self.NavigateMedia, path=d.attrib['key']),
                                     title=d.attrib.get('title'),
                                     rating_key=d.attrib.get('ratingKey', "0"),
                                     summary=d.attrib.get('summary'), thumb=d.attrib.get('thumb')))
                elif type == 'season':
                    oc.add(
                        TVShowObject(key=Callback(self.NavigateMedia, path=d.attrib['key']),
                                     title=d.attrib.get('title'),
                                     rating_key=d.attrib.get('ratingKey', "0"),
                                     summary=d.attrib.get('summary'), thumb=d.attrib.get('thumb')))
                else:
                    oc.add(DirectoryObject(key=Callback(self.NavigateMedia, path=path + "/" + d.attrib['key']),
                                           title=d.attrib.get('title', ""),
                                           thumb=d.attrib.get('thumb', None)))
        vids = page.xpath("//Video")
        if len(vids) > 0:
            for v in vids:
                type = v.attrib.get('type', None)
                if type == 'movie':
                    oc.add(TVShowObject(key=Callback(self.ReportProblemMedia, rating_key=v.attrib['ratingKey'],
                                                     title=v.attrib.get('title')),
                                        rating_key=v.attrib.get('ratingKey', "0"), title=v.attrib.get('title'),
                                        summary=v.attrib.get('summary'), thumb=v.attrib.get('thumb')))
                elif type == 'episode':
                    # oc.add(EpisodeObject(key=Callback(self.ReportProblemMedia, rating_key=v.attrib['ratingKey'], title=v.attrib.get('title')),
                    #                      rating_key=v.attrib.get('ratingKey', "0"), title=v.attrib.get('title'),
                    #                      summary=v.attrib.get('summary'), thumb=v.attrib.get('thumb')))
                    oc.add(DirectoryObject(key=Callback(self.ReportProblemMedia, rating_key=v.attrib['ratingKey'],
                                                        title=v.attrib.get('title')),
                                           title=v.attrib.get('title'), summary=v.attrib.get('summary'),
                                           thumb=v.attrib.get('thumb')))
        return oc

    def ReportProblemMedia(self, rating_key, title):
        oc = ObjectContainer(title1="What is the problem?", title2=title)
        page = XML.ElementFromURL("http://127.0.0.1:32400/library/metadata/" + rating_key)
        container = page.xpath("/MediaContainer")[0]
        libraryTitle = container.attrib.get("librarySectionTitle", "Unknown")
        vid = page.xpath("//Video")[0]
        type = vid.attrib.get('type', 'unknown')
        thumb = vid.attrib.get('thumb', None)
        name = ""
        if type == 'movie':
            if 'year' in vid.attrib:
                title += " (" + vid.attrib['year'] + ")"
            name = title
        elif type == 'episode':
            ep_num = int(vid.attrib.get('index', "1"))
            sea_num = int(vid.attrib.get('parentIndex', "1"))
            show_title = vid.attrib.get('grandparentTitle', "")
            title = vid.attrib.get('title', "")
            name = "%s - S%sxE%0d - %s" % (show_title, sea_num, ep_num, title)
        if Client.Product == 'Plex Web':
            oc.add(TVShowObject(key=Callback(self.ReportProblemMedia, rating_key=rating_key, title=title),
                                rating_key=rating_key, title=title,
                                thumb=thumb))
        report = name + " in Library: '" + libraryTitle + "'"
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title="Cancel"))
        for problem in COMMON_MEDIA_PROBLEMS:
            oc.add(
                DirectoryObject(key=Callback(self.ConfirmReportProblem, query=report + " - " + problem, type='media'),
                                title=problem))
        if self.use_dumb_keyboard:
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            # oc.add(DirectoryObject(key=Callback(Keyboard, callback=self.ConfirmReportProblem, parent=ReportProblem),
            #                        title="Report a General Problem"))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.ReportProblemMediaOther,
                         parent_call=Callback(self.ReportProblem),
                         dktitle=L("Other Problem"),
                         message=L("What is the problem?"), report=report)
        elif Client.Product == "Plex Web":  # Plex Web does not create a popup input directory object, so use an intermediate menu
            oc.add(DirectoryObject(key=Callback(self.ReportProblemMediaOther, report=report), title=L("Other Problem")))
        else:
            oc.add(
                InputDirectoryObject(key=Callback(self.ReportProblemMediaOther, report=report),
                                     title=L("Other Problem"),
                                     prompt=L("What is the problem?")))

        return oc

    def ReportProblemMediaOther(self, query="", report=""):
        if not query:
            oc = ObjectContainer(title2=L("Report Problem with Media"))
            if Client.Product == "Plex Web":
                oc.message = L("Enter your problem in the search box.")
            oc.add(
                InputDirectoryObject(key=Callback(self.ReportProblemMediaOther, report=report),
                                     title=L("Other Problem"),
                                     prompt=L("What is the problem?")))
            return oc
        return self.ConfirmReportProblem(query=report + " - " + query, type='media')

    def ReportGeneralProblem(self):
        if isClient(MESSAGE_OVERLAY_CLIENTS):
            oc = ObjectContainer(header=TITLE, message=L("Enter your problem in the search box."))
        else:
            oc = ObjectContainer(title2=title)
        if self.use_dumb_keyboard:
            Log.Debug("Client does not support Input. Using DumbKeyboard")
            # oc.add(DirectoryObject(key=Callback(Keyboard, callback=self.ConfirmReportProblem, parent=ReportProblem),
            #                        title="Report a General Problem"))
            DumbKeyboard(prefix=PREFIX, oc=oc, callback=self.ConfirmReportProblem,
                         parent_call=Callback(self.ReportProblem),
                         dktitle=L("Report General Problem"),
                         message=L("What is the problem?"))
        else:
            oc.add(
                InputDirectoryObject(key=Callback(self.ConfirmReportProblem, type='general'),
                                     title=L("Report a General Problem"),
                                     prompt=L("What is the problem?")))
        return oc

    def ConfirmReportProblem(self, query="", type='general'):
        if type == 'general':
            query = "Issue: " + query
        oc = ObjectContainer(title1=L("Confirm"), title2=query)
        oc.add(DirectoryObject(key=Callback(self.NotifyProblem, problem=query), title=L("Yes"), thumb=R('check.png')))
        oc.add(DirectoryObject(key=Callback(self.SMainMenu), title=L("No"), thumb=R('x-mark.png')))
        return oc

    def NotifyProblem(self, problem):
        title = "Plex Request Channel - Problem Reported"
        user = "A user"
        if self.token in Dict['register'] and Dict['register'][self.token]['nickname']:
            user = Dict['register'][self.token]['nickname']
        body = user + " has reported a problem with the Plex Server. \n" + problem
        Notify(title=title, body=body, devices=Prefs['pushbullet_devices'])
        return self.SMainMenu(message="The admin has been notified", title1="Main Menu",
                              title2="Admin notified of problem")


def checkAdmin(toke):
    # import urllib2
    try:
        url = "https://plex.tv/users/account" if Prefs['plextv'] else "http://127.0.0.1:32400/myplex/account"
        # req = urllib2.Request(url, headers={'X-Plex-Token': toke})
        # resp = urllib2.urlopen(req)
        html = HTTP.Request(url, headers={'X-Plex-Token': toke})
        if html.content:
            return True
    except:
        if Dict['debug']:
            Log.Error(str(traceback.format_exc()))  # raise e
    return False


def resetRegister():
    for key in Dict['register']:
        Dict['register'][key]['requests'] = 0
    Dict['register_reset'] = Datetime.TimestampFromDatetime(Datetime.Now())
    Dict.Save()


# Notifications Functions

# Notify user of requests
def notifyRequest(req_id, req_type, title="", message=""):
    if Prefs['pushbullet_api']:
        try:
            if req_type == 'movie':
                movie = Dict['movie'][req_id]
                title_year = movie['title']
                title_year += (" (" + movie['year'] + ")" if movie.get('year', None) else "")
                user = movie['user'] if movie['user'] else "A user"
                title = "Plex Request Channel - New Movie Request"
                message = user + " has requested a new movie.\n" + title_year + "\n" + \
                          movie.get('source', "IMDB") + " id: " + req_id + "\nPoster: " + \
                          movie['poster']
            elif req_type == 'tv':
                tv = Dict['tv'][req_id]
                user = tv['user'] if tv['user'] else "A user"
                title = "Plex Request Channel - New TV Show Request"
                message = user + " has requested a new tv show.\n" + tv['title'] + "\n" + \
                          tv.get('source', "TVDB") + " id: " + req_id + "\nPoster: " + \
                          tv['poster']
            elif req_type == 'music':
                music = Dict['music'][req_id]
                user = music['user'] if music['user'] else "A user"
                title = "Plex Request Channel - New Album Request"
                message = user + " has requested a new album.\n" + music['title'] + "\n" + \
                          music.get('source', "MusicBrainz") + " id: " + req_id + "\nPoster: " + \
                          music['poster']
            else:
                return
            if Prefs['pushbullet_devices']:
                devices = Prefs['pushbullet_devices'].split(",")
                for d in devices:
                    response = sendPushBullet(title, message, d)
                    if response:
                        Log.Debug("Pushbullet notification sent to device: " + d + " for: " + req_id)
            else:
                response = sendPushBullet(title, message)
                if response:
                    Log.Debug("Pushbullet notification sent for: " + req_id)
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug("Pushbullet failed: " + e.message)
    if Prefs['pushover_user']:
        try:
            if req_type == 'movie':
                movie = Dict['movie'][req_id]
                title_year = movie['title']
                title_year += (" (" + movie['year'] + ")" if movie.get('year', None) else "")
                user = movie['user'] if movie['user'] else "A user"
                title = "Plex Request Channel - New Movie Request"
                message = user + " has requested a new movie.\n" + title_year + "\n" + \
                          movie.get('source', "IMDB") + " id: " + req_id + "\nPoster: " + \
                          movie['poster']
            elif req_type == 'tv':
                tv = Dict['tv'][req_id]
                user = tv['user'] if tv['user'] else "A user"
                title = "Plex Request Channel - New TV Show Request"
                message = user + " has requested a new tv show.\n" + tv['title'] + "\n" + \
                          tv.get('source', "TVDB") + " id: " + req_id + "\nPoster: " + \
                          tv['poster']
            elif req_type == 'music':
                music = Dict['music'][req_id]
                user = music['user'] if music['user'] else "A user"
                title = "Plex Request Channel - New Album Request"
                message = user + " has requested a new album.\n" + music['title'] + "\n" + \
                          music.get('source', "MusicBrainz") + " id: " + req_id + "\nPoster: " + \
                          music['poster']
            else:
                return
            response = sendPushover(title, message)
            if response:
                Log.Debug("Pushover notification sent for :" + req_id)
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug("Pushover failed: " + e.message)
    if Prefs['pushalot_api']:
        try:
            if req_type == 'movie':
                movie = Dict['movie'][req_id]
                title_year = movie['title']
                title_year += (" (" + movie['year'] + ")" if movie.get('year', None) else "")
                user = movie['user'] if movie['user'] else "A user"
                title = "Plex Request Channel - New Movie Request"
                message = user + " has requested a new movie.\n" + title_year + "\n" + \
                          movie.get('source', "IMDB") + " id: " + req_id + "\nPoster: " + \
                          movie['poster']
            elif req_type == 'tv':
                tv = Dict['tv'][req_id]
                user = tv['user'] if tv['user'] else "A user"
                title = "Plex Request Channel - New TV Show Request"
                message = user + " has requested a new tv show.\n" + tv['title'] + "\n" + \
                          tv.get('source', "TVDB") + " id: " + req_id + "\nPoster: " + \
                          tv['poster']
            elif req_type == 'music':
                music = Dict['music'][req_id]
                user = music['user'] if music['user'] else "A user"
                title = "Plex Request Channel - New Album Request"
                message = user + " has requested a new album.\n" + music['title'] + "\n" + \
                          music.get('source', "MusicBrainz") + " id: " + req_id + "\nPoster: " + \
                          music['poster']
            else:
                return
            response = sendPushalot(title, message)
            if response:
                Log.Debug("Pushalot notification sent for :" + req_id)
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug("Pushalot failed: " + e.message)
    if Prefs['email_to']:
        try:
            if req_type == 'movie':
                movie = Dict['movie'][req_id]
                title = movie['title'] + " (" + movie['year'] + ")"
                poster = movie['poster']
                user = movie['user'] if movie['user'] else "A user"
                id_type = movie.get('source', "IMDB")
                subject = "Plex Request Channel - New Movie Request"
                summary = ""
                if movie['summary']:
                    summary = movie['summary'] + "<br>\n"
            elif req_type == 'tv':
                tv = Dict['tv'][req_id]
                title = tv['title']
                user = tv['user'] if tv['user'] else "A user"
                id_type = tv.get('source', "TVDB")
                poster = tv['poster']
                subject = "Plex Request Channel - New TV Show Request"
                summary = ""
                if tv['summary']:
                    summary = tv['summary'] + "<br>\n"
            elif req_type == 'music':
                music = Dict['music'][req_id]
                title = music.get('title')
                user = music.get('user', "A user")
                id_type = music.get('source', "musicbrainz")
                poster = music['poster']
                subject = "Plex Request Channel - New Album Request"
                summary = ""
            else:
                return
            message = user + " has made a new request! <br><br>\n" + \
                      "<font style='font-size:20px; font-weight:bold'> " + title + " </font><br>\n" + \
                      "(" + id_type + " id: " + req_id + ") <br>\n" + \
                      summary + \
                      "<Poster:><img src= '" + poster + "' width='300'>"
            sendEmail(subject, message, 'html')
            Log.Debug("Email notification sent for: " + req_id)
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug("Email failed: " + e.message)


def Notify(title, body, devices=None):
    if Prefs['email_to']:
        try:
            if not sendEmail(title, body, 'html'):
                Log.Debug("Email notification sent")
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug("Email failed: " + e.message)
    if Prefs['pushbullet_api']:
        try:
            if devices:
                for d in devices.split(','):
                    if sendPushBullet(title, body, d):
                        Log.Debug("Pushbullet notification sent to " + d)
            elif sendPushBullet(title, body):
                Log.Debug("Pushbullet notification sent")
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug("PushBullet failed: " + e.message)
    if Prefs['pushover_user']:
        try:
            if sendPushover(title, body):
                Log.Debug("Pushover notification sent")
        except Exception as e:
            Log.Error(str(traceback.format_exc()))  # raise e
            Log.Debug("Pushover failed: " + e.message)


def sendPushBullet(title, body, device_iden=""):
    api_header = {'Authorization': 'Bearer ' + Prefs['pushbullet_api'],
                  'Content-Type': 'application/json'
                  }
    data = {'type': 'note', 'title': title, 'body': body}
    if device_iden:
        data['device_iden'] = device_iden
    if Prefs['pushbullet_channel']:
        data['channel_tag'] = Prefs['pushbullet_channel']
    values = JSON.StringFromObject(data)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    pushBulletRequest = urllib2.Request(PUSHBULLET_API_URL + "pushes", data=values, headers=api_header)
    return urllib2.urlopen(pushBulletRequest,context=ctx)


def sendPushover(title, message):
    data = {'token': Prefs['pushover_api'], 'user': Prefs['pushover_user'], 'title': title, 'message': message}
    return HTTP.Request(PUSHOVER_API_URL, values=data)


def sendPushalot(title, message):
    data = {'AuthorizationToken': Prefs['pushalot_api'], 'Title': title, 'Body': message, 'IsImportant': 'false',
            'IsSilent': 'false'}
    return HTTP.Request(PUSHALOT_API_URL, values=data)


# noinspection PyUnresolvedReferences
def sendEmail(subject, body, email_type='html'):
    from email.MIMEText import MIMEText
    from email.MIMEMultipart import MIMEMultipart
    from email.Utils import formatdate
    import smtplib

    msg = MIMEMultipart()
    msg['From'] = Prefs['email_from']
    msg['To'] = Prefs['email_to']
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(body, email_type))
    server = smtplib.SMTP(Prefs['email_server'], int(Prefs['email_port']))
    if Prefs['email_secure']:
        server.ehlo()
        server.starttls()
        server.ehlo()
    if Prefs['email_username']:
        server.login(Prefs['email_username'], Prefs['email_password'])
    text = msg.as_string()
    senders = server.sendmail(Prefs['email_from'], Prefs['email_to'], text)
    server.quit()
    return senders


def isClient(obj_list):
    return Client.Platform in obj_list or Client.Product in obj_list


def userFromToken(token):
    if token in Dict['register']:
        if Dict['register'][token]['nickname']:
            return Dict['register'][token]['nickname']
        else:
            return "guest_" + Hash.SHA1(token)[:10]
    return ""

