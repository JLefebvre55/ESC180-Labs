cur_hedons = 0
cur_health = 0
last_hedons = 0
last_health = 0
    
cur_star = None
cur_star_activity = None
last_star_time = 0
    
bored_with_stars = False
    
last_activity = None
last_activity_duration = 0
    
cur_time = 0
    
last_finished = -1000

def initialize():
    '''Initializes the global variables needed for the simulation. Incomplete'''
    
    global cur_hedons, cur_health, last_hedons, last_health

    global cur_time
    global last_activity, last_activity_duration
    
    global last_finished
    global bored_with_stars
    
    cur_hedons = 0
    cur_health = 0
    last_hedons = 0 
    last_health = 0
    
    cur_star = None
    cur_star_activity = None
    last_star_time = 0
    
    bored_with_stars = False
    
    last_activity = None
    last_activity_duration = 0
    
    cur_time = 0
    
    last_finished = -1000

def is_tired():
    '''Have there been less than 2 hours since the end of the last exercise?'''
    return cur_time-last_exercise_end < 120

def update_health(health):
    global last_health, cur_health
    last_health = health
    cur_health += health
    
def update_hedons(hedons):
    global last_hedons, cur_hedons
    last_hedons = hedons
    cur_hedons += hedons
    
def perform_activity(activity, minutes):
    '''
    Perform a given activity for a given number of minutes.
    Assumes activity is a string, one of "running", "textbooks", or "resting".
    '''
    
    if minutes not in ["running", "textbooks", "resting"] or minutes < 0:
        return
    
    result_health = 0
    result_hedons = 0
    duration = minutes
    
    #If we are continuing the same activity, remove last increment, combine last minutes
    
    
    result_health += estimate_health_delta(activity, minutes)
    result_hedons += estimate_hedons_delta(activity, minutes)
    
    update_health(result_health)
    update_health(result_hedons)
    last_activity = activity
    last_activity_duration = minutes
    cur_time += minutes
    
def estimate_hedons_delta(activity, minutes):
    if activity == "running":
        if is_tired():
            return -2*minutes
        else:
            return 2*min(minutes, 10)-2*max(minutes-10, 0)
    if activity == "textbooks":
        if is_tired():
            return -2*minutes
        else:
            return min(minutes, 20)-max(minutes-20, 0)
    else:
        return 0
    
def estimate_health_delta(activity, minutes):
    result = 0
    if activity == last_activity:
        result -= last_health
        minutes += last_activity_duration
    if activity == "running":
        result+=min(minutes,180)*3 + max(0, minutes-180)
    if activity == "textbooks":
        return 2*minutes
    else:
        return

def star_can_be_taken(activity):
    return activity == cur_star_activity and not bored_with_stars and last_star_time == cur_time

def get_cur_hedons():
    return cur_hedons
    
def get_cur_health():
    return cur_health
    
def offer_star(activity):
    return last_star_time == cur_time
        
def most_fun_activity_minute():
    return max([estimate_hedons_delta(a) for a in ["running", "textbooks", "resting"]])
    
################################################################################
#These functions are not required, but we recommend that you use them anyway
#as helper functions

def get_effective_minutes_left_hedons(activity):
    '''Return the number of minutes during which the user will get the full
    amount of hedons for activity activity'''
    pass
    
def get_effective_minutes_left_health(activity):
    pass    
    
###############################################################################
if __name__ == "__main__":
    perform_activity("running", 120)
    print(get_cur_health())
    perform_activity("running", 30)
    print(get_cur_health())
    perform_activity("running", 50)
    print(get_cur_health())
#     initialize()
#     perform_activity("running", 30)    
#     print(get_cur_hedons())            #-20 = 10 * 2 + 20 * (-2)
#     print(get_cur_health())            #90 = 30 * 3
#     print(most_fun_activity_minute())  #resting
#     perform_activity("resting", 30)    
#     offer_star("running")              
#     print(most_fun_activity_minute())  #running
#     perform_activity("textbooks", 30)  
#     print(get_cur_health())            #150 = 90 + 30*2
#     print(get_cur_hedons())            #-80 = -20 + 30 * (-2)
#     offer_star("running")
#     perform_activity("running", 20)
#     print(get_cur_health())            #210 = 150 + 20 * 3
#     print(get_cur_hedons())            #-90 = -80 + 10 * (3-2) + 10 * (-2)
#     perform_activity("running", 170)
#     print(get_cur_health())            #700 = 210 + 160 * 3 + 10 * 1
#     print(get_cur_hedons())            #-430 = -90 + 170 * (-2)