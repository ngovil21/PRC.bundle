#API Package for Request Channel.
#import and add classes to system modules

import sys

import Couchpotato
sys.modules["api.Couchpotato"] = Couchpotato

import Email
sys.modules["api.Email"] = Email

import OpenMovieDatabase
sys.modules["api.OpenMovieDatabase"] = OpenMovieDatabase

import Pushalot
sys.modules["api.Pushalot"] = Pushalot

import Pushbullet
sys.modules["api.Pushbullet"] = Pushbullet

import Pushover
sys.modules["api.Pushover"] = Pushover

import Telegram
sys.modules["api.Telegram"] = Telegram

import Radarr
sys.modules["api.Radarr"] = Radarr

import Sickbeard
sys.modules["api.Sickbeard"] = Sickbeard

import Slack
sys.modules["api.Slack"] = Slack

import Discord
sys.modules["api.Discord"] = Discord

import Sonarr
sys.modules["api.Sonarr"] = Sonarr

import TheMovieDatabase
sys.modules["api.TheMovieDatabase"] = TheMovieDatabase

import theTVDB
sys.modules["api.theTVDB"] = theTVDB

import Plex
sys.modules["api.Plex"] = Plex

