import json
import random
import re
import dataScrape

class queryingData:

    def loadJson(self, queryText):
        
        if (queryText.lower() == "admin update data"):
            try:
                dataScrape.getData()
                return("Data updated successfully")  
            except Exception as ex:
                return(ex)

        elif (queryText.lower() == "info"):
            self.info = "Hi this chatbot is created to track statistics of the CoViD-19 pandemic in the Philippines.\n" \
                "Data is from the public API of DOH. However, it may not be up to date with the newest cases that is not yet updated on the DOH's server.\n" \
                    "\nThe chatbot currently supports the following keywords:\n" \
                        "*INFO - to display information regarding this chatbot\n" \
                            "*PH# - to display the details of the person (ex: PH661)\n"\
                            "*PLACE\HOSPITAL - to display current cases in a place or hospital (ex: CAGAYAN or CAGAYAN VALLEY MEDICAL CENTER)\n"\
                            "*PUI\n"\
                                "*PUM\n"\
                                    "*CONFIRMED\n"\
                                        "*DEAD\n"\
                                            "*RECOVERED\n"\
                                                "*TESTS"
                                                    

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

        elif re.search(r'(pui)', queryText.lower()):#for PUIs
            with open('statistics.json') as file:
                self.data = json.load(file)

            for features in self.data['features']:
                for key, value in features.items():
                    return("There are currently {} PUIs in the Philippines".format(value['PUIs']))
        
        elif re.search(r'pum', queryText.lower()):#for PUMs
            with open('statistics.json') as file:
                self.data = json.load(file)

            for features in self.data['features']:
                for key, value in features.items():
                    return("There are currently {} PUMs in the Philippines".format(value['PUMs']))

        elif re.search(r'(confirmed)|(confirm)|(current)', queryText.lower()):#for confirmed cases
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

        if re.search(r'(recovered)', queryText.lower()):#for recovered
            with open('statistics.json') as file:
                self.data = json.load(file)

            for features in self.data['features']:
                for key, value in features.items():
                    return("There are currently {} recovered in the Philippines".format(value['recovered']))

        if re.search(r'(deaths)|(dead)', queryText.lower()):#for deaths
            with open('statistics.json') as file:
                self.data = json.load(file)

            for features in self.data['features']:
                for key, value in features.items():
                    return("There are currently {} deaths in the Philippines".format(value['deaths']))

        if re.search(r'(pui)', queryText.lower()):#for tests
            with open('statistics.json') as file:
                self.data = json.load(file)

            for features in self.data['features']:
                for key, value in features.items():
                    return("There are currently {} tests conducted in the Philippines".format(value['tests']))

        else: #for facility or place
            self.response = ""
            with open('facilityStats.json') as file:
                self.data = json.load(file)
            
            with open('locationStats.json') as file:
                self.data2= json.load(file)

            for features in self.data2['features']:
                    for key, value in features.items():
                        queryText = queryText.lower()
                        regex = r'' + queryText + r''

                        if re.search(regex, value['residence'].lower()):
                            self.response = self.response + ("-{} has {} confirmed cases of CoViD-19\n".format(value['residence'], value['value']))
                            #return("{} has {} patients with CoViD-19".format(value['facility'], value['count_']))

            for features in self.data['features']:
                    for key, value in features.items():
                        queryText = queryText.lower()
                        regex = r'' + queryText + r''

                        if re.search(regex, value['facility'].lower()):
                            self.response = self.response + ("-{} has {} patients with CoViD-19\n".format(value['facility'], value['count_']))
                            #return("{} has {} patients with CoViD-19".format(value['facility'], value['count_']))

            if (self.response == ""):
                unknown = ["Sorry, I dont understand.", "I can't comprehend", "Sorry, please check your keywords"]
                return (random.choice(unknown))
            else:
                return(self.response)

# for features in self.data['features']:
#                 for key, value in features.items():
#                     if (value['PH_masterl'] == queryText.upper()):
#                         return ("{}, {}, {}, resident of {} and admitted at {}".format(value['PH_masterl'], value['kasarian'], value['edad'], value['residence'], value['facility']))
        

    # def userQuery(self, queryText):

        
                
    #     if re.search(r'PUI', queryText.lower()):
    #         for features in self.data['features']:
    #             for key, value in features.items():

    #     else:            
    #         for features in self.data['features']:
    #             for key, value in features.items():

    #                 if re.search(r'^ph\d+', queryText.lower()):
    #                     if (value['PH_masterl'] == queryText):
    #                         return (value['residence'])
                    
    #                 else:
    #                     unknown = ["Sorry, I dont understand.", "I can't comprehend", "Sorry, please check your keywords"]
    #                     return(random.choice(unknown))
                


    #             #print(value['FID'])
    #             # for val2 in value['PH_master1']:
    #             #     print(val2['PH661'])

# q = queryingData()
# print(q.loadJson("cagayan"))