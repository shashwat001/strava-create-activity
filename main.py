import config
import requests
import datetime as DT
import xml.etree.ElementTree as ET
import xml.dom.minidom
import time
import argparse

def getAPIData(activityid):
    activityUrl = 'https://www.strava.com/activities/' + activityid + '/streams'

    queryString='?stream_types[]=time&stream_types[]=velocity_smooth&stream_types[]=altitude&stream_types[' \
                ']=distance&stream_types[]=latlng'

    cookies = {config.sessionvarname : config.sessionvalue}

    r = requests.get(url = activityUrl + queryString, cookies = cookies)
    data = r.json()
    return data


def convertToISO(timestamp):
    return DT.datetime.utcfromtimestamp(timestamp).isoformat() + 'Z'

def generateTrackpoint(timestamp, latval, lonval, altitude, distance, speed):
    trackpoint = ET.Element('Trackpoint')
    timeNode = ET.SubElement(trackpoint, 'Time')
    timeNode.text = convertToISO(timestamp)

    positionNode = ET.SubElement(trackpoint, 'Position')
    lat = ET.SubElement(positionNode, 'LatitudeDegrees')
    lon = ET.SubElement(positionNode, 'LongitudeDegrees')
    lat.text = str(latval)
    lon.text = str(lonval)

    altitudeNode = ET.SubElement(trackpoint, 'AltitudeMeters')
    altitudeNode.text = str(altitude)

    distanceNode = ET.SubElement(trackpoint, 'DistanceMeters')
    distanceNode.text = str(distance)

    extension = ET.SubElement(trackpoint, 'Extensions')
    tpx = ET.SubElement(extension, 'TPX')
    tpx.set('xmlns', 'http://www.garmin.com/xmlschemas/ActivityExtension/v2')
    speedNode = ET.SubElement(tpx, 'Speed')
    speedNode.text = str(speed)
    return trackpoint

def getTrackXML(ts, data):

    timearr = data['time']
    distancearr = data['distance']
    altitudearr = data['altitude']
    velocityarr = data['velocity_smooth']
    latlngarr = data['latlng']

    track = ET.Element('Track')
    for j in range(len(timearr)):
        track.append(generateTrackpoint(ts + timearr[j], latlngarr[j][0], latlngarr[j][1], altitudearr[j],
                                        distancearr[j], velocityarr[j]))

    return track

def generateActivity(starttime, data):
    starttimeISO = convertToISO(starttime)

    timearr = data['time']
    distancearr = data['distance']
    velocityarr = data['velocity_smooth']

    activitiesnode = ET.Element('Activities')
    activityNode = ET.SubElement(activitiesnode, 'Activity')
    activityNode.set('Sport', 'Biking')

    id = ET.SubElement(activityNode, 'Id')
    id.text = starttimeISO

    lap = ET.SubElement(activityNode, 'Lap')
    lap.set('StartTime', starttimeISO)

    totaltime = ET.SubElement(lap, 'TotalTimeSeconds')
    totaltime.text = str(timearr[-1] - timearr[0])

    distance = ET.SubElement(lap, 'DistanceMeters')
    distance.text = str(distancearr[-1] - distancearr[0])

    maximumspeed = ET.SubElement(lap, 'MaximumSpeed')
    maximumspeed.text = str(max(velocityarr))

    calories = ET.SubElement(lap, 'Calories')
    calories.text = '0'

    intensity = ET.SubElement(lap, 'Intensity')
    intensity.text = 'Active'

    trigger = ET.SubElement(lap, 'TriggerMethod')
    trigger.text = 'Manual'

    lap.append(getTrackXML(starttime, data))

    return activitiesnode

def generateTCX(starttime, data):
    tcd = ET.Element('TrainingCenterDatabase')
    tcd.set('xsi:schemaLocation', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd')
    tcd.set('xmlns:ns5', 'http://www.garmin.com/xmlschemas/ActivityGoals/v1')
    tcd.set('xmlns:ns3', 'http://www.garmin.com/xmlschemas/ActivityExtension/v2')
    tcd.set('xmlns:ns2', 'http://www.garmin.com/xmlschemas/UserProfile/v2')
    tcd.set('xmlns', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')
    tcd.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    tcd.append(generateActivity(starttime, data))
    return tcd

def getXML(activityid, starttime):
    data = getAPIData(activityid)

    activity = ET.tostring(generateTCX(starttime, data))
    print xml.dom.minidom.parseString(activity).toprettyxml()

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--activityid", help="strava activity id", required=True)
parser.add_argument("-s", "--start", help="activity start time in epoch seconds", required=True)

args = parser.parse_args()
getXML(args.activityid, int(args.start))






