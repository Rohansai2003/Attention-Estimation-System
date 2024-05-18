import math 

def line_Angle(percentage, sector_number):
    sector_degrees = 60
    angle = percentage * sector_degrees   
    start_angle = (sector_number) * sector_degrees    
    angle +=(start_angle)      
    return angle

def angle_of_acute_bisector(angle1, angle2):
    
    avg_angle = ( (angle1 + angle2) / 2 )%360
    return avg_angle

def sector_and_percentage_from_angle(angle):
    sector_degrees = 60
    sector_number = math.ceil((angle% 360) / sector_degrees)
    
    percentage = ((angle % sector_degrees) / sector_degrees )* 100
    
    
    print(angle)
    return angle ,sector_number ,percentage

def circumplex(percentages):
    new_index_order = [1, 0, 6, 5, 4, 3]
    probs = [percentages[i] for i in new_index_order]
    probable =[]
    probable = probs 
    for i in range(6):
        if probable[i] < 0.1:
            probable[i] = 0   
    
    Angles = []
    for i in range(6):
        if probable[i] == 0:
            continue
        Angles.append(line_Angle(probable[i], i))
    if Angles==None:
        return None, None, None, None
    out = Angles[0]
    for angle in Angles:
        out= angle_of_acute_bisector(out, angle)
    angle_degrees,sector_number, percentage= sector_and_percentage_from_angle(out)
    return probs ,angle_degrees,sector_number, percentage