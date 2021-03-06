import json
import random
import re
import dataScrape


class queryingData:

    def loadJson(self, queryText):

        if (queryText.lower() == "admin update data"):
            try:
                dataScrape.getData()
                return("Data updated successfully Boss Rane")
            except Exception as ex:
                return(ex)

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
* FRESH - display fresh cases.
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

        elif re.search(r'^(ph)\d+', queryText.lower()):  # for PH###
            FV = "For validation"
            with open('masterList.json') as file:
                self.data = json.load(file)

            for case in self.data['data']:
                if (str(case['case_no'][2:]).lstrip("0") == queryText[2:].lstrip("0")):
                    if (case['sex'] == FV and case['age'] == FV and case['residence_in_the_ph'] == FV and case['hospital_admitted_to'] == FV and case['date_of_announcement_to_public'] == FV):
                        return ("{}'s details are not yet available".format(queryText.upper()))
                    else:
                        return ("{}, {}, {}, {} nationality from {}, admitted at {}, announced to public on {}, and now with a status of {}".format(queryText.upper(), case['sex'], case['age'], case['nationality'], case['residence_in_the_ph'], case['hospital_admitted_to'], case['date_of_announcement_to_public'], case['health_status']))

        elif re.search(r'^(fresh)', queryText.lower()):  # for cases fresh
            with open('statistics.json') as file:
                self.data = json.load(file)

            return("There are {} new cases, {} new deaths, and {} new recoveries in the Philippines as of {}".format(self.data['data']['cases_today'], self.data['data']['deaths_today'], self.data['data']['recoveries_today'], self.data['data']['last_update']))

        elif re.search(r'^(pui)', queryText.lower()):  # for PUIs
            return("Sorry the public API offered by DOH before was unavailable. Thus, the chatbot can't offer information on the number of PUIs.")

        elif re.search(r'^(pum)', queryText.lower()):  # for PUMs
            return("Sorry the public API offered by DOH before was unavailable. Thus, the chatbot can't offer information on the number of PUMs.")

        elif re.search(r'^(confirmed)|^(confirm)|^(current)', queryText.lower()):  # for confirmed cases
            with open('statistics.json') as file:
                self.data = json.load(file)

            return("There are {} confirmed cases in the Philippines as of {}".format(self.data['data']['cases'], self.data['data']['last_update']))

        elif re.search(r'^(test)|^(tested)|^(tests)', queryText.lower()):  # for tests
            return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")

        elif re.search(r'^(rate)|^(rates)|^(current)', queryText.lower()):  # for fatality rate
            with open('statistics.json') as file:
                self.data = json.load(file)

            return("The recovery rate is {} and the fatality rate is {} as of {}".format(self.data['data']['recovery_rate'], self.data['data']['fatality_rate'], self.data['data']['last_update']))

        elif re.search(r'^(recovered)|^(recovery)|^(recover)', queryText.lower()):  # for recovered
            with open('statistics.json') as file:
                self.data = json.load(file)

            return("There are currently {} recovered in the Philippines as of {}".format(self.data['data']['recoveries'], self.data['data']['last_update']))

        elif re.search(r'^(death)|^(dead)|^(die)|^(deaths)', queryText.lower()):  # for deaths
            with open('statistics.json') as file:
                self.data = json.load(file)

            return("There are currently {} death cases in the Philippines as of ".format(self.data['data']['deaths'], self.data['data']['last_update']))

        else:  # for facility or region
            self.response = ""
            with open('facilityStats.json') as file:
                self.data = json.load(file)

            with open('locationStats.json') as file:
                self.data2 = json.load(file)

            queryText = queryText.lower()
            regex = r'' + queryText + r''

            for key, value in self.data2.items():

                if re.search(regex, key.lower()):
                    if (value == 1):
                        self.response = self.response + \
                            ("-{} has {} confirmed case of CoViD-19\n".format(key, value))
                    else:
                        self.response = self.response + \
                            ("-{} has {} confirmed cases of CoViD-19\n".format(key, value))

            for features in self.data['data']:
                facilityInitials = ""
                facilityInit = features['facility'].replace(
                    "and", " ").replace(
                        "for", " ").replace(
                            "-", " ").replace(
                                "of", " ").replace(
                                    "in", " ").replace(
                                        "the", " ").split()
                for word in facilityInit:
                    facilityInitials = facilityInitials + word[0]
                facilityInitials = ("".join(facilityInitials).lower())

                if re.search(regex, features['facility']) or re.search(r'^' + queryText, facilityInitials):

                    if (features['confirmed_cases'] <= 1 and features['puis'] <= 1):
                        self.response = self.response + ("-{} has {} confirmed case and {} PUI.\n".format(
                            features['facility'], features['confirmed_cases'], features['puis']))
                    elif (features['confirmed_cases'] <= 1 and features['puis'] > 1):
                        self.response = self.response + ("-{} has {} confirmed case and {} PUIs.\n".format(
                            features['facility'], features['confirmed_cases'], features['puis']))
                    elif (features['puis'] <= 1 and features['confirmed_cases'] > 1):
                        self.response = self.response + ("-{} has {} confirmed cases and {} PUI.\n".format(
                            features['facility'], features['confirmed_cases'], features['puis']))
                    else:
                        self.response = self.response + ("-{} has {} confirmed cases and {} PUIs.\n".format(
                            features['facility'], features['confirmed_cases'], features['puis']))

            if (self.response == ""):
                unknown = ["Sorry, I dont understand.",
                           "I can't comprehend", "Sorry, please check your keywords"]
                return (random.choice(unknown))
                # return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")

            else:
                return(self.response)
                # return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")


# testing purposes
# if __name__ == '__main__':
#     q = queryingData()
#     print(q.loadJson("confirmed"))
