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
            self.info = "Hi this chatbot is created to track statistics of the CoViD-19 pandemic in the Philippines.\n" \
                "Data is from the public API of DOH. However, it may not be up to date with the newest cases that is not yet updated on the DOH's server.\n" \
                    "\nThe chatbot currently supports the following keywords:\n" \
                        "*INFO - to display information regarding this chatbot\n" \
                            "*PH# - to display the details of the person (ex: PH661)\n"\
                            "*PLACE\HOSPITAL - to display current cases in a place or hospital (ex: CAGAYAN or CAGAYAN VALLEY MEDICAL CENTER or CVMC)\n"\
                            "*PUI\n"\
                                "*PUM\n"\
                                    "*CONFIRMED\n"\
                                        "*DEATHS\n"\
                                            "*RECOVERED\n"\
                                                "*TESTS\n"\
                                                    "You can also try to greet, say thanks, and bid goodbye.\n\n"\
                                                        "-Rane 2020"
                                                    

            return (self.info)

        elif re.search(r'^(hi)|^(hello)', queryText.lower()):
            self.response = ["Hi there.", "Hello there", "Good day"]
            return (random.choice(self.response))
        
        elif re.search(r'^(bye)|^(goodbye)', queryText.lower()):
            self.response = ["Bye. Keep Safe and always wash your hands!", "Goodbye! Always keep safe!", "Keep Safe! Keep clean!", "Bye! Stay indoors! Together we fight!"]
            return (random.choice(self.response))

        elif re.search(r'^(thanks)|^(thank)', queryText.lower()):
            self.response = ["No problem. Let's flatten the curve", "You're welcome. Help flatten the curve!", "You're welcome! Stay indoors!"]
            return (random.choice(self.response))

        elif re.search(r'^(pui)', queryText.lower()):#for PUIs
            with open('statistics.json') as file:
                self.data = json.load(file)

            for features in self.data['features']:
                for key, value in features.items():
                    #return("There are currently {} PUIs in the Philippines".format(value['PUIs']))
                    return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")
        
        elif re.search(r'^(pum)', queryText.lower()):#for PUMs
            with open('statistics.json') as file:
                self.data = json.load(file)

            for features in self.data['features']:
                for key, value in features.items():
                    #return("There are currently {} PUMs in the Philippines".format(value['PUMs']))
                    return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")

        elif re.search(r'^(confirmed)|^(confirm)|^(current)', queryText.lower()):#for confirmed cases
            with open('statistics.json') as file:
                self.data = json.load(file)

            for features in self.data['features']:
                for key, value in features.items():
                    return("There are currently {} confirmed cases in the Philippines".format(value['confirmed']))

        elif re.search(r'^ph\d+', queryText.lower()): #for PH###
            with open('masterList.json') as file:
                self.data = json.load(file)

            for features in self.data['features']:
                for key, value in features.items():
                    if (value['PH_masterl'] == queryText.upper()):
                        return ("{}, {}, {}, resident of {} and admitted at {}".format(value['PH_masterl'], value['kasarian'], value['edad'], value['residence'], value['facility']))
            return("{}'s details are not yet available.".format(queryText.lower()))

        if re.search(r'^(recovered)|^(recovery)|^(recover)', queryText.lower()):#for recovered
            with open('statistics.json') as file:
                self.data = json.load(file)

            for features in self.data['features']:
                for key, value in features.items():
                    return("There are currently {} recovered in the Philippines".format(value['recovered']))

        if re.search(r'^(death)|^(dead)|^(die)|^(deaths)', queryText.lower()):#for deaths
            with open('statistics.json') as file:
                self.data = json.load(file)

            for features in self.data['features']:
                for key, value in features.items():
                    return("There are currently {} deaths in the Philippines".format(value['deaths']))

        if re.search(r'^(test)|^(tested)|^(tests)', queryText.lower()):#for tests
            with open('statistics.json') as file:
                self.data = json.load(file)

            for features in self.data['features']:
                for key, value in features.items():
                    #return("There are currently {} tests conducted in the Philippines".format(value['tests']))
                    return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")


        else: #for facility or place
            self.response = ""
            with open('facilityStats.json') as file:
                self.data = json.load(file)
            
            with open('locationStats.json') as file:
                self.data2= json.load(file)
            
            
            # queryInitials = queryText.split()
            # for word in queryInitials:
            #     queryInit = queryInit + word[0]
            # queryInitial = ("".join(queryInit).lower())
            
            queryText = queryText.lower()
            regex = r'' + queryText + r''

            for features in self.data2['features']:
                    for key, value in features.items():

                        if re.search(regex, value['residence'].lower()):
                            if (value['value'] == 1):
                                self.response = self.response + ("-{} has {} confirmed case of CoViD-19\n".format(value['residence'], value['value']))
                            else:
                                self.response = self.response + ("-{} has {} confirmed cases of CoViD-19\n".format(value['residence'], value['value']))

            for features in self.data['features']:
                    for key, value in features.items():
                        facilityInitials = ""
                        facilityInit = value['facility'].replace(
                            "and", " ").replace(
                                "for", " ").replace(
                                    "-", " ").replace(
                                        "of", " ").replace(
                                            "in", " ").replace(
                                                "the", " ").split()
                        for word in facilityInit:
                            facilityInitials = facilityInitials + word[0]
                        facilityInitials = ("".join(facilityInitials).lower())

                        if re.search(regex, value['facility'].lower())  or re.search(r'^' + queryText , facilityInitials):
                        
                            if (value['count_'] == 1):
                                self.response = self.response + ("-{} has {} patient with CoViD-19\n".format(value['facility'], value['count_']))
                            else:
                                self.response = self.response + ("-{} has {} patients with CoViD-19\n".format(value['facility'], value['count_']))
                        
            if (self.response == ""):
                unknown = ["Sorry, I dont understand.", "I can't comprehend", "Sorry, please check your keywords"]
                return (random.choice(unknown))
                #return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")

            else:
                #return(self.response)
                return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")


#testing
#q = queryingData()
#print(q.loadJson("admin update data"))