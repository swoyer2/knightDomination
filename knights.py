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
        # self.fourProof(fields)

        self.play(self.camera.frame.animate.set(width=36))
        self.fiveProof(fields)

        # # Shows all board states (Probably final section just for satisfaction)
        # currentField = fields[0]

        # for i, field in enumerate(fields):
        #     self.play(Transform(currentField, field))
        #     self.play(self.camera.frame.animate.set(width=field.width * 3.0))

        #     self.show(allBoards[i], field)
            
        #     self.wait()
    def getPostionOfAttack(self, index, size, field):
        moves = [(1,2), (-1,2), (1,-2), (-1,-2), (2,1), (-2,1), (2,-1), (-2,-1)]
        possibleAttacks = []
        attacks = []

        cord = self.indexToCord(index, size)

        for move in moves:
            possibleAttacks.append([cord[0]+move[0], cord[1]+move[1]])

        for attack in possibleAttacks:
            if attack[0] < 0 or attack[1] < 0 or attack[0] > size-1 or attack[1] > size-1:
                pass
            else:
                attacks.append(self.cordToIndex(attack, size))

        return attacks
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
        self.clear()
    
    def fourProof(self, fields):
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
        self.clear()

    def fiveProof(self, fields):
        # Show contradiction statement, we assume we can do it in 4 knights
        # If that is the case then 4 knights have to cover 25 squares
        equation = Tex("5 \times 5 = 25")

        # Display the equation on the screen
        self.play(Write(equation))
        self.play(FadeOut(equation))

        self.play(DrawBorderThenFill(fields[2]))
        self.wait()
        heatMap1 = [3,4,5,4,3,
                      4,5,7,5,4,
                      5,7,9,7,5,
                      4,5,7,5,4,
                      3,4,5,4,3]
        heatMap1Group = VGroup()
        for i, num in enumerate(heatMap1):
            heatMap1Group.add(Integer(number=num).set_color(YELLOW).move_to(fields[2][i].get_center()))

        # Show how heatmap is made
        tempKnight = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[2][0].get_center())
        attacks = self.getAttacks(0, 5, fields[2])
        self.play(FadeIn(tempKnight), FadeIn(attacks))
        tempKnight.generate_target()
        for i in range(25):
            attacks = self.getAttacks(i, 5, fields[2])
            if i != 0:
                self.play(FadeIn(heatMap1Group[i-1]), MoveToTarget(tempKnight), FadeIn(attacks))
                tempKnight.target.shift(fields[2][i].get_center())
            else:
                self.play(FadeIn(heatMap1Group[0]), MoveToTarget(tempKnight), FadeIn(attacks))

        self.play(FadeOut(tempKnight), FadeOut(attacks))

        # We cannot do 3 7's because they interfere with each other

        # Show with LaTeX that we need to use the 9 square because
        # 7+7+5+5 < 25
        inequality = Tex(r"7 + 7 + 5 + 5 < 25")
        inequality.move_to(ORIGIN)
        self.play(Write(inequality))
        newInequality = Tex(r"24 < 25")
        self.play(Transform(inequality, newInequality))
        self.wait()
        self.play(FadeOut(inequality), FadeOut(newInequality))

        # Show 9 square taken
        knight = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[2][12].get_center())
        attacks = VGroup()
        attacks.add(self.getAttacks(12, 5, fields[2]))

        # Update heatmap
        heatMap2 = [3,3,5,3,3,
                    3,5,7,5,3,
                    5,7,0,7,5,
                    3,5,7,5,3,
                    3,3,5,3,3]
        heatMap2Group = VGroup()
        for i, num in enumerate(heatMap2):
            if num:
                heatMap2Group.add(Integer(number=num).set_color(YELLOW).move_to(fields[2][i].get_center()))
        self.play(FadeIn(knight), FadeIn(attacks), Transform(heatMap1Group, heatMap2Group))

        # Show we have to use a 7 square because 9+5+5+5 < 25
        inequality = Tex(r"9 + 5 + 5 + 5 < 25")
        inequality.move_to(ORIGIN)
        self.play(Write(inequality))
        newInequality = Tex(r"24 < 25")
        self.play(Transform(inequality, newInequality))
        self.wait()
        self.play(FadeOut(inequality), FadeOut(newInequality))

        allGroup = VGroup()
        allGroup.add(heatMap1Group, knight, attacks)
        self.play(Rotate(allGroup, angle=2*PI))

        # Update heatmap
        heatMap3 = [1,1,1,2,3,
                    1,3,5,1,0,
                    2,None,None,5,3,
                    1,3,5,1,0,
                    1,1,1,2,3]
        heatMap3Group = VGroup()
        for i, num in enumerate(heatMap3):
            if num != None:
                heatMap3Group.add(Integer(number=num).set_color(YELLOW).move_to(fields[2][i].get_center()))

        knight2 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[2][11].get_center())
        attacks.add(self.getAttacks(11, 5, fields[2]))

        self.play(FadeIn(knight2), FadeIn(attacks), Transform(heatMap1Group, heatMap3Group))

        # Show now we need to cover 9 squares with 2 knights, which can only be done with 2 5 squares
        # However it is impossible to have two 5 square knights because they overlap each other
        # Therefore we need 5 knights to cover a 5x5 board
        
        self.wait()
        self.clear()

    def sixProof(self, fields):
        self.play(DrawBorderThenFill(fields[3]))
        knight = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[3][13].get_center())
        knight2 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[3][14].get_center())
        knight3 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[3][15].get_center())
        knight4 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[3][16].get_center())
        knight5 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[3][19].get_center())
        knight6 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[3][20].get_center())
        knight7 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[3][21].get_center())
        knight8 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[3][22].get_center())
        attacks1 = VGroup()
        attacks2 = VGroup()
        attacks3 = VGroup()
        attacks4 = VGroup()
        attacks5 = VGroup()
        attacks6 = VGroup()
        attacks7 = VGroup()
        attacks8 = VGroup()
        attacks1.add(self.getAttacks(13, 6, fields[3]))
        attacks2.add(self.getAttacks(14, 6, fields[3]))
        attacks3.add(self.getAttacks(15, 6, fields[3]))
        attacks4.add(self.getAttacks(16, 6, fields[3]))
        attacks5.add(self.getAttacks(19, 6, fields[3]))
        attacks6.add(self.getAttacks(20, 6, fields[3]))
        attacks7.add(self.getAttacks(21, 6, fields[3]))
        attacks8.add(self.getAttacks(22, 6, fields[3]))
        AGroup = VGroup()
        BGroup = VGroup()
        CGroup = VGroup()
        DGroup = VGroup()
        letters = ['A','B','A','B','A','B',
                   None, None, None, None, None,
                   None, None, None, None, None,
                   None, None, None, None, None,
                   None, None, None, None, None,
                   'D','C','D','C','D','C']
        for index, letter in enumerate(letters):
            if letter == 'A':
                AGroup.add(Text(letter).set_color(YELLOW).move_to(fields[3][index].get_center()))
            if letter == 'B':
                BGroup.add(Text(letter).set_color(YELLOW).move_to(fields[3][index].get_center()))
            if letter == 'C':
                CGroup.add(Text(letter).set_color(YELLOW).move_to(fields[3][index].get_center()))
            if letter == 'D':
                DGroup.add(Text(letter).set_color(YELLOW).move_to(fields[3][index].get_center()))
            
        # Move knight around to show that a knight cannot touch both A and B
        tempKnight = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[3][0].get_center())

        # Show that no knight can cover more than 2 of the positions A or B

        # Show knight range is only 2 units around it so it cannot touch both ends

        # Show same stuff as before but with C and D (Just rotate and use symmetry)

        # Final board
        self.play(FadeIn(knight), FadeIn(attacks1))
        self.play(FadeIn(knight2), FadeIn(attacks2))
        self.play(FadeIn(knight3), FadeIn(attacks3))
        self.play(FadeIn(knight4), FadeIn(attacks4))
        self.play(FadeIn(knight5), FadeIn(attacks5))
        self.play(FadeIn(knight6), FadeIn(attacks6))
        self.play(FadeIn(knight7), FadeIn(attacks7))
        self.play(FadeIn(knight8), FadeIn(attacks8))

        
    def sevenProof(self, fields):
        self.play(DrawBorderThenFill(fields[4]))
        knight = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[4][15].get_center())
        knight2 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[4][16].get_center())
        knight3 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[4][17].get_center())
        knight4 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[4][18].get_center())
        knight5 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[4][19].get_center())
        knight6 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[4][29].get_center())
        knight7 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[4][30].get_center())
        knight8 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[4][31].get_center())
        knight9 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[4][32].get_center())
        knight10 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[4][33].get_center())
        attacks1 = VGroup()
        attacks2 = VGroup()
        attacks3 = VGroup()
        attacks4 = VGroup()
        attacks5 = VGroup()
        attacks6 = VGroup()
        attacks7 = VGroup()
        attacks8 = VGroup()
        attacks9 = VGroup()
        attacks10 = VGroup()
        attacks1.add(self.getAttacks(15, 7, fields[4]))
        attacks2.add(self.getAttacks(16, 7, fields[4]))
        attacks3.add(self.getAttacks(17, 7, fields[4]))
        attacks4.add(self.getAttacks(18, 7, fields[4]))
        attacks5.add(self.getAttacks(19, 7, fields[4]))
        attacks6.add(self.getAttacks(29, 7, fields[4]))
        attacks7.add(self.getAttacks(30, 7, fields[4]))
        attacks8.add(self.getAttacks(31, 7, fields[4]))
        attacks9.add(self.getAttacks(32, 7, fields[4]))
        attacks10.add(self.getAttacks(33, 7, fields[4]))
        AGroup = VGroup()
        letters = ['A', 'A', None, 1, 1, None, 'A',
                   None, 'A', 1, 1, 1, None, 'A',
                   1, 1, 1, 1, 1, 1, None,
                   1, 1, 1, None, None, 1, 1,
                   None, 1, 1, 1, 1, 1, 1,
                   'A', None, 1, 1, 1, 'A', None,
                   'A', None, 1, 1, None, 'A', 'A']
        
        for index, letter in enumerate(letters):
            if letter == 'A':
                AGroup.add(Text(letter).set_color(YELLOW).move_to(fields[4][index].get_center()))
        self.play(FadeIn(AGroup))
        # Show no knight can cover any of these spots
        tempKnight = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[4][0].get_center())
        tempKnight.generate_target()
        attacks = self.getAttacks(0, 7, fields[4])
        for i in range(49):
            if i:
                self.play(FadeOut(attacks))
                tempKnight.target.shift(1.5 * RIGHT)
                if i % 7 == 0:
                    tempKnight.target.shift(1.5 * DOWN)
                    tempKnight.target.shift(1.5 * 7 * LEFT)
            attacks = self.getAttacks(i, 7, fields[4])
            if letters[i] == "A":
                # emphasize A
                pass
            if letters[i] == 1:
                positions = self.getPostionOfAttack(i, 7, fields[4])
                for pos in positions:
                    if letters[pos] == "A":
                        # Emphasize A
                        pass

            self.play(MoveToTarget(tempKnight), FadeIn(attacks))

        self.play(FadeOut(tempKnight), FadeOut(attacks))
        # Final Board
        self.play(FadeIn(knight), FadeIn(attacks1))
        self.play(FadeIn(knight2), FadeIn(attacks2))
        self.play(FadeIn(knight3), FadeIn(attacks3))
        self.play(FadeIn(knight4), FadeIn(attacks4))
        self.play(FadeIn(knight5), FadeIn(attacks5))
        self.play(FadeIn(knight6), FadeIn(attacks6))
        self.play(FadeIn(knight7), FadeIn(attacks7))
        self.play(FadeIn(knight8), FadeIn(attacks8))
        self.play(FadeIn(knight9), FadeIn(attacks9))
        self.play(FadeIn(knight10), FadeIn(attacks10))
        
    def eightProof(self, fields):
        self.play(DrawBorderThenFill(fields[5]))
        knight = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][13].get_center())
        knight2 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][17].get_center())
        knight3 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][18].get_center())
        knight4 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][20].get_center())
        knight5 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][21].get_center())
        knight6 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][26].get_center())
        knight7 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][37].get_center())
        knight8 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][42].get_center())
        knight9 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][43].get_center())
        knight10 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][45].get_center())
        knight11 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][46].get_center())
        knight12 = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][50].get_center())
        attacks1 = VGroup()
        attacks2 = VGroup()
        attacks3 = VGroup()
        attacks4 = VGroup()
        attacks5 = VGroup()
        attacks6 = VGroup()
        attacks7 = VGroup()
        attacks8 = VGroup()
        attacks9 = VGroup()
        attacks10 = VGroup()
        attacks11 = VGroup()
        attacks12 = VGroup()
        attacks1.add(self.getAttacks(13, 8, fields[5]))
        attacks2.add(self.getAttacks(17, 8, fields[5]))
        attacks3.add(self.getAttacks(18, 8, fields[5]))
        attacks4.add(self.getAttacks(20, 8, fields[5]))
        attacks5.add(self.getAttacks(21, 8, fields[5]))
        attacks6.add(self.getAttacks(26, 8, fields[5]))
        attacks7.add(self.getAttacks(37, 8, fields[5]))
        attacks8.add(self.getAttacks(42, 8, fields[5]))
        attacks9.add(self.getAttacks(43, 8, fields[5]))
        attacks10.add(self.getAttacks(45, 8, fields[5]))
        attacks11.add(self.getAttacks(46, 8, fields[5]))
        attacks12.add(self.getAttacks(50, 8, fields[5]))
        AGroup = VGroup()
        letters = ['A', 'A', None, None, None, None, 'A', 'A',
                   None, 'A', None, None, None, None, 'A', None,
                   None, None, None, None, None, None, None, None,
                   None, None, None, None, None, None, None, None,
                   None, None, None, None, None, None, None, None,
                   None, None, None, None, None, None, None, None, 
                   None, 'A', None, None, None, None, 'A', None,
                   'A', 'A', None, None, None, None, 'A', 'A']
        
        for index, letter in enumerate(letters):
            if letter == 'A':
                AGroup.add(Text(letter).set_color(YELLOW).move_to(fields[5][index].get_center()))
        self.play(FadeIn(AGroup))
        # Show no knight can cover any of these spots
        tempKnight = SVGMobject('WKnight.svg').scale(0.5).move_to(fields[5][0].get_center())
        tempKnight.generate_target()
        attacks = self.getAttacks(0, 8, fields[5])
        for i in range(64):
            if i:
                self.play(FadeOut(attacks))
                tempKnight.target.shift(1.5 * RIGHT)
                if i % 8 == 0:
                    tempKnight.target.shift(1.5 * DOWN)
                    tempKnight.target.shift(1.5 * 8 * LEFT)
            attacks = self.getAttacks(i, 8, fields[5])
            if letters[i] == "A":
                # emphasize A
                pass
            if letters[i] == 1:
                positions = self.getPostionOfAttack(i, 8, fields[5])
                for pos in positions:
                    if letters[pos] == "A":
                        # Emphasize A
                        pass

            self.play(MoveToTarget(tempKnight), FadeIn(attacks))

        self.play(FadeOut(tempKnight), FadeOut(attacks))

        # Final Board
        self.play(FadeIn(knight), FadeIn(attacks1))
        self.play(FadeIn(knight2), FadeIn(attacks2))
        self.play(FadeIn(knight3), FadeIn(attacks3))
        self.play(FadeIn(knight4), FadeIn(attacks4))
        self.play(FadeIn(knight5), FadeIn(attacks5))
        self.play(FadeIn(knight6), FadeIn(attacks6))
        self.play(FadeIn(knight7), FadeIn(attacks7))
        self.play(FadeIn(knight8), FadeIn(attacks8))
        self.play(FadeIn(knight9), FadeIn(attacks9))
        self.play(FadeIn(knight10), FadeIn(attacks10))
        self.play(FadeIn(knight11), FadeIn(attacks11))
        self.play(FadeIn(knight12), FadeIn(attacks12))