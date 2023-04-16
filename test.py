import requests
import json

def getPropertiesList():
    results = []
    pageCount = 1
    while True:
        print(f"Fetching page {pageCount}...")
        url = f"https://www.magicbricks.com/mbsrp/propertySearch.html?editSearch=Y&category=R&propertyType=10002,10003,10021,10022,10020&city=2951&page={pageCount}&groupstart=90&offset=0&maxOffset=121&sortBy=relevant&postedSince=-1&pType=10002,10003,10021,10022,10020&isNRI=N&multiLang=en"
        response = requests.get(url)
        if response.status_code != 200:
            # Save results to file
            with open("properties_listing.json", "w") as f:
                f.write(json.dumps(results, indent=4))
            break
        data = response.json()
        results.extend(data["resultList"])
        pageCount += 1
    return results

def getLandmarkData(propID, latitude, longitude):
    url = f"https://www.magicbricks.com/mbldp/getLandmarkData?propId={propID}&isRental=Y"
    response = requests.post(url, json={"lat": latitude, "lng": longitude, "city":"2951"})
    data = response.json()
    data = data["finalResultLandmarks"]
    # return data
    # To get all closer landmarks, comment the below two lines and uncomment above line
    closestLandmarks = [{landmark["label"]: landmark["data"][0]} for landmark in data]
    return closestLandmarks

def main():
    # Update Properties List, Uncomment once a day to update
    # getPropertiesList()
    # Fetch updated listing
    with open("properties_listing.json", "r") as f:
        results = json.loads(f.read())
    # Add landmark data
    for i, result in enumerate(results):
        print(f"Fetching landmark data for property {i+1}: {result['auto_desc']}...")
        propID = result["id"]
        latitude = result["pmtLat"]
        longitude = result["pmtLong"]
        result["nearestLandmarkDetails"] = getLandmarkData(propID, latitude, longitude)
        results[i] = result
        print("\n\n------------------\n\n")
    # Update results file with latest landmark data
    with open("results.json", "w") as f:
        f.write(json.dumps(results, indent=4))

main()