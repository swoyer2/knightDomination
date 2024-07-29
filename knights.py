from manim import *
import math

board3 = [0, 0, 0, 0, 1, 0, 1, 1, 1]
board4 = [0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0]
board5 = [0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0]
board6 = [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
board7 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
board8 = [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]

allBoards = [board3, board4, board5, board6, board7, board8]

class array(MovingCameraScene):
    def construct(self):
        fields = []
        for board in allBoards:
            field = VGroup(*[Square(side_length=1.5) for _ in range(len(board))])
            field.arrange_in_grid(rows=int(math.sqrt(len(board))),cols=int(math.sqrt(len(board))),buff=0)
            fields.append(field)

        # Intro
        #self.intro(fields)

        # Three proof
        #self.threeProof(fields)

        # Four proof
        knight = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[1][6].get_center())
        knight4 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[1][9].get_center())
        knight2 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[1][5].get_center())
        knight3 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[1][10].get_center())
        attacks1 = VGroup()
        attacks2 = VGroup()
        attacks3 = VGroup()
        attacks4 = VGroup()
        attacks1.add(self.getAttacks(6, 4, fields[1]))
        attacks4.add(self.getAttacks(9, 4, fields[1]))
        attacks2.add(self.getAttacks(5, 4, fields[1]))
        attacks3.add(self.getAttacks(10, 4, fields[1]))
        self.play(DrawBorderThenFill(fields[1]))
        self.wait()
        three = fields[0].shift(LEFT*.76).shift(UP*.76).set_color(YELLOW)
        self.play(Create(three))
        self.wait()
        self.play(FadeIn(knight), FadeIn(attacks1))
        self.play(FadeIn(knight2), FadeIn(attacks2))
        self.play(FadeIn(knight3), FadeIn(attacks3))
        self.play(FadeIn(knight4), FadeIn(attacks4))
        self.wait()

        # # Shows all board states (Probably final section just for satisfaction)
        # currentField = fields[0]

        # for i, field in enumerate(fields):
        #     self.play(Transform(currentField, field))
        #     self.play(self.camera.frame.animate.set(width=field.width * 3.0))

        #     self.show(allBoards[i], field)
            
        #     self.wait()

    def getAttacks(self, index, size, field):
        moves = [(1,2), (-1,2), (1,-2), (-1,-2), (2,1), (-2,1), (2,-1), (-2,-1)]
        possibleAttacks = []
        attacks = VGroup()

        cord = self.indexToCord(index, size)

        for move in moves:
            possibleAttacks.append([cord[0]+move[0], cord[1]+move[1]])

        for attack in possibleAttacks:
            if attack[0] < 0 or attack[1] < 0 or attack[0] > size-1 or attack[1] > size-1:
                pass
            else:
                attacks.add(Circle().scale(0.25).scale(0.5).move_to(field[self.cordToIndex(attack, size)].get_center()))

        return attacks


    def indexToCord(self, index, size):
        return index % size, math.floor(index/size)

    def cordToIndex(self, cord, size):
        return cord[1] * size + cord[0]

    def show(self, board, field):
        everything = VGroup()
        for i, ele in enumerate(board):
            if ele:
                attacks = VGroup()
                knight = SVGMobject('WKnight.svg').scale(0.5).move_to(field[i].get_center())
                attacks.add(self.getAttacks(i, int(math.sqrt(len(board))), field))
                everything.add(attacks, knight)
                self.play(FadeIn(knight))
                self.play(FadeIn(attacks))
                self.wait()
            
        self.play(FadeOut(everything))

    def intro(self, fields):
        # Beginning showing how knight moves
        knight = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[4][24].get_center())
        self.play(self.camera.frame.animate.set(width=24))
        self.play(DrawBorderThenFill(fields[4]))
        self.play(Create(knight))

        attacks = VGroup()
        attacks.add(self.getAttacks(24, 7, fields[4]))
        tempCircle = Circle().scale(0.25).scale(0.5).move_to(fields[4][19].get_center())
        self.play(FadeIn(tempCircle))

        arrow1 = Arrow(0*LEFT, 3.25*RIGHT, color=YELLOW)
        arrow2 = Arrow(arrow1.get_end(), arrow1.get_end()+1.5*UP, color=YELLOW)
        self.play(GrowArrow(arrow1))
        self.play(GrowArrow(arrow2))

        self.play(FadeIn(attacks), FadeOut(arrow1, arrow2), FadeOut(tempCircle))
        self.wait()

        # Showing how knights act on edge of board
        knight.generate_target()
        knight.target.shift(fields[4][21].get_center())
        attacks.generate_target()
        attacks.target.shift(fields[4][21].get_center())
        self.play(MoveToTarget(knight), MoveToTarget(attacks))
        self.wait()
        self.play(Uncreate(attacks[0][1]), Uncreate(attacks[0][3]), Uncreate(attacks[0][5]), Uncreate(attacks[0][7]))
        self.wait()

        # Explanation of problem
        self.play(FadeOut(attacks), Uncreate(knight))
        self.wait()

        allCircles = VGroup()
        for i in range(49):
            allCircles.add(Circle().scale(0.25).scale(0.5).move_to(fields[4][i].get_center()))
        self.play(FadeIn(allCircles))
        self.wait()
        self.clear()

    def threeProof(self, fields):
        # Show 3x3 Proof
        knight = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[0][4].get_center())
        attacks = VGroup()
        attacks.add(self.getAttacks(4, 3, fields[0]))
        self.play(DrawBorderThenFill(fields[0]))
        self.play(FadeIn(knight), FadeIn(attacks))
        
        knight.generate_target()
        knight.target.shift(fields[0][0].get_center())
        threeList = [Integer(number=3).set_color(YELLOW).move_to(fields[0][0].get_center()),
        Integer(number=3).set_color(YELLOW).move_to(fields[0][1].get_center()),
        Integer(number=3).set_color(YELLOW).move_to(fields[0][2].get_center()),
        Integer(number=3).set_color(YELLOW).move_to(fields[0][5].get_center()),
        Integer(number=3).set_color(YELLOW).move_to(fields[0][8].get_center()),
        Integer(number=3).set_color(YELLOW).move_to(fields[0][7].get_center()),
        Integer(number=3).set_color(YELLOW).move_to(fields[0][6].get_center()),
        Integer(number=3).set_color(YELLOW).move_to(fields[0][3].get_center())]

        one = Integer(number=1).set_color(YELLOW).move_to(fields[0][4].get_center())
        self.play(FadeIn(one), MoveToTarget(knight))
        self.wait()
        knight.target.shift(RIGHT*3)
        self.play(FadeIn(threeList[0]), FadeIn(threeList[1]), MoveToTarget(knight))
        knight.target.shift(DOWN*3)
        self.play(FadeIn(threeList[2]), FadeIn(threeList[3]), MoveToTarget(knight))
        knight.target.shift(LEFT*3)
        self.play(FadeIn(threeList[4]), FadeIn(threeList[5]), MoveToTarget(knight))
        knight.target.shift(UP*4.5)
        self.play(FadeIn(threeList[6]), FadeIn(threeList[7]), MoveToTarget(knight))
        self.wait()

        # Move knight to middle
        knight.target.shift(DOWN*3, RIGHT*math.sqrt(2))
        self.play(FadeOut(one), MoveToTarget(knight))
        
        # Show number count 8 squares left
        equation = MathTex(r"8 \neq 3+3").move_to(LEFT*5)
        equation2 = MathTex(r"8 \neq 6").move_to(LEFT*5)
        self.play(Indicate(threeList[0]), Indicate(threeList[1]), Indicate(threeList[2]), Indicate(threeList[3]), 
                Indicate(threeList[4]), Indicate(threeList[5]), Indicate(threeList[6]), Indicate(threeList[7]))
        self.wait()
        knight2 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[0][6].get_center())
        knight3 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[0][7].get_center())
        knight4 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[0][8].get_center())
        threeGroup = VGroup()
        for ele in threeList:
            threeGroup.add(ele)
        attack2 = VGroup()
        attack2.add(self.getAttacks(6, 3, fields[0]))
        attack3 = VGroup()
        attack3.add(self.getAttacks(7, 3, fields[0]))
        attack4 = VGroup() 
        attack4.add(self.getAttacks(8, 3, fields[0]))

        self.play(FadeIn(knight2), FadeOut(threeGroup), FadeIn(attack2))
        self.play(FadeIn(knight3), FadeIn(attack3))
        self.play(FadeIn(equation))
        self.play(Transform(equation, equation2))
        self.play(FadeIn(knight4), FadeIn(attack4))
        self.wait()
        self.clear()

    def fourtemp(self, fields):
        # Four Proof
        allGroup = VGroup()
        knight = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[1][6].get_center())
        knight2 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[1][9].get_center())
        knight3 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[1][5].get_center())
        knight4 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[1][10].get_center())
        attacks1 = VGroup()
        attacks2 = VGroup()
        attacks3 = VGroup()
        attacks4 = VGroup()
        attacks1.add(self.getAttacks(6, 4, fields[1]))
        attacks2.add(self.getAttacks(9, 4, fields[1]))
        attacks3.add(self.getAttacks(5, 4, fields[1]))
        attacks4.add(self.getAttacks(10, 4, fields[1]))
        self.play(DrawBorderThenFill(fields[1]))

        surrounding1, surrounding2 = SurroundingRectangle(fields[1][0], color=YELLOW, buff=MED_LARGE_BUFF).scale(0.6), SurroundingRectangle(fields[1][15], color=YELLOW, buff=MED_LARGE_BUFF).scale(0.6)
        surrounding3, surrounding4 = SurroundingRectangle(fields[1][3], color=YELLOW, buff=MED_LARGE_BUFF).scale(0.6), SurroundingRectangle(fields[1][12], color=YELLOW, buff=MED_LARGE_BUFF).scale(0.6)
        self.play(Create(surrounding1), Create(surrounding2))
        self.wait()
        self.play(FadeIn(knight), FadeIn(knight2), FadeIn(attacks1), FadeIn(attacks2))
        self.wait()
        allGroup.add(knight, knight2, attacks1, attacks2, fields[1], surrounding1, surrounding2)

        self.play(Rotate(allGroup, angle=PI))
        self.play(Rotate(knight, angle=PI, about_point=knight.get_center()), Rotate(knight2, angle=PI, about_point=knight2.get_center()))
        self.wait()

        self.play(FadeOut(knight), FadeOut(attacks1))
        self.play(FadeOut(surrounding1), FadeOut(surrounding2), FadeIn(surrounding3), FadeIn(surrounding4))
        self.play(FadeIn(knight3), FadeIn(knight4), FadeIn(attacks3), FadeIn(attacks4))
        allGroup.add(surrounding3, surrounding4, knight3, knight4)
        allGroup.remove(knight, surrounding1, surrounding2)
        self.play(Rotate(allGroup, angle=PI))
        self.wait()
        self.play(Rotate(allGroup, angle=-PI))
        self.wait()
        self.play(FadeOut(knight3), FadeOut(attacks3))
        self.wait()