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
                "DOH does not offer any public API as of now. Thus, Data is from https://coronavirus-ph-api.herokuapp.com/ and https://covid19.mathdro.id/. However, it may not be up to date with the newest cases that is not yet updated on the APIs.\n" \
                    "\nThe chatbot currently supports the following keywords:\n" \
                        "*INFO - to display information regarding this chatbot\n" \
                            "*PH# - to display the details of the person (ex: PH661)\n"\
                            "*REGION # - to display cases in a region (ex: REGION II (Use Roman Numerals))\n"\
                            "*HOSPITAL - to display cases in a hospital (ex: CAGAYAN VALLEY MEDICAL CENTER or CVMC)\n"\
                                "*CONFIRMED\n"\
                                    "*DEATHS\n"\
                                        "*RECOVERED\n"\
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
            return("Sorry the public API offered by DOH before was unavailable. Thus, the chatbot can't offer information on the number of PUIs.")

        
        elif re.search(r'^(pum)', queryText.lower()):#for PUMs
            return("Sorry the public API offered by DOH before was unavailable. Thus, the chatbot can't offer information on the number of PUMs.")

        elif re.search(r'^(confirmed)|^(confirm)|^(current)', queryText.lower()):#for confirmed cases
            with open('statistics.json') as file:
                self.data = json.load(file)

            return("There are currently {} confirmed cases in the Philippines".format(self.data['confirmed']['value']))

        elif re.search(r'^ph\d+', queryText.lower()): #for PH###
            with open('masterList.json') as file:
                self.data = json.load(file)

            for case in self.data:
                if (str(case['case_no']) == queryText.lower()[2:]):
                    if (case['gender'] == "TBA" and case['age'] == "TBA" and case['resident_of'] == "TBA" and case['hospital_admitted_to'] == "TBA" and case['date'] == "TBA"):
                        return ("{}'s details are not yet available".format(queryText.upper()))
                    else:
                        return ("{}, {}, {}, from Region {} and admitted at {} on {}".format(queryText.upper(), case['gender'], case['age'], case['resident_of'], case['hospital_admitted_to'], case['date']))
            return("{}'s details are not yet available.".format(queryText.upper()))

        if re.search(r'^(recovered)|^(recovery)|^(recover)', queryText.lower()):#for recovered
            with open('statistics.json') as file:
                self.data = json.load(file)

            return("There are currently {} recovered in the Philippines".format(self.data['recovered']['value']))

        if re.search(r'^(death)|^(dead)|^(die)|^(deaths)', queryText.lower()):#for deaths
            with open('statistics.json') as file:
                self.data = json.load(file)

            return("There are currently {} deaths cases in the Philippines".format(self.data['deaths']['value']))

        if re.search(r'^(test)|^(tested)|^(tests)', queryText.lower()):#for tests
            return("Sorry the public API offered by DOH before was taken down by DOH. Thus, the chatbot can't offer updated information anymore.")

        else: #for facility or region
            self.response = ""
            with open('facilityStats.json') as file:
                self.data = json.load(file)
            
            with open('locationStats.json') as file:
                self.data2= json.load(file)
            
            queryText = str(queryText.lower())
            regex = r'' + queryText + r''


            if (queryText.split()[0].strip().lower() == "region"): #for region
                region = queryText.split()[1].strip().upper()

                if region in self.data2:#for residence
                    if (self.data2[region] == 1):
                        self.response = self.response + ("-{} has {} confirmed case of CoViD-19\n".format(queryText.upper(), self.data2[region]))
                    else:
                        self.response = self.response + ("-{} has {} confirmed cases of CoViD-19\n".format(queryText.upper(), self.data2[region]))

            for facility in self.data: #for facility
                facilityInitials = ""
                facilityInit = facility['facility'].replace(
                    "and", " ").replace(
                        "for", " ").replace(
                            "-", " ").replace(
                                "of", " ").replace(
                                    "in", " ").replace(
                                        "the", " ").split()
                for word in facilityInit:
                    facilityInitials = facilityInitials + word[0]
                facilityInitials = ("".join(facilityInitials).lower())

                if re.search(regex, facility['facility'].lower()):
                    if (facility['confirmed_cases'] == 1 and facility['puis'] == 1):
                        self.response = self.response + ("-{} has {} confirmed case and {} PUI of CoViD-19\n".format(facility['facility'].upper(), facility['confirmed_cases'], facility['puis']))
                    elif (facility['puis'] == 1):
                        self.response = self.response + ("-{} has {} confirmed cases and {} PUI of CoViD-19\n".format(facility['facility'].upper(), facility['confirmed_cases'], facility['puis']))
                    elif (facility['confirmed_cases'] == 1):
                        self.response = self.response + ("-{} has {} confirmed case and {} PUIs of CoViD-19\n".format(facility['facility'].upper(), facility['confirmed_cases'], facility['puis']))
                    else:
                        self.response = self.response + ("-{} has {} confirmed cases and {} PUIs of CoViD-19\n".format(facility['facility'].upper(), facility['confirmed_cases'], facility['puis']))

            if (self.response == ""):
                unknown = ["Sorry, I dont understand.", "I can't comprehend", "Sorry, please check your keywords"]
                return (random.choice(unknown))

            else:
                return(self.response)


#testing purposes
#q = queryingData()
#print(q.loadJson("cagayan"))