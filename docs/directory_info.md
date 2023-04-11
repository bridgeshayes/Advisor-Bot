BaseURL:  `https://portapi.tntech.edu/express/api/unprotected/getDirectoryInfoByAPIKey.php`
Parameters:
* apiKey (required)
* searchCriteria (required)
	
#### Example Calls

Search By Name:
```
https://portapi.tntech.edu/express/api/unprotected/getDirectoryInfoByAPIKey.php?apiKey=764AA90B-E06A-4A05-BE23-774DF2ECC33&searchCriteria=burchfield
```

Search By Department:
```
https://portapi.tntech.edu/express/api/unprotected/getDirectoryInfoByAPIKey.php?apiKey=764AA90B-E06A-4A05-BE23-774DF2ECC33&searchCriteria=deptsearchComputer%20Science
```

Search By Email Address:
```
https://portapi.tntech.edu/express/api/unprotected/getDirectoryInfoByAPIKey.php?apiKey=764AA90B-E06A-4A05-BE23-774DF2ECC33&searchCriteria=bburchfield@tntech.edu
```

Search By Phone Extension:
```
https://portapi.tntech.edu/express/api/unprotected/getDirectoryInfoByAPIKey.php?apiKey=764AA90B-E06A-4A05-BE23-774DF2ECC33&searchCriteria=3389
```

#### Expected Results
The user will normally receive an array of JSON objects with the properties of:

	* LastName
	* FirstName
	* MiddleName
	* EmailAddress
	* Dept
	* Title
	* Phone
	* Building
	* POBOX
	* OrgnCode
		
#### Example Return
```json
[{
    "FirstName": "Jerry",
    "LastName": "Gannod",
    "EmailAddress": "jgannod@tntech.edu",
    "Dept": "Computer Science",
    "Title": "Chairperson",
    "Phone": "931-372-3691",
    "Building": "Bruner Hall (BRUN) 242",
    "POBox": "5101"
  }
]
```

#### Error Results

| Error                                                                             | Description |
|-----------------------------------------------------------------------------------| ------------|
| {"Error": "User not authorized for this function"}                                | A request with a bad apiKey |
| {"Error" : "APIKey cannot be blank"}                                              | A request with a blank or missing apiKey will return a JSON object |	
| {"Error": "SearchCriteria cannot be blank"}                                       | A request that has a blank or is missing the searchCriteria will return a JSON object |
| [{"Error": "APIKey cannot be blank"}, {"Error":"SearchCriteria cannot be blank"}] | Multiple blank or missing parameters will result in an array of JSON objects |

