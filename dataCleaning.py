import json
import random
import re
import dataScrape
import datetime from datetime
import pandas as pd


class queryingData:

    def __init__(self):
        self.loadStats()

    def loadStats(self):
        with open('statistics.json') as file:
            self.data = json.load(file)

        self.dateUpdated = pd.to_datetime(self.data["updated"], unit="ms")[:10]
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
        self.recoveryRate = self.recovered/self.cases
        self.deathRate = self.deaths/self.cases
    
    def updateData(self):
        try:
            dataScrape.getData()
            self.loadStats()
            return("Data updated successfully Boss Rane")
        except Exception as ex:
            return(ex)


    def loadJson(self, queryText):

        if (queryText.lower() == "admin update data"):
            self.updateData()

        elif (queryText.lower() == "info"):
            self.info = """Hi this chatbot is created to track statistics of the CoViD-19 pandemic in the Philippines.
Data is from https://coronavirus-ph-api.herokuapp.com/. However, it may not be up to date with the newest cases that is not yet updated on the APIs.
* INFO - to display information regarding this chatbot.
* PH# - to display the details of the person (ex: PH661).
* Location - to display cases in a location (ex: Cagayan).
* HOSPITAL - to display current cases  hospital (ex: CAGAYAN VALLEY MEDICAL CENTER or CVMC).
* CONFIRMED - to display total confirmed cases.
* DEATHS - to display total deaths.
* RECOVERED - to display total recoveries.
* RATES - display recovery and fatality rate.
* TODAY - display new cases for the day.
"""

            return (self.info)

        elif re.search(r'^(hi)|^(hello)', queryText.lower()):
            self.response = ["Hi there.", "Hello there", "Good day"]
            return (random.choice(self.response))

        elif re.search(r'^(bye)|^(goodbye)', queryText.lower()):
            self.response = ["Bye. Keep Safe and always wash your hands!", "Goodbye! Always keep safe!",
                             "Keep Safe! Keep clean!", "Bye! Stay indoors! Together we fight!"]
            return (random.choice(self.response))

        elif re.search(r'^(thanks)|^(thank)', queryText.lower()):
            self.response = ["No problem. Let's flatten the curve",
                             "You're welcome. Help flatten the curve!", "You're welcome! Stay indoors!"]
            return (random.choice(self.response))

        elif re.search(r'^(today)', queryText.lower()):  # for cases today
            return("There are {} new cases, {} new deaths, and {} new recoveries in the Philippines as of {}".format(self.cases, self.deaths, self.recovered, self.dateUpdated))

        elif re.search(r'^(confirmed)|^(confirm)|^(current)|^(case)|^(cases)', queryText.lower()):  # for confirmed cases
            return("There are {} confirmed cases in the Philippines as of {}".format(self.cases, self.dateUpdated))

        elif re.search(r'^(active)', queryText.lower()):  # for active cases
            return("There are {} active cases in the Philippines as of {}".format(self.active, self.dateUpdated))

        elif re.search(r'^(test)|^(tested)|^(tests)', queryText.lower()):  # for tests
            return("There are {} tests in the Philippines as of {}".format(self.active, self.dateUpdated))

        elif re.search(r'^(rate)|^(rates)', queryText.lower()):  # for fatality rate
            return("The recovery rate is {} and the fatality rate is {} as of {}".format(self.recoveryRate, self.deathRate, self.dateUpdated))

        elif re.search(r'^(recovered)|^(recovery)|^(recover)', queryText.lower()):  # for recovered
            return("There are currently {} recovered in the Philippines as of {}".format(self.recovered, self.dateUpdated))

        elif re.search(r'^(death)|^(dead)|^(die)|^(deaths)', queryText.lower()):  # for deaths
            return("There are currently {} death cases in the Philippines as of ".format(self.deaths, self.dateUpdated))

        else:  # for facility or region
            unknown = ["Sorry, I dont understand.",
                        "I can't comprehend", "Sorry, please check your keywords"]
            return (random.choice(unknown))
                # return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")
                # return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")


# testing purposes
if __name__ == '__main__':
    q = queryingData()
    print(q.loadJson("confirmed"))