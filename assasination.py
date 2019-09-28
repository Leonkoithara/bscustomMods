import bs
import random

def bsGetAPIVersion():
    return 4

def bsGetGames():
    return [Assasination]

def bsGetLevels():
    return [bs.Level('Assasination', displayName='${GAME}', gameType=testGame, settings={}, previewTexName='bridgitPreview')]

class testGame(bs.TeamGameActivity):
    @classmethod
    def getName(cls):
        return 'Assasination'

    @classmethod
    def getDescription(cls, sessionType):
        return 'Survive the hordes of crazed murderers'

    @classmethod
    def getSupportedMaps(cls, sessionType):
        return ['Bridgit']

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
        self._botProb = [   0.25,
                            0.05,
                            0.05,
                            0.25,
                            0.05,
                            0.05,
                            0.05,
                            0.1,
                            0.02,
                            0.02,
                            0.1,
                            0.01]

        self._botSpawnProbs = []
        psum = 0
        for i in self._botProb:
            psum += i
            self._botSpawnProbs.append(psum)

    def onBegin(self):
        bs.TeamGameActivity.onBegin(self)

        self._wave = 0;

        self._bots = bs.BotSet()
        self.setupStandardPowerupDrops()

        bs.gameTimer(3500, bs.WeakCall(self.spawnBots))
        #bs.gameTimer(2000, bs.WeakCall(self.dropPowerup))

    def handleMessage(self, m):
        if isinstance(m, bs.PlayerSpazDeathMessage):
            self.endGame()

    def spawnBots(self):
        botSpawnPoints = [(5.5, 3, -1.5), (-5.5, 3, -1.5)]
        r = random.random()
        for i in range(len(self._botSpawnTypes)):
            if(r < self._botSpawnProbs[i]):
                break
        p1 = random.randint(0, 1)
        self._bots.spawnBot(self._botSpawnTypes[i], pos=botSpawnPoints[p1])

        r = random.random()
        for i in range(len(self._botSpawnTypes)):
            if(r < self._botSpawnProbs[i]):
                break
        p2 = random.randint(0, 1)
        self._bots.spawnBot(self._botSpawnTypes[i], pos=botSpawnPoints[p2])

        bs.gameTimer(5500, bs.WeakCall(self.spawnBots), repeat=False)

    def dropPowerup(self):
        powerupSpawnPt = (5.5, 3, -1.5)
        powerupType = bs.Powerup.getFactory().getRandomPowerupType()
        bs.screenMessage(powerupType)
        bs.Powerup(position=powerupSpawnPt, powerupType=powerupType).autoRetain()

    def endGame(self):
        results = bs.TeamGameResults()

        elapsedTime = bs.getGameTime()

        for team in self.teams: 
            results.setTeamScore(team,elapsedTime/1000)

        self.end(results=results)
