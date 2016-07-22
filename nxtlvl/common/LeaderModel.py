from pprint import pprint
from PIL import Image, ImageDraw, ImageFont
from os import path


class LeaderModel:
    DIFFICULTY_LOW = 1
    DIFFICULTY_MEDIUM = 2
    DIFFICULTY_HIGH = 3

    TYPE_A = 'A'
    TYPE_B = 'B'
    TYPE_C = 'C'


    def __init__(self):
        self.diameter = 18

        base = path.dirname(__file__)

        self.im = Image.open(base + '/leadermodel.jpg')
        self.draw = ImageDraw.Draw(self.im)
        self.font = ImageFont.load(base + '/timB18.pil')

        self.currentNum = 0
        self.tutorInsetColor = (71, 191, 241)
        self.coachInsetColor = (91, 149, 176)
        self.managerInsetColor = (106, 151, 174)
        self.employees = []
        self.employee_numbers = {}

        self.fontColors = (
            (84, 128, 192),
            (104, 199, 241),
            (101, 190, 199),
            (48, 165, 132),
            (111, 131, 77),
            (230, 202, 10),
            (242, 186, 82),
            (197, 37, 43),
            (232, 71, 103),
            (40, 42, 89)
        )

        self.circleCoordinates = {
            self.DIFFICULTY_HIGH: {
                self.TYPE_A: (
                    (725, 124), (765, 124), (805, 124), (871, 124), (911, 124), (951, 124),
                    (725, 164), (765, 164), (805, 164), (871, 164), (911, 164), (951, 164),
                    (725, 204), (765, 204), (805, 204), (871, 204), (911, 204), (951, 204),
                    (725, 244), (911, 244), (951, 244),
                ),
                self.TYPE_B: (
                    (453, 124), (493, 124), (533, 124), (598, 124), (638, 124), (678, 124),
                    (453, 164), (493, 164), (533, 164), (598, 164), (638, 164), (678, 164),
                    (453, 204), (493, 204), (533, 204), (598, 204), (638, 204), (678, 204),
                    (598, 244), (638, 244), (678, 244),
                ),
                self.TYPE_C: (
                    (181, 124), (221, 124), (261, 124), (325, 124), (365, 124), (405, 124),
                    (181, 164), (221, 164), (261, 164), (325, 164), (365, 164), (405, 164),
                    (181, 204), (221, 204), (261, 204), (325, 204), (365, 204), (405, 204),
                    (325, 244), (365, 244), (405, 244),
                ),
            },
            self.DIFFICULTY_MEDIUM: {
                self.TYPE_A: (
                    (725, 445), (765, 445), (805, 445),
                    (725, 485), (765, 485), (805, 485), (871, 485), (911, 485), (951, 485),
                    (725, 525), (765, 525), (805, 525), (871, 525), (911, 525), (951, 525),
                    (725, 565), (765, 565), (805, 565), (871, 565), (911, 565), (951, 565),
                ),
                self.TYPE_B: (
                    (453, 405), (493, 405), (533, 405), (598, 405), (638, 405), (678, 405),
                    (453, 445), (493, 445), (533, 445), (598, 445), (638, 445), (678, 445),

                    (453, 565), (493, 565), (533, 565), (598, 565), (638, 565), (678, 565),
                    (598, 605), (638, 605), (678, 605),
                ),
                self.TYPE_C: (  # (181, 295), (221, 295), (261, 295),
                                # (181, 335), (221, 335), (261, 335),		(325, 335), (365, 335), (405, 335),

                                (181, 405), (221, 405), (261, 405), (325, 405), (365, 405), (405, 405),
                                (325, 445), (365, 445), (405, 445),
                                (325, 485), (365, 485), (405, 485),

                                (181, 525), (221, 525), (261, 525),
                                (181, 565), (221, 565), (261, 565),
                                (181, 605), (221, 605), (261, 605),

                                ),
            },
            self.DIFFICULTY_LOW: {
                self.TYPE_A: (

                    (725, 763), (765, 763), (805, 763), (871, 763), (911, 763), (951, 763),
                    (871, 803), (911, 803), (951, 803),  # (725, 843),  # (725, 883),	(765, 883), (805, 883),
                ),
                self.TYPE_B: (
                    (453, 763), (493, 763), (533, 763),
                    (453, 803), (493, 803), (533, 803), (598, 803), (638, 803), (678, 803),
                    (453, 843), (493, 843), (533, 843), (598, 843), (638, 843), (678, 843),
                    (453, 883), (493, 883), (533, 883), (598, 883), (638, 883), (678, 883),
                ),
                self.TYPE_C: (
                    (181, 803), (221, 803), (261, 803), (325, 803), (365, 803), (405, 803),
                    (181, 843), (221, 843), (261, 843), (325, 843), (365, 843), (405, 843),
                    (181, 883), (221, 883), (261, 883), (325, 883), (365, 883), (405, 883),
                ),
            }
        }

        self.circles = {
            self.DIFFICULTY_HIGH: {
                self.TYPE_A: {'max': 21, 'actions': []},
                self.TYPE_B: {'max': 21, 'actions': []},
                self.TYPE_C: {'max': 21, 'actions': []}
            },
            self.DIFFICULTY_MEDIUM: {
                self.TYPE_A: {'max': 21, 'actions': []},
                self.TYPE_B: {'max': 21, 'actions': []},
                self.TYPE_C: {'max': 21, 'actions': []}
            },
            self.DIFFICULTY_LOW: {
                self.TYPE_A: {'max': 9, 'actions': []},
                self.TYPE_B: {'max': 21, 'actions': []},
                self.TYPE_C: {'max': 18, 'actions': []}
            }
        }


    def addCircle(self, action):
        """

        :param action: Action
        :return: int the number that will be written in the circle.
        """

        con = self.circles[action.difficulty][action.type]

        if len(con['actions']) - 1 == con['max']:
            # todo test this in browser
            raise Exception('Too many cirles added for difficulty "{0}" type "{1}"'.format(
                action.difficulty, action.type
            ))

        con['actions'].append(action)

        if not action.employee.id in self.employees:
            self.employees.append(action.employee.id)

        if not action.employee.id in self.employee_numbers:
            self.employee_numbers[action.employee.id] = []

        self.employee_numbers[action.employee.id].append(action.id)

        return len(self.employee_numbers[action.employee.id])

    def getEmployeeColors(self, only_id=None):

        colors = {}

        for i, val in enumerate(self.employees):
            if only_id and val == only_id:
                return self.fontColors[i]
            colors[val] = self.fontColors[i]

        return colors

    def drawCircle(self, center, text, action):
        """

        :param center:
        :param text: str
        :return:
        """

        textXOffset = 6 if len(text) is 1 else 12

        color = (0, 0, 0)

        for i, val in enumerate(self.employees):
            if val == action.employee.id:
                color = self.fontColors[i]
                break

        draw = ImageDraw.Draw(self.im)
        # (545, 775, 575, 805)
        bbox = (
            center[0] - self.diameter,
            center[1] - self.diameter,
            center[0] + self.diameter,
            center[1] + self.diameter
        )
        draw.ellipse(bbox, fill=(255, 255, 255), outline=self.tutorInsetColor)
        draw.text((center[0] - textXOffset, center[1] - 14), text, fill=color, font=self.font)

    def getNextNum(self):
        self.currentNum += 1
        return str(self.currentNum)


    def writeImage(self, filename):

        for difficulty in self.circles:
            for type in self.circles[difficulty]:

                for i, val in enumerate(self.circles[difficulty][type]['actions']):

                    # Find the circle number
                    empl_action_cnt = 0

                    for actionid in self.employee_numbers[val.employee.id]:
                        empl_action_cnt += 1
                        if actionid == val.id:
                            break

                            # if not val.employee.id in self.employee_numbers:
                            # self.employee_numbers[val.employee.id] = []
                    #
                    # self.employee_numbers[val.employee.id].append(val.id)

                    # self.drawCircle(self.circleCoordinates[difficulty][type][i], str(i + 1), val)
                    self.drawCircle(
                        self.circleCoordinates[difficulty][type][i],
                        str(empl_action_cnt),  # str(len(self.employee_numbers[val.employee.id])),
                        val
                    )

        out = open(filename, 'w')
        self.im.save(out, 'PNG')


#
# Test code
#

if __name__ == '__main__':
    class Employee:
        def __init__(self, eId):
            self.id = eId

    class Action:
        def __init__(self, aId, eId, aDifficulty, aType):
            self.id = aId
            self.employee = Employee(eId)
            self.difficulty = aDifficulty
            self.type = aType

    lm = LeaderModel()

    lm.addCircle(Action(1, 1, LeaderModel.DIFFICULTY_HIGH, LeaderModel.TYPE_A))
    lm.addCircle(Action(2, 1, LeaderModel.DIFFICULTY_HIGH, LeaderModel.TYPE_B))
    lm.addCircle(Action(3, 1, LeaderModel.DIFFICULTY_HIGH, LeaderModel.TYPE_C))
    lm.addCircle(Action(4, 2, LeaderModel.DIFFICULTY_HIGH, LeaderModel.TYPE_A))
    lm.addCircle(Action(5, 2, LeaderModel.DIFFICULTY_HIGH, LeaderModel.TYPE_B))
    lm.addCircle(Action(6, 2, LeaderModel.DIFFICULTY_HIGH, LeaderModel.TYPE_C))
    lm.addCircle(Action(7, 3, LeaderModel.DIFFICULTY_HIGH, LeaderModel.TYPE_A))
    lm.addCircle(Action(8, 3, LeaderModel.DIFFICULTY_HIGH, LeaderModel.TYPE_B))
    lm.addCircle(Action(9, 3, LeaderModel.DIFFICULTY_HIGH, LeaderModel.TYPE_C))

    lm.addCircle(Action(10, 4, LeaderModel.DIFFICULTY_MEDIUM, LeaderModel.TYPE_A))
    lm.addCircle(Action(11, 4, LeaderModel.DIFFICULTY_MEDIUM, LeaderModel.TYPE_B))
    lm.addCircle(Action(12, 4, LeaderModel.DIFFICULTY_MEDIUM, LeaderModel.TYPE_C))
    lm.addCircle(Action(13, 5, LeaderModel.DIFFICULTY_MEDIUM, LeaderModel.TYPE_A))
    lm.addCircle(Action(14, 5, LeaderModel.DIFFICULTY_MEDIUM, LeaderModel.TYPE_B))
    lm.addCircle(Action(15, 5, LeaderModel.DIFFICULTY_MEDIUM, LeaderModel.TYPE_C))
    lm.addCircle(Action(16, 6, LeaderModel.DIFFICULTY_MEDIUM, LeaderModel.TYPE_A))
    lm.addCircle(Action(17, 6, LeaderModel.DIFFICULTY_MEDIUM, LeaderModel.TYPE_B))
    lm.addCircle(Action(18, 6, LeaderModel.DIFFICULTY_MEDIUM, LeaderModel.TYPE_C))

    lm.addCircle(Action(19, 7, LeaderModel.DIFFICULTY_LOW, LeaderModel.TYPE_A))
    lm.addCircle(Action(20, 7, LeaderModel.DIFFICULTY_LOW, LeaderModel.TYPE_B))
    lm.addCircle(Action(21, 7, LeaderModel.DIFFICULTY_LOW, LeaderModel.TYPE_C))
    lm.addCircle(Action(22, 8, LeaderModel.DIFFICULTY_LOW, LeaderModel.TYPE_A))
    lm.addCircle(Action(23, 8, LeaderModel.DIFFICULTY_LOW, LeaderModel.TYPE_B))
    lm.addCircle(Action(24, 8, LeaderModel.DIFFICULTY_LOW, LeaderModel.TYPE_C))
    lm.addCircle(Action(25, 9, LeaderModel.DIFFICULTY_LOW, LeaderModel.TYPE_A))
    lm.addCircle(Action(26, 9, LeaderModel.DIFFICULTY_LOW, LeaderModel.TYPE_B))
    lm.addCircle(Action(27, 9, LeaderModel.DIFFICULTY_LOW, LeaderModel.TYPE_C))
    lm.addCircle(Action(28, 10, LeaderModel.DIFFICULTY_LOW, LeaderModel.TYPE_A))
    lm.addCircle(Action(29, 10, LeaderModel.DIFFICULTY_LOW, LeaderModel.TYPE_B))
    lm.addCircle(Action(30, 10, LeaderModel.DIFFICULTY_LOW, LeaderModel.TYPE_C))

    lm.writeImage('leadermodel_test.png')




