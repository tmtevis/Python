
# LIVE BETTING TEST CASE #
test1 = '(Sports (Live))		[WON] - LIVE BETTING BET (Internet)'
test2 = '[227.3/250.0] BASKETBALL•LLANEROS..@GIGANTES..•1ST QUARTER TEAM TOTALS•GIGANTES DE GUAYANA • UNDE...	227/250	250'
test1_split = test1.rsplit()
test2_split = test2.rsplit()
                                        #   Junk Line Syntax
# print(test1_split)                    #   ['(Sports', '(Live))', '[WON]', '-', 'LIVE', 'BETTING', 'BET', '(Internet)']
# print(len(test1_split))               #   length of 8


                                        #   Live Betting Syntax
# print(test2_split)                      #   ['[227.3/250.0]', 'BASKETBALL•LLANEROS..@GIGANTES..•1ST', 'QUARTER', 'TEAM', 'TOTALS•GIGANTES', 'DE', 'GUAYANA', '•', 'UNDE...', '227/250', '250']
# print(len(test2_split))                 #   11 items
# print(test2_split[1][0].isalpha())      #   True
# print(test2_split[1])
# print(test2_split[9])                 #   Wager:  227/250
# print(test2_split[10])                #   Win:    250

# test3 = '[11/11/2020 07:04 PM] - [CFB] - [118] BALL STATE -9-110 [Lost] (Score: 38-31)'
# test3_split = test3.rsplit()
# print(test3_split)                        # ['[11/11/2020', '07:04', 'PM]', '-', '[CFB]', '-', '[118]', 'BALL', 'STATE', '-9-110', '[Lost]', '(Score:', '38-31)']
# print(len(test3_split))                   # 13
# print(test3_split[1][0].isdigit())        # True
                                            # valid bet - count it

# test4 = '[11/10/2020 05:51 PM] -[OPEN PLAY]'    # Extra line - delete
# test4_split = test4.rsplit()
# print(test4_split[4])
# print(len(test4_split))                         # Catch with this - len = 5

test5 = 'TST15903 / WIZARDS903	11/15/2020 8:58:04 PM	#304481637'
test5_split = test5.rsplit()
print(test5_split)
print(len(test5_split))                         # Catch with this - len = 5
        
# print(to_write)
# print(test2[0][0].isnumeric())
# # print(test2.index('[11/15/2020'))
# # print('[11/15/2020')

# LIVE BETTING STYLE:
# TST15903 / WIZARDS903	11/15/2020 8:58:04 PM	#304481637
# (Sports (Live))		[WON] - LIVE BETTING BET (Internet)
# [25.0/300.0] AMERICAN FOOTBALL•BAL..@NE..•2ND TOUCHDOWN SCORER•REX BURKHEAD•+1200	25/300	300

# (Casino)		[WON] - CASINO GAME (Internet)
# (Sports)		[PENDING] - PARLAY 3 TEAM (Internet - IP: 2607:fb90:a63:764e:b0e7:ac9f:a188:d71e)
# FC BJ Mobile	0	5

