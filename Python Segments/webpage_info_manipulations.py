from datetime import date

def get_num_lines(fName):
    f = open(fName, 'r+')
    count = 0
    for line in f:
        count = count + 1
    f.close()
    return count
def format_file(fName):
    fRead = open(fName, 'r')
    fWrite = open('temp.txt', 'w+')
    while True:
        line = fRead.readline()
        if line == 'NAS9\n':
            continue
        if line == '':
            break
        else:
            fWrite.write(line)
    fRead.close()
    fWrite.close()
    fTemp = open('temp.txt', 'r')
    fOverwrite = open(fName, 'w+')
    while True:
        line = fTemp.readline()
        fOverwrite.write(line)
        if line == '':
            break
    fTemp.close()
    fWrite.close()
    fTempClear = open('temp.txt', 'w+')
    fTempClear.close()
# strips out everything but transaction data. specifics to be fetched later.
def distill_data(fName, fDistilled):
    fRead = open(fName, 'r')
    distilled = open(fDistilled, 'w+')
    for x in range(get_num_lines(fName)):
        line = fRead.readline()  # read line from login_attempt.txt
        parsed_line = line.rsplit()       # ['TST15903', '/', 'WIZARDS903', '11/15/2020', '4:03:16', 'PM', '#304368525']
        if(parsed_line[0].__contains__('TST')):
            user = parsed_line[0]
            transaction = parsed_line[6]
            transaction_info = user + ' ' + transaction + '\n'
            distilled.write(transaction_info)                   #   Writes each line as: TST15903 #304368525
        else:
            continue

def get_new_bets():
    # first half of function generates distilled report of new bets to new_bets_distilled.txt
    # second half of function searches login_attempt.txt for those new transactions and generates report with specifics
    login_lines = get_num_lines('login_attempt.txt')
    login_lines_distilled = get_num_lines('login_attempt_distilled.txt')
    record_lines_distilled = get_num_lines('webpage_status_distilled.txt')
    fNBDistilled = open('new_bets_distilled.txt', 'w+')         # file to dump distilled version of new transactions
    fLoginDistilled = open('login_attempt_distilled.txt', 'r')
    match = 0           # use this as flag for when a transaction is found
    for x in range(login_lines_distilled):
        lineAttempt = fLoginDistilled.readline()       # read first transaction of login_attempt_distilled.txt
        fRecord = open('webpage_status_distilled.txt', 'r')    # open record to start at beginning
        for y in range(record_lines_distilled):                           # iterate through every line of webpage_status_distilled.txt
            lineRecord = fRecord.readline()
            if(str(lineAttempt) == str(lineRecord)):            # if line in record matches line in login_attempt, it is an old transaction
                match = 1                                       # match flag is set
                continue
        if(match == 0):                                         # transaction is new - write to distilled new_bets text file
            fNBDistilled.write(lineAttempt)
        else:
            match = 0                                           # reset match flag, close record file for next open/compare
            fRecord.close()

    fNBDistilled.close()
    fLoginDistilled.close()
    fRecord.close()                                             # new transactions forked into distilled text file - complete
                                                                # parse full version of login_attempt.txt to get exact wager data
    num_new_transactions = get_num_lines('new_bets_distilled.txt')
    fNewDistilled = open('new_bets_distilled.txt', 'r')         # re-open distilled version of new transactions
    fNewBets = open('new_bets.txt', 'w+')

    for z in range(num_new_transactions):                       # iterate through new_bets_distilled.txt
        distilled_transaction = fNewDistilled.readline()        # get line
        dt_parsed = distilled_transaction.rsplit()              # split into ['TST15903', '#304368525']
        fLogin = open('login_attempt.txt', 'r')
        for zz in range(login_lines):                           # begin search for transaction in login_attempt.txt
            login_line = fLogin.readline()                      
            ll_parsed = login_line.rsplit()                     # splits line. all possibilities below:
                                                                # ['TST15903', '/', 'WIZARDS903', '11/15/2020', '4:03:16', 'PM', '#304368525']
                                                                # ['(Sports)', '[PENDING]', '-', 'PARLAY', '3', 'TEAM', '(Internet', '-', 'IP:', '2607:fb90:a63:764e:b0e7:ac9f:a188:d71e)']
                                                                # ['[11/15/2020', '04:30', 'PM]', '-', '[NFL]', '-', '[1270]', 'TOTAL', 'U27-105', '(1H', 'SEA', 'SEAHAWKS', 'VRS', '1H', 'LA', 'RAMS)', '[Pending]']

            if(dt_parsed[0] == ll_parsed[0]):                   # comparing for username. ex: 'TST15903' with 'TST15903', '(Sports)' or '[11/15/2020'
                if(dt_parsed[1] == ll_parsed[6]):               # if username is matched, compare for transaction ID. ex: #304368525'
                    fNewBets.write(login_line)                  # writes: 'TST15903 / WIZARDS903	11/15/2020 4:03:16 PM	#304368525'
                    while True:
                        valid = 1
                        bet_line = fLogin.readline()            # Possible Formats:
                                                                # (Casino)		[WON] - CASINO GAME (Internet)
                                                                # (Sports)		[PENDING] - PARLAY 3 TEAM (Internet - IP: 2607:fb90:a63:764e:b0e7:ac9f:a188:d71e)
                                                                # FC BJ Mobile	0	5
                                                                # Roulette American H5 (Mobile)	0	-218

                                                                # [11/15/2020 04:30 PM] - [NFL] - [1252] 1H PIT STEELERS -233 [Pending]
                                                                # [11/15/2020 04:30 PM] - [NFL] - [1270] TOTAL U27-105 (1H SEA SEAHAWKS VRS 1H LA RAMS) [Pending]
                                                                # [11/10/2020 05:51 PM] -[OPEN PLAY]
                                                                
                                                                # 500/3000	0

                                                                # LIVE BETTING STYLE:
                                                                # TST15903 / WIZARDS903	11/15/2020 8:58:04 PM	#304481637
                                                                # (Sports (Live))		[WON] - LIVE BETTING BET (Internet)
                                                                # [25.0/300.0] AMERICAN FOOTBALL•BAL..@NE..•2ND TOUCHDOWN SCORER•REX BURKHEAD•+1200	25/300	300


                        bet_line_parsed = bet_line.rsplit()
                        print(bet_line_parsed[0])
                        if(bet_line_parsed[0] == '(Sports' or '(Casino'):   # discard '(Sports)' line
                            print('sports found')
                            valid = 0
                            continue
                        if(bet_line_parsed[0][0].isnumeric()):      # meant to catch wager: ['450/1897',	'0'] --> 4 is numeric
                            wager = str(bet_line_parsed[0]) + '\n'  # adjust to add new-line char before writing
                            fNewBets.write(wager)
                            False                                   # break loop to look for next transaction
                        if(valid = 1):
                            fNewBets.write(bet_line)
    fLogin.close()
    fRecord.close()
    fNewDistilled.close()
    fNewBets.close()




# distill_data('login_attempt.txt', 'login_attempt_distilled.txt')
# distill_data('webpage_status.txt', 'webpage_status_distilled.txt')
get_new_bets()




## FILE STRUCTURE:
#
# TST15903 / WIZARDS903	11/15/2020 4:03:16 PM	#304368525
# (Sports)		[PENDING] - PARLAY 3 TEAM (Internet - IP: 2607:fb90:a63:764e:b0e7:ac9f:a188:d71e)
# [11/15/2020 04:30 PM] - [NFL] - [1252] 1H PIT STEELERS -233 [Pending]
# [11/15/2020 04:30 PM] - [NFL] - [1270] TOTAL U27-105 (1H SEA SEAHAWKS VRS 1H LA RAMS) [Pending]
# [11/15/2020 04:30 PM] - [NFL] - [1271] TOTAL O24-115 (1H SFO 49ERS VRS 1H NO SAINTS) [Pending]
# 450/1897	0
# TST15903 / WIZARDS903	11/15/2020 4:02:36 PM	#304367081
# (Sports)		[PENDING] - PARLAY 3 TEAM (Internet - IP: 2607:fb90:a63:764e:b0e7:ac9f:a188:d71e)
# [11/15/2020 04:06 PM] - [NFL] - [1268] TOTAL U27½-110 (1H BUF BILLS VRS 1H ARI CARDINALS) [Pending] (Score: 0-0)
# [11/15/2020 04:30 PM] - [NFL] - [1270] TOTAL U27-105 (1H SEA SEAHAWKS VRS 1H LA RAMS) [Pending]
# [11/15/2020 04:30 PM] - [NFL] - [1272] 1H NO SAINTS -6-110 [Pending]
# 500/3000	0