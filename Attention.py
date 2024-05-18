import math 

def calculate_hypotenuse(a, b):
    if a is not None and b is not None:
        return math.sqrt(pow(a, 2) + pow(b, 2))
    else:
        return None

def percentage_attention_values(value, lower_bound, upper_bound):
    if lower_bound <= value <= upper_bound:
        range_size = upper_bound - lower_bound
        distance_from_lower = value - lower_bound
        percentage = (distance_from_lower / range_size) * 100
        return percentage
    else:
        return 0
    
def attention_percentage(hr, vr):
    if hr==None or vr==None:
        return None,None, None,None
    val = calculate_hypotenuse(hr, vr)
    per = 0
    sector = 0
    if 0.740 <= val < 0.775:
        per =percentage_attention_values(val, 0.740, 0.775)
        sector = 4
    elif 0.775 <= val < 0.798:
        per= percentage_attention_values(val, 0.775, 0.798)
        sector = 1
    elif 0.798 <= val < 0.843:
        per= percentage_attention_values(val, 0.798, 0.843)
        sector = 5
    elif 0.843 <= val < 0.878:
        per =percentage_attention_values(val, 0.843, 0.878)
        sector = 3
    elif 0.878 <= val < 0.909:
        per =percentage_attention_values(val, 0.878, 0.909)
        sector = 6
    elif 0.909 <= val <= 1.078:
        per = percentage_attention_values(val, 0.909, 1.078)
        sector = 2
    else:
        per=0
        sector =0
    angle_degrees= line_Angle(per, sector) 
    print(angle_degrees)
    return val,angle_degrees, sector, per    

def line_Angle(percentage, sector_number):
    sector_degrees = 60   
    angle = (percentage/100 )* sector_degrees
    start_angle = (sector_number-1) * sector_degrees    
    angle +=(start_angle)      
    return angle

