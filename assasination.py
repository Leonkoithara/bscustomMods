import bs

def bsGetAPIVersion():
    return 4

def bsGetGames():
    return [Assasination]

def bsGetLevels():
    return [bs.Level('Assasination', displayName='${GAME}', gameType=testGame, settings={}, previewTexName='cragCastlePreview')]

class testGame(bs.TeamGameActivity):
    @classmethod
    def getName(cls):
        return 'Assasination'

    @classmethod
    def getDescription(cls, sessionType):
        return 'Survive the hordes of crazed murderers'

    @classmethod
    def getSupportedMaps(cls, sessionType):
        return ['Crag Castle']

    @classmethod
    def supportsSessionType(cls, sessionType):
        return True if issubclass(sessionType, bs.CoopSession) else False

    def onBegin(self):
        bs.TeamGameActivity.onBegin(self)

        self._wave = 0;

        self._bots = bs.BotSet()

        self._botSpawnTimer = bs.Timer(3000, bs.WeakCall(self.spawnBots))

    def handleMessage(self, m):
        if isinstance(m, bs.PlayerSpazDeathMessage):
            self.endGame()

    def spawnBots(self):
        # self._bots.spawnBot(bs.PirateBot, pos=(6,7,-6))
        # self._bots.spawnBot(bs.PirateBot, pos=(-3,10,-2))
        # self._bots.spawnBot(bs.PirateBot, pos=(5, 6, -2))
        # self._bots.spawnBot(bs.PirateBot, pos=(-6, 7, -6))

    def endGame(self):
        #self._timer.stop()

        results = bs.TeamGameResults()

        elapsedTime = bs.getGameTime()

        for team in self.teams: 
            results.setTeamScore(team,elapsedTime/1000)

        self.end(results=results)
