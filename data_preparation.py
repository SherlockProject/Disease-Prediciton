##Database Connection
import couchdb
import time
import us
import numpy as np
import datetime as dt



class Data_preparation:
     
    
    
    @staticmethod
    def getTweetCount(startdate, enddate):
        couch = couchdb.Server('https://c46dc820-3d2a-4b8e-9a4b-839619a7afc0-bluemix.cloudant.com')
        db_tweets = couch['flutweets']
        
        
        tweets = []
        for result in db_tweets.view("index/getDates"):
            tempdate = result['key'].split(" ")[1] + "-" + result['key'].split(" ")[2] + "-" + result['key'].split(" ")[5] + "-" + result['key'].split(" ")[3]
            date = dt.datetime.strptime(tempdate,"%b-%d-%Y-%H:%M:%S");
            if date >= startdate and date <= enddate:
                tweets.append(len(db_tweets[result['id']]['data']))
        
        return tweets

        
            
            
    
    
    
    
    
    
    
    @staticmethod
    def GetMostRecentData(amount_of_tweets):    
        ###############################################################
        ##  Step 1: Read data from all sources
        ###############################################################
        
        ## Time for speed measure
        time1 = time.time()
        
        
        ##Open Server Connection 
        couch = couchdb.Server('https://c46dc820-3d2a-4b8e-9a4b-839619a7afc0-bluemix.cloudant.com')
        db = couch['locations']
        db_tweets = couch['flutweets']
        db_state = couch['disease_data']
        
        
        #### GET TWEETS
        tweets = [];
        dates =[]
        j = 0
        for result in  db_tweets.view('index/index'):
            tweets.extend(result['value']);
            j+=1;
            if j == amount_of_tweets:
                break;
            
        for result in  db_tweets.view('index/date'):
            dates.append(result)
            break;    
        
        print dates
        #### GET STATEDATA
        
        data = []
        all_states = []
        
        for result in db_state.view("states/getAll"):
            all_states = result
        
        
        # List with every state only once
        corrected_states = []
        # Bool for inserting new values
        insert = True;
        #exists = False;
        # Get the date that we are interested in
        date = dt.datetime.strptime(dates[0]["value"],"%b-%d-%Y");
        print "date: " + str(date)
        
        #Iterate through entries, insert only the newest ones
        for entry in all_states['value']:
            if len(corrected_states) > 0:
                for subentry in corrected_states:
                    if subentry["state"] == entry["state"]:
                        #exists = True;
                        #Compare the dates of 2 entries
                        old = dt.datetime.strptime(subentry['date'],"%b-%d-%Y")
                        new = dt.datetime.strptime(entry['date'],"%b-%d-%Y")
                        if new > old and new <= date: 
                            insert = True;
                            corrected_states.remove(subentry);
                        else:
                            insert = False;
                            
                    else:
                        insert = True;
                        
            if insert:
                corrected_states.append(entry)
                insert = False;
        
        
        #List with the levels inside
        #data = np.zeros(len(corrected_states))
        
        #print "Corrected States: "+ str(corrected_states)
        
        for i in corrected_states:
            level = int( i['level'].split(" ")[1])
            data.append(level)
        
        #print "data: "+str(data)       
        ##############################################################
        ## Step 2: DATA PREPARATION:
        ##############################################################
        
        
        ## Buckets for the tweet sorting
        state_tweets= np.zeros(53)
        
        ### Array for the citynames and state IDs
        city_states = {};
        for result in  db.view('namequery/namequery'):
            city_states[len(city_states)-1] = result;
            
        
        
        
        
        
        ## Storage to store already found cities and speed it up
        storage = {}
        
        
        ## State mapping for later sorting:
        name_to_fips = us.states.mapping('abbr', 'fips')
        
        
        ###############################################################
        ##  Step 3: Sort data in the state array
        ###############################################################
        
        ## Iterate through the tweets
        for tweetcount in range(len(tweets)):
            ## Get city name
            #city = data_dict[0]['tweetList'][tweetcount]['user']['location']
            city = tweets[tweetcount]['location']
            
            if(len(city)>3 and not(city is None) ):  
                ## check, if the city is already in the storage
                if city in storage:
                    state_id = storage[city];
                    if state_id < 53:
                        state_tweets[state_id] += 1;
                        
                
                ## Else find out if the city is in the US and if so, what its 
                ## state ID is
                else:
                    
                    for result in range(len(city_states)-1):
                        #String preparation
                        if "," in city:
                            city = city.split(",")[0];
                        if city_states[result]["key"] == city:
                            #print city_states[result]["key"] +" - " + city + ", num: "+ str(tweetcount)
                          
                            index = int(name_to_fips[city_states[result]["value"] ])
                            #print index
                            if index < 53:
                                state_tweets[index] += 1;
                            storage[city] =index;
          
                            break;  
                            
                             
                                     
                                    
               
                
        ## Print time as a speed measure      
        time2 = time.time();
        timedelta=time2-time1;
        
        #To avoid errors in case of too few tweets- unlikely to happen
        if(max(state_tweets) == 0):
            state_tweets[0] = 1;
          
        print "time :" + str(timedelta)
        
        # Return the x and y value
        return (state_tweets, data);
        