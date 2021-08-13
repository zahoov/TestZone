import datetime


class NMEAParser():
    """
    This class takes a single line of GPS NMEA data reading and translates them into usable data such as
    latitude, longitude, timestamps, etc.
    """

    def __init__(self, line: str) -> None:
        """
        Initialization. Only implemented for GGA and RMC data sentences.

        Args:
            line(str): A string line assumed to be a GPS data sentence

        Raises:
            Exception: Raised if non-NMEA data is given (not possessing the $GP tag in the beginning)
            Exception: Raised if the NMEA data is of non-accepted format
        """

        # gets the NMEA data type
        self.NMEAType = line[0:6]
        self.incomplete = False
        self.acceptedFormat = ["GGA", "GSA", "RMC", "VTG", "GSV"]

        # checks if data is NMEA
        if self.NMEAType[0:3] != "$GN":
            raise Exception("Non-NMEA data type given")

        # checks if NMEA data is supported in class
        if self.NMEAType[-3:] not in self.acceptedFormat:
            raise Exception(
                "Given NMEA data is currently not supported with this class")

        # based on accepted format, gets the class method to be called
        #self.parsingMethod = getattr(self, "parse" + "RMC")
        #self.NMEAType[-3:]
        #print(getattr(self, "parse" + self.NMEAType[-3:]))
        #self.parsingMethod(line)
        self.parseRMC(line)
        #print(test)
        #return()

    def parseGGA(self, gga: str) -> None:
        """
        This function takes a string line that is assumed to have the tag $GPGGA and translates the line into readable values
        and stores them as class attributes. Line is separated into an array with split.

        Args:
            gga (str): A string line taken from raw GPS NMEA data. Must have the $GPGGA tag.

        Raises:
            Exception: If the length of split data is not equal to the standard length of GGA data, an exception is raised.
        """

        # splits raw NMEA into an array with 15 elements and gets rid of checksum data
        gga = gga.split("*")[0]
        separatedNMEA = gga.split(",")

        if len(separatedNMEA) != 15:  # checks if data is complete
            self.incomplete = True
            return

        # attribute mapping with dictionary
        self.attributeMap = {
            "timestamp": [1, self.methodTimestamp],
            "latitude": [2, self.methodLatitude],
            "latitudeDirection": [3, None],
            "longitude": [4, self.methodLongitude],
            "longitudeDirection": [5, None],
            "GPSQuality": [6, int],
            "numSatellites": [7, int],
            "horizontalDilution": [8, float],
            "altitude": [9, float],
            "altitudeUnits": [10, None],
            "geoidHeight": [11, float],
            "geoidUnits": [12, None],
            "GPSAge": [13, None],
        }

        # creates new class attributes and assigns them with values using dictionary items
        self.attributeSetting(separatedNMEA, self.attributeMap)

    def parseGSA(self, gsa: str) -> None:
        print("Not implemented yet")
        pass

    def parseGSV(self, gsv: str) -> None:
        print("Not implemented yet")
        pass

    def parseRMC(self, rmc: str) -> None:
        #print('wow')
        """This function takes a string line that is assumed to have the tag $GPRMC and translates the line into readable values
        and stores them as class attributes. Line is separated with split

        Args:
            rmc (str): A string line taken from raw GPS NMEA data. Must have the $GPGGA tag.

        Raises:
            Exception: If the length of split data is not equal to the standard length of RMC data, an exception is raised.
        """

        # splits raw NMEA into an array of 13 elements and gets rid of checksum data
        rmc = rmc.split("*")[0]
        separatedNMEA = rmc.split(",")
        #print(separatedNMEA)

        if len(separatedNMEA) != 13:  # checks if data is complete
            raise Exception(
                "Given NMEA data is not complete. It may be modified or an error may have occured in the GPS system")

        # attribute mapping with dictionary
        self.attributeMap = {
            "timestamp": [1, self.methodTimestamp],
            "status": [2, None],
            "latitude": [3, self.methodLatitude],
            "latitudeDirection": [4, None],
            "longitude": [5, self.methodLongitude],
            "longitudeDirection": [6, None],
            "knotSpeed": [7, float],
            "trackAngle": [8, float],
            "date": [9, self.methodDate],
            "magneticVariation": [10, None],
            "magneticDirection": [11, None]
        }

        self.attributeSetting(separatedNMEA, self.attributeMap)
        #print(self.attributeMap)

    def parseVTG(self, vtg: str) -> None:
        print("Not implemented yet")
        pass

    def methodTimestamp(self, rawStamp: str) -> str:
        """This function takes in raw timestamp from NMEA data and converts them into a Python time object

        Args:
            rawStamp (str): Raw NMEA timestamp

        Returns:
            datetime.time: The timestamp as datetime.time object
        """
        #print(rawStamp)
        #if (len(rawStamp)) < 10:
        #    self.incomplete = True
        #    print('damn')
        #    return

        hour = int(rawStamp[:2]) - 7 if int(rawStamp[:2]
                                            ) >= 7 else 24 + int(rawStamp[:2]) - 7
        minute = rawStamp[2:4]
        seconds = rawStamp[4:6]
        #print(str(hour) + ":" + str(minute) + ":" + str(seconds))

        timestamp = ":".join([str(hour), minute, seconds])
        return timestamp

    def methodDate(self, rawDate: str) -> str:
        """This function takes in raw date string from NMEA data and converts them into a Python date object

        Args:
            rawStamp (str): Raw NMEA date string

        Returns:
            datetime.date: The date as datetime.date object
        """
        
        if (len(rawDate)) < 3:
            self.incomplete = True
            return

        day = rawDate[:2]
        month = rawDate[2:4]
        year = "20" + rawDate[-2:]

        date = "-".join([year, month, day])
        return date

    def methodLatitude(self, rawLat: str) -> float:
        """This function takes in raw latitude string from NMEA and converts them into a float type with its decimal degrees value

        Args:
            rawLat (str): Latitude string in DMM format with no spaces

        Returns:
            float: Latitude float in DD format
        """
        #print(rawLat)
        degree = float(rawLat[0:2])
        minutes = float(rawLat[-7:])
        decimals = minutes / 60.0
        #print(degree + decimals)
        return (degree + decimals)

    def methodLongitude(self, rawLong: str) -> float:
        """This function takes in raw longitude string from NMEA and converts them into a float type with its decimal degrees value

        Args:
            rawLong (str): Longitude string in DMM format with no spaces

        Returns:
            float: Longitude float in DD format
        """

        degree = float(rawLong[0:3])
        minutes = float(rawLong[-7:])
        decimals = minutes / 60.0

        return degree + decimals

    def attributeSetting(self, NMEAList: list, map: dict) -> None:
        """This function takes the separated NMEA and assigns them into class attributes using dictionary

        Args:
            NMEAList (list): The separated NMEA list
            map (dict): Attribute map containing the keys as attribute names and an array consisting of
            the index of attribute in NMEAList and the method necessary to process the raw format of the attribute
        """
        #print(NMEAList)
        # creates new class attributes and assigns them with values using dictionary items
        for key in map:
            # skip data processing if no value in line
            if NMEAList[map[key][0]] == "" and key in ["latitude", "longitude"]:
                map[key] = None
                self.incomplete = True
                #print('no value in line')
                return

            if NMEAList[map[key][0]] == "":
                map[key] = None
                #print('continue')
                continue

            # see if there are any stored methods in the dictionary
            if map[key][1] == None:
                map[key] = NMEAList[map[key][0]]
                #print(NMEAList[map[key][0]])
            # use the method stored in dictionary if it exists
            else:
                
                map[key] = map[key][1](NMEAList[map[key][0]])
                #print(map[key][1](NMEAList[map[key][0]]))
            
        #print(map)
        #return(map)
        
