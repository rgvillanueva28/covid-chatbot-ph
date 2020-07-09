import json
import random
import re
import dataScrape
import pandas as pd


class queryingData:

    def __init__(self):
        self.loadStats()

    def loadStats(self):
        with open('statistics.json') as file:
            self.data = json.load(file)

        self.dateUpdated = pd.to_datetime(self.data["updated"], unit="ms").strftime("%B %d, %Y")
        self.cases = self.data["cases"]
        self.todayCases = self.data["todayCases"]
        self.deaths = self.data["deaths"]
        self.todayDeaths = self.data["todayDeaths"]
        self.recovered = self.data["recovered"]
        self.todayRecovered = self.data["todayRecovered"]
        self.active = self.data["active"]
        self.critical = self.data["critical"]
        self.tests = self.data["tests"]
        self.testsPerMil = self.data["testsPerOneMillion"]
        self.casesPerMil = self.data["casesPerOneMillion"]
        self.deathsPerMil = self.data["deathsPerOneMillion"]
        self.recoveredPerMil = self.data["recoveredPerOneMillion"]
        self.criticalPerMil = self.data["criticalPerOneMillion"]
        self.recoveryRate = self.recovered/self.cases*100
        self.deathRate = self.deaths/self.cases*100
    
    def updateData(self):
        try:
            dataScrape.getData()
            self.loadStats()
            return("Data updated successfully Boss Rane")
        except Exception as ex:
            return(ex)


    def loadJson(self, queryText):

        if (queryText.lower() == "admin update data"):
            return self.updateData()

        elif (queryText.lower() == "info"):
            self.info = """Hi this chatbot is created to track statistics of the CoViD-19 pandemic in the Philippines.
Data is from https://disease.sh. However, it may not be up to date with the newest cases that is not yet updated on the APIs.
* INFO - to display information and list of commands.
* CASES - to display total cases.
* ACTIVE - to display current active cases
* DEATHS - to display total deaths.
* RECOVERED - to display total recoveries.
* CRITICAL - to display critical cases.
* TESTS - to display number of tests conducted.
* RATES - display recovery and fatality rate.
* TODAY - display new cases for the day.
* TOTAL - display the total cases including active, deaths, and recoveries.
* PER MILLION - to display statistics per one million.
"""

            return (self.info)

        elif re.search(r'^(hi)|^(hello)', queryText.lower()):
            self.response = ["Hi there!", "Hello there!", "Good day!"]
            return (random.choice(self.response))

        elif re.search(r'^(bye)|^(goodbye)', queryText.lower()):
            self.response = ["Bye. Keep Safe and always wash your hands!", "Goodbye! Always keep safe!",
                             "Keep Safe! Keep clean!", "Bye! Stay indoors! Together we fight!"]
            return (random.choice(self.response))

        elif re.search(r'^(thanks)|^(thank)', queryText.lower()):
            self.response = ["No problem! Let's flatten the curve!",
                             "You're welcome. Help flatten the curve!", "You're welcome! Stay indoors!"]
            return (random.choice(self.response))

        elif re.search(r'^(total)', queryText.lower()):  # for total cases
            return("There are {} total cases,\n{} active,\n{} deaths, and\n{} recoveries in the Philippines as of {}.".format(self.cases, self.active, self.deaths, self.recovered, self.dateUpdated))

        elif re.search(r'^(today)', queryText.lower()):  # for cases today
            return("There are {} new cases,\n{} new deaths, and\n{} new recoveries in the Philippines today, {}.".format(self.todayCases, self.todayDeaths, self.todayRecovered, self.dateUpdated))

        elif re.search(r'^(confirmed)|^(confirm)|^(current)|^(case)|^(cases)', queryText.lower()):  # for confirmed cases
            return("There are {} confirmed cases in the Philippines as of {}.".format(self.cases, self.dateUpdated))

        elif re.search(r'^(active)', queryText.lower()):  # for active cases
            return("There are {} active cases in the Philippines as of {}.".format(self.active, self.dateUpdated))

        elif re.search(r'^(test)|^(tested)|^(tests)', queryText.lower()):  # for tests
            return("There are {} tests in the Philippines as of {}".format(self.active, self.dateUpdated))

        elif re.search(r'^(rate)|^(rates)', queryText.lower()):  # for fatality rate
            return("The recovery rate is {:.2f} and the fatality rate is {:.2f} as of {}.".format(self.recoveryRate, self.deathRate, self.dateUpdated))

        elif re.search(r'^(recovered)|^(recovery)|^(recover)', queryText.lower()):  # for recovered
            return("There are currently {} recovered in the Philippines as of {}.".format(self.recovered, self.dateUpdated))

        elif re.search(r'^(death)|^(dead)|^(die)|^(deaths)', queryText.lower()):  # for deaths
            return("There are currently {} death cases in the Philippines as of {}.".format(self.deaths, self.dateUpdated))
        
        elif re.search(r'^(critical)', queryText.lower()):  # for deaths
            return("There are currently {} critical cases in the Philippines as of {}.".format(self.critical, self.dateUpdated))
        
        elif re.search(r'^(per million)', queryText.lower()):  # for deaths
            return("There are\n{} cases per million\n{} deaths per million\n{} recoveries per million\n{} tests per million\nin the Philippines as of {}.".format(self.casesPerMil, self.deathsPerMil, self.recoveredPerMil, self.testsPerMil, self.dateUpdated))

    #    self.testsPerMil = self.data["testsPerOneMillion"]
    #     self.casesPerMil = self.data["casesPerOneMillion"]
    #     self.deathsPerMil = self.data["deathsPerOneMillion"]
    #     self.recoveredPerMil = self.data["recoveredPerOneMillion"]
    #     self.criticalPerMil = self.data["criticalPerOneMillion"]

        else:  # for facility or region
            unknown = ["Sorry, I dont understand.",
                        "I can't comprehend.", "Sorry, please check your keywords."]
            return (random.choice(unknown))
                # return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")
                # return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")


# testing purposes
# if __name__ == '__main__':
#     q = queryingData()
#     print(q.loadJson("total"))