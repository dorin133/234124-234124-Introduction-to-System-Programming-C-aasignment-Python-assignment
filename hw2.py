def printCompetitor(competitor):
    '''
    Given the data of a competitor, the function prints it in a specific format.
    Arguments:
        competitor: {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition_name = competitor['competition name']
    competition_type = competitor['competition type']
    competitor_id = competitor['competitor id']
    competitor_country = competitor['competitor country']
    result = competitor['result']
    
    print(f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}')


def printCompetitionResults(competition_name, winning_gold_country, winning_silver_country, winning_bronze_country):
    '''
    Given a competition name and its champs countries, the function prints the winning countries 
        in that competition in a specific format.
    Arguments:
        competition_name: the competition name
        winning_gold_country, winning_silver_country, winning_bronze_country: the champs countries
    '''
    undef_country = 'undef_country'
    countries = [country for country in [winning_gold_country, winning_silver_country, winning_bronze_country] if country != undef_country]
    print(f'The winning competitors in {competition_name} are from: {countries}')


def key_sort_competitor(competitor):
    '''
    A helper function that creates a special key for sorting competitors.
    Arguments:
        competitor: a dictionary contains the data of a competitor in the following format: 
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition_name = competitor['competition name']
    result = competitor['result']
    return (competition_name, result)


'''
    Given a file name, the function returns a list of competitors.
    Arguments: 
        file_name: the input file name. Assume that the input file is in the directory of this script.
    Return value:
        A list of competitors, such that every record is a dictionary, in the following format:
            {'competition name': competition_name, 'competition type': competition_type,
                'competitor id': competitor_id, 'competitor country': competitor_country, 
                'result': result}
'''
def readParseData(file_name):
    with open(file_name,"r") as f:
        lines = f.read().splitlines()
    splited_list = []
    for element in lines:
        splited_list.append(element.split(' '))
    competition_list = []
    competitor_dict = {}
    for element in splited_list:
        if(element[0]=="competition"):
            new_competition_dict={}
            new_competition_dict["competition name"]= element[1]
            new_competition_dict["competitor id"]= (int)(element[2])
            new_competition_dict["competition type"]= element[3]
            new_competition_dict["result"]= (int)(element[4])
            competition_list.append(new_competition_dict)
        else:
            competitor_dict[(int)(element[1])] = element[2]
    for competitor_id in competitor_dict.keys():
        for element in competition_list:       
            if(competitor_id == element["competitor id"]):
                element["competitor country"] = competitor_dict[competitor_id]
    return competition_list

def getCompetitorResult(competitor):
    '''
    A helper function that returns the result of a competitor.
    Arguments:
        competitor: a dictionary that contains the data of a competitor in the following forma: 
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    return competitor["result"]

def calcWinner(competition):
    '''
    A helper function that creates the winners in a single competition.
    Arguments:
        competition: a list of dictionarys that contains the data of a competition in the following format: 
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition=sorted(competition,key=getCompetitorResult,reverse=competition[0]["competition type"]=="untimed")
    winners=[competition[0]["competition name"],"undef_country","undef_country","undef_country"]
    for i in range(min(len(winners)-1,len(competition))):
        winners[i+1]=competition[i]["competitor country"]
    return winners


def appearsOnlyOnce(competition,competitor_id,competition_name):
    '''
    A helper function that checks if a competitor enrolled more then once to a single competition.
    Arguments:
        competition: a dictionary contains the data of a competitor in the following format: 
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
        competitor_id: the id of the competitor
        competition_name: the name of the competition       
    '''
    counter=0
    for element in competition:
        if(element["competitor id"]==competitor_id and element["competition name"]==competition_name):
            counter+=1
            if(counter>1):
                return False
    return True
    
def calcCompetitionsResults(competitors_in_competitions):
    '''
    Given the data of the competitors, the function returns the champs countries for each competition.
    Arguments:
        competitors_in_competitions: A list that contains the data of the competitors
                                    (see readParseData return value for more info)
    Retuen value:
        A list of competitions and their champs (list of lists). 
        Every record in the list contains the competition name and the champs, in the following format:
        [competition_name, winning_gold_country, winning_silver_country, winning_bronze_country]
    '''
    competitions_champs = []
    olympics=[elem for elem in competitors_in_competitions if appearsOnlyOnce(competitors_in_competitions,elem["competitor id"],elem["competition name"])]
    while len(olympics)>0:
        current_competition=[elem for elem in olympics if elem["competition name"]==olympics[0]["competition name"]]
        competitions_champs.append(calcWinner(current_competition))
        olympics=[elem for elem in olympics if elem["competition name"]!=olympics[0]["competition name"]]
    return competitions_champs


def partA(file_name = 'input.txt', allow_prints = True):
    # read and parse the input file
    competitors_in_competitions = readParseData(file_name)
    if allow_prints:
        for competitor in sorted(competitors_in_competitions, key=key_sort_competitor):
            printCompetitor(competitor)
    
    # calculate competition results
    competitions_results = calcCompetitionsResults(competitors_in_competitions)
    if allow_prints:
        for competition_result_single in sorted(competitions_results):
            printCompetitionResults(*competition_result_single)
    
    return competitions_results


def partB(file_name = 'input.txt'):
    import Olympics
    competitions_results = partA(file_name, allow_prints = False)
    olympics=Olympics.OlympicsCreate()
    for winners in competitions_results:
        Olympics.OlympicsUpdateCompetitionResults(olympics, str(winners[1]), str(winners[2]), str(winners[3]))
    Olympics.OlympicsWinningCountry(olympics)
    Olympics.OlympicsDestroy(olympics)


if __name__ == "__main__":
    '''
    The main part of the script.
    __main__ is the name of the scope in which top-level code executes.
    
    To run only a single part, comment the line below which correspondes to the part you don't want to run.
    '''    
    file_name='input.txt'
    partA(file_name)
    partB(file_name)



