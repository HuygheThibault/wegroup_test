from __future__ import absolute_import
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from app.models.zipcode import ZipCodeRiskFactor

import requests
import csv
import datetime
import calendar


class IndexResponse(BaseModel):
    index: float


async def get_index(request: Request, year: int = 2004):
    # EXERCISE 1

    # TODO INDEX_1
    # Make sure only 1996, 2004 and 2013 are valid
    # https://fastapi.tiangolo.com/tutorial/handling-errors/
    # tip: from fastapi import HTTPException
    valid = [1996, 2004, 2013, 2020]

    if year not in valid:
        raise HTTPException(
            status_code=404,
            detail="Year is not valid, please choose one of the following: {}".format(valid),
            headers={"Error": "Not a valid year"}
        )

    # TODO INDEX_2
    # Retrieve the latest index from external source for given base year
    # https://statbel.fgov.be/en/themes/consumer-prices/health-index
    response = requests.get("https://bestat.statbel.fgov.be/bestat/api/views/48744f07-252a-4a42-bca3-a2d7cb31c2fd/result/JSON")
    r = response.json()["facts"]

    index = 0

    for i in r:
        if int(i["Base year"].split("=")[0]) == year \
                and int(i["Month"].split(" ")[1]) == datetime.datetime.now().year \
                and i["Month"].split(" ")[0] == calendar.month_name[datetime.datetime.now().month - 1]: # Get last 'completed' month
            index = i["Health index"]

    # TODO INDEX_3
    # Format and return the response
    return {"index": index}


async def get_zipcode_risk_factor(request: Request, zipcode: int):
    # EXERCISE 2

    # TODO ZIPCODE_1
    # Validate if the zipcode entered has the correct format (integer between 1000 and 9999)

    if 1000 <= zipcode <= 9999:
        print("valid")
    else:
        raise HTTPException(
            status_code=404,
            detail="zipcode is not valid, please choose a number between 1000 and 9999",
            headers={"Error": "Not a valid zipcode"}
        )

    # TODO ZIPCODE_2
    # Read the file app.data.zipcodes.csv and format data

    zipcodes = {}

    with open('./app/data/zipcodes.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            boundries = row[0].split("-")

            if len(boundries) > 1:
                r = range(int(boundries[0]), int(boundries[1]) + 1)
                for item in list(r):
                    zipcodes[item] = row[1]
            else:
                zipcodes[boundries[0]] = row[1]

    # TODO ZIPCODE_3
    # Validate if the zipcode entered is in the dataset

    if zipcode in zipcodes.keys():
        # TODO ZIPCODE_4
        # Formulate appropriate response
        return {"zipcode": zipcode,
                "risk_factor": zipcodes[zipcode]}
    # else:
    #     zipcode_class = "Not available"


async def get_zipcode_risk_factor_from_database(request: Request, zipcode: int):
    # EXERCISE 3
    # TODO database exercise
    if 1000 <= zipcode <= 9999:
        print("valid")
    else:
        raise HTTPException(
            status_code=404,
            detail="zipcode is not valid, please choose a number between 1000 and 9999",
            headers={"Error": "Not a valid zipcode"}
        )



    return await request.app.repositories.zipcodes.get(zipcode)


router = APIRouter()


router.add_api_route(
    "/index/{year}",
    get_index,
    include_in_schema=True,
    deprecated=False,
    methods=["GET"],
    status_code=200,
    description="Retrieve the latest Belgian health index from external source for given base year. (default 2004)",
    summary="Retrieve Belgian Health Index",
    tags=["EX1"],
    response_model=IndexResponse,
)


router.add_api_route(
    "/zipcode/{zipcode}",
    get_zipcode_risk_factor,
    include_in_schema=True,
    deprecated=False,
    methods=["GET"],
    status_code=200,
    description="Retrieve the risk factor associated with given zipcode",
    summary="Retrieve Zipcode Risk Factor",
    tags=["EX2"],
    response_model=ZipCodeRiskFactor,
)

router.add_api_route(
    "/databases/zipcode/{zipcode}",
    get_zipcode_risk_factor_from_database,
    include_in_schema=True,
    deprecated=False,
    methods=["GET"],
    status_code=200,
    description="Retrieve the risk factor associated with given zipcode from databases",
    summary="Retrieve Zipcode Risk Factor from database",
    tags=["EX3"],
    response_model=ZipCodeRiskFactor,
)
