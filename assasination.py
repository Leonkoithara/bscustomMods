import bs
import random

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

    def __init__(self, settings):
        bs.TeamGameActivity.__init__(self, settings) 

        self._botSpawnTypes = [ bs.BomberBot, 
                                bs.BomberBotPro, 
                                bs.BomberBotProShielded,
                                bs.ToughGuyBot,
                                bs.ToughGuyBotPro,
                                bs.ToughGuyBotProShielded,
                                bs.ChickBot,
                                bs.ChickBotPro,
                                bs.ChickBotProShielded,
                                bs.NinjaBot,
                                bs.MelBot,
                                bs.PirateBot]
        self._botSpawnProbs = [ 0.2,
                                0.225,
                                0.25,
                                0.45,
                                0.5,
                                0.55,
                                0.6,
                                0.7,
                                0.75,
                                0.85,
                                0.95,
                                1.0]

    def onBegin(self):
        bs.TeamGameActivity.onBegin(self)

        self._wave = 0;

        self._bots = bs.BotSet()

        bs.gameTimer(3500, bs.WeakCall(self.spawnBots), repeat=True)

    def handleMessage(self, m):
        if isinstance(m, bs.PlayerSpazDeathMessage):
            self.endGame()

    def spawnBots(self):
        botSpawnPoints = [(5, 6, -2), (6, 10, -5.5), (-3, 10, -5.5), (-5, 6, -2)]
        r = random.random()
        for i in range(len(self._botSpawnTypes)):
            if(r < self._botSpawnProbs[i]):
                break

        p1 = random.randint(0, 3)

        self._bots.spawnBot(self._botSpawnTypes[i], pos=botSpawnPoints[p1])

    def endGame(self):
        #self._timer.stop()

        results = bs.TeamGameResults()

        elapsedTime = bs.getGameTime()

        for team in self.teams: 
            results.setTeamScore(team,elapsedTime/1000)

        self.end(results=results)
