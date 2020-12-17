'''
Jayden Lefebvre
Gamify - ESC180 - Fall 2020
'''

#Current hedons and health poinrs (integers).
cur_hedons = 0
cur_health = 0

#Current stars assignment time (integer) and activity (string).
cur_star = None
cur_star_activity = None

#Stores if the user is bored with stars (boolean), and the times of the last 3 star offers (integers).
bored_with_stars = False
last_3_stars = [-1000, -1000, -1000]

#Which activity did the user last complete (string)? 
#How long had the latest activity been going on, cumulatively (integer)?
last_activity = None
cumulative_activity_duration = 0

#Current time (integer)
cur_time = 0
#At what time did the last exercise (running/textbooks) end (integer)?
last_exercise_end = -1000

def initialize():
    '''Initialize the global variables needed for the simulation.'''
    global cur_hedons, cur_health, cur_star, cur_star_activity, bored_with_stars, last_3_stars
    global last_activity, cumulative_activity_duration, cur_time, last_exercise_end
    cur_hedons = 0
    cur_health = 0
    cur_star = None
    cur_star_activity = None
    bored_with_stars = False
    last_3_stars = [-1000, -1000, -1000]
    last_activity = None
    cumulative_activity_duration = 0
    cur_time = 0
    last_exercise_end = -1000

def is_tired():
    '''
    Is the user tired?
    The user is tired if they finished running or carrying textbooks less than 2 hours before the current activity started.
    '''
    return last_exercise_end + 120 > cur_time

def get_effective_minutes_left_hedons(activity):
    '''Return the number of minutes during which the user will get the full
    amount of hedons for activity 'activity'. Returns 0 by default, or if unlimited minutes left.'''
    if activity == "resting":
        return 0
    elif activity == "running":
        if not is_tired():
            result = 10
        else:
            return 0
    elif activity == "textbooks":
        if not is_tired():
            result = 20
        else:
            return 0
    else:
        return 0
    if activity == last_activity:
        result = max(result - cumulative_activity_duration, 0)
    return result

def get_effective_minutes_left_health(activity):
    '''Return the number of minutes during which the user will get the full
    amount of health points for activity 'activity'. Returns -1 if activity is invalid, or unlimited minutes left.'''
    if activity == "running":
        result = 180
    elif activity == "textbook":
        return 0
    else:
        return 0
    if activity == last_activity:
        result = max(result-cumulative_activity_duration, 0)
    return result

def estimate_hedons_delta(activity, duration):
    '''Return the amount of hedons the user would get for performing activity
    'activity' for duration minutes'''
    effective = get_effective_minutes_left_hedons(activity)
    star_hedons = 0
    if star_can_be_taken(activity):
        star_hedons = 3 * min(duration, 10)
    if activity == "running":
        if is_tired():
            return -2 * duration + star_hedons
        else:
            return 2 * min(effective, duration) - 2 * max(duration-effective, 0) + star_hedons
    if activity == "textbooks":
        if is_tired():
            return -2 * duration + star_hedons
        else:
            return min(effective, duration) - max(duration-effective, 0) + star_hedons
    return star_hedons

def estimate_health_delta(activity, duration):
    '''Return the amount of health points the user would get for performing activity
    'activity' for duration 'duration'.'''
    effective = get_effective_minutes_left_health(activity)
    if activity == "running":
        return 3 * min(effective, duration) + max(duration-effective, 0)
    if activity == "textbooks":
        return 2 * duration
    if activity == "resting":
        return 0    
    
def perform_activity(activity, duration):
    '''
    Perform a given activity 'activity' for a given duration 'duration'. 
    Calculates and applies hedons, health points, stars, etc.
    '''
    global bored_with_stars, cur_health, cur_hedons, cumulative_activity_duration, last_activity, cur_time, last_exercise_end
    #Check activity and duration
    if activity not in ["running", "textbooks", "resting"]:
        return
    #Check star boredom
    if last_3_stars[2] + 180 > cur_time:
        bored_with_stars = True
    #Get and apply hedons and health
    cur_hedons += estimate_hedons_delta(activity, duration)
    cur_health += estimate_health_delta(activity, duration)
    #Check match, reset consecutivity
    if activity != last_activity:
        cumulative_activity_duration = duration
        last_activity = activity
    #Add time, set last exercise end
    cur_time += duration
    if activity in ["running", "textbooks"]:
        last_exercise_end = cur_time
    
def star_can_be_taken(activity):
    '''
    Is there a star that can be taken and used on a given activity 'activity'?
    True iff no time passed between the star’s being offered and the activity, and the user is not bored with
    stars, and the star was offered for this activity.
    '''
    return cur_star_activity == activity and not bored_with_stars and cur_star == cur_time

def get_cur_hedons():
    '''
    Get accumulated hedons so far.
    '''
    return cur_hedons
    
def get_cur_health():
    '''
    Get accumulated health points so far.
    '''
    return cur_health
    
def offer_star(activity):
    '''
    Offer the user a star for a given activity 'activity'. Shifts star tracking list.
    '''
    global cur_star, cur_star_activity, last_3_stars
    #Check activity
    if activity not in ["running", "textbooks", "resting"]:
        return
    #Set star activity and time
    cur_star = cur_time
    cur_star_activity = activity
    #Shift stars, add latest
    last_3_stars[1:3] = last_3_stars[0:2]
    last_3_stars[0] = cur_star
        
def most_fun_activity_minute():
    '''
    Which activity would give the most hedons for one minute?
    '''
    best = "resting" #True neutral, always zero
    hedons = 0
    for a in ["running", "textbooks", "resting"]:
        h = estimate_hedons_delta(a, 1)
        if h > hedons:
            best = a
            hedons = h
    return best
        
# Test code
if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)    
    print(get_cur_hedons())            #-20 = 10 * 2 + 20 * (-2)
    print(get_cur_health())            #90 = 30 * 3
    print(most_fun_activity_minute())  #resting
    perform_activity("resting", 30)    
    offer_star("running")              
    print(most_fun_activity_minute())  #running
    perform_activity("textbooks", 30)  
    print(get_cur_health())            #150 = 90 + 30*2
    print(get_cur_hedons())            #-80 = -20 + 30 * (-2)
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health())            #210 = 150 + 20 * 3
    print(get_cur_hedons())            #-90 = -80 + 10 * (3-2) + 10 * (-2)
    perform_activity("running", 170)
    print(get_cur_health())            #700 = 210 + 160 * 3 + 10 * 1
    print(get_cur_hedons())            #-430 = -90 + 170 * (-2)
    
    