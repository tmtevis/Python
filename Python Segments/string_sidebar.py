from datetime import date
today = date.today()
# next_line_parsed = ['(Sports)', '[PENDING]', '-', 'PARLAY', '3', 'TEAM', '(Internet', '-', 'IP:', '2607:fb90:a63:764e:b0e7:ac9f:a188:d71e)']
# next_line_parsed =['500/3000', '0']
next_line_parsed = ['[11/16/2020', '04:06', 'PM]', '-', '[NFL]', '-', '[1268]', 'TOTAL', 'U27Â½-110', '(1H', 'BUF', 'BILLS', 'VRS', '1H', 'ARI', 'CARDINALS)', '[Pending]', '(Score:', '0-0)']

today_search = today.strftime('[%m/%d/%Y')
print(today_search)
if(next_line_parsed[0] == today_search):
    print('found')

# if(next_line_parsed.index(0) == 'FC' or '(Sports' or '(Casino)' or '(Sports)' or 'Roulette'):
#     print('Line Skipped: FC, Sports or Casino: ', next_line_parsed.index(0), '\n')

    
if(next_line_parsed[4] == ('PLAY]')):
    print('Line Skipped: FREE PLAY\n')                        
# Live Betting
# ['[227.3/250.0]', 'BASKETBALL•LLANEROS..@GIGANTES..•1ST', 'QUARTER', 'TEAM', 'TOTALS•GIGANTES', 'DE', 'GUAYANA', '•', 'UNDE...', '227/250', '250']
if(next_line_parsed[1][0].isalpha() and (len(next_line_parsed) == 11)):
# 'BASKETBALL•LLANEROS..@GIGANTES..•1ST - 227/250'
    toWrite = next_line_parsed[1] + ' - ' + next_line_parsed[9]

    print('Live Bet Counted')


# ['[11/11/2020', '07:04', 'PM]', '-', '[CFB]', '-', '[118]', 'BALL', 'STATE', '-9-110', '[Lost]', '(Score:', '38-31)']
if(next_line_parsed[1][0].isdigit() and (len(next_line_parsed) == 13)):
    print('Bet Counted')

    
if(len(next_line_parsed) == 2):
    # wager = str(bet_line_parsed[0]) + '\n'
    print('Wager at End')
