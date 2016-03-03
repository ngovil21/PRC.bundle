#Modified version of DumbTools for Plex v1.1 by Cory <babylonstudio@gmail.com>

KEYS = list('abcdefghijklmnopqrstuvwxyz1234567890-=;[]\\\',./')
SHIFT_KEYS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+:{}|\"<>?')

TITLE = 'Plex Request Channel'
PREFIX = '/video/plexrequestchannel'


DUMB_KEYBOARD_CLIENTS = ['Plex for iOS', 'Plex Media Player', 'Plex Home Theater', 'OpenPHT', 'Plex for Roku', 'iOS', 'Roku', 'tvOS' 'Konvergo',
                         'Plex for Apple TV', 'Plex for Xbox 360', 'Plex for Xbox One', 'Xbox One', 'Mystery 4', 'Plex for Vizio', 'Plex TV']

NO_MESSAGE_CONTAINER_CLIENTS = ['Plex for iOS', 'tvOS', 'Plex for Apple TV', 'Plex for Xbox One', 'iOS', 'Mystery 4', 'Samsung', 'Plex for Samsung']

MESSAGE_OVERLAY_CLIENTS = ['Android', 'Roku', 'Konvergo', 'Plex Web']


@route(PREFIX + "/dumbtools/keyboard")
def Keyboard(query=None, callback=None, parent_call=None, shift=False, secure='False', locked='locked', title="Search", message=None):
    if 'DumbKeyboard-History' not in Dict:
        Dict['DumbKeyboard-History'] = []

    if not query:
        Log.Debug("Keyboard created.")
    if secure == 'True' and query is not None:
        string = ''.join(['*' for i in range(len(query[:-1]))]) + query[-1]
    else:
        string = query if query else ""
    if Client.Platform in MESSAGE_CONTAINER_CLIENTS or Client.Product in MESSAGE_CONTAINER_CLIENTS:
        oc = ObjectContainer(title1=title, title2=string, message=message)
    else:
        oc = ObjectContainer(title1=title, title2=string)
    # Submit
    # Log.Debug("Create Submit key")
    oc.add(DirectoryObject(key=Callback(callback, query=query, locked=locked), title=u'%s: %s' % (L('Submit'), string)))
    # Search History
    if Dict['DumbKeyboard-History']:
        # Log.Debug("Create History")
        oc.add(
            DirectoryObject(key=Callback(History, query=query, callback=callback, locked=locked, secure=secure), title=u'%s' % L('Search History')))
    # Space
    # Log.Debug("Create Space Key")
    oc.add(DirectoryObject(key=Callback(Keyboard, query=query + " " if query else " ", callback=callback,parent_call=parent_call, locked=locked, secure=secure, title=title),
                           title=L('Space')))
    # Backspace (not really needed since you can just hit back)
    if query is not None:
        # Log.Debug("Create backspace key")
        oc.add(DirectoryObject(
            key=Callback(Keyboard, query=query[:-1], callback=callback, parent_call=parent_call, locked=locked, secure=secure, title=title),
            title=L('Backspace')))
    # Shift
    # Log.Debug("Create Shift Key")
    oc.add(
        DirectoryObject(
            key=Callback(Keyboard, query=query, callback=callback, parent_call=parent_call, locked=locked, secure=secure, shift=True, title=title),
            title=L('Shift')))
    # Keys
    # Log.Debug("Generating keys")
    if parent_call:
        oc.add(DirectoryObject(key=parent_call, title=L("Cancel")))
    for key in KEYS if not shift else SHIFT_KEYS:
        oc.add(
            DirectoryObject(key=Callback(Keyboard, query=query + key if query else key, callback=callback, parent_call=parent_call, locked=locked, secure=secure, title=title),
                            title=u'%s' % key))
    # Log.Debug("Return Object Container")
    return oc


@route(PREFIX + "/dumbtools/history")
def History(query=None, callback=None, parent_call=None, locked='locked', secure='False'):
    oc = ObjectContainer()
    oc.add(DirectoryObject(key=Callback(Keyboard, query=query, callback=callback, parent_call=parent_call, locked=locked, secure=secure),
                           title=L("Return to Keyboard")))
    if Dict['DumbKeyboard-History']:
        oc.add(DirectoryObject(key=Callback(ClearHistory, callback=callback, parent_call=parent_call, locked=locked, secure=secure),
                               title=u'%s' % L('Clear History')))
    for item in Dict['DumbKeyboard-History']:
        oc.add(DirectoryObject(key=Callback(callback, query=item, locked=locked),
                               title=u'%s' % item))
    return oc


@route(PREFIX + "/dumbtools/clearhistory")
def ClearHistory(query="", callback=None, parent_call=None, locked='locked', secure='False'):
    Dict['DumbKeyboard-History'] = []
    Dict.Save()
    return Keyboard(query=query, callback=callback, parent_call=parent_call, locked=locked, secure=secure)


@route(PREFIX + "/dumbtools/addhistory")
def AddHistory(query):
    if query not in Dict['DumbKeyboard-History']:
        Dict['DumbKeyboard-History'].append(query)
        Dict.Save()

# @route(PREFIX + "/dumbtools/submit")
# def Submit(query, callback=callback, locked=locked):
#     self.AddHistory(query)
#     kwargs = {'query': query}
#     kwargs.update(self.callback_args)
#     return Callback(**kwargs)
