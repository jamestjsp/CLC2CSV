# CLC2CSV
A CLC file Conversion utility

## Need of CLC file convertion

The CLC file is designed to parse only on DMCPlus or AspenIQ aplication. This is not a standerd CSV format, if the user need the data to load in any other aplication like System Identification Toolbox™ from MATLAB® one need to manualy edit the file to a standerd CSV format. The Python script is an attempt to automate the manual task.

## What is Advanced Control Collect?

Aspen Advanced Control Collect provides data collection and data extraction functions for use on all Advanced Control-supported platforms. Data collection and data extraction are handled by two separate tools.

**Data collection**
The data collection capability of Advanced Control Collect allows you to specify the sample period for collection and the tags for which data is to be collected, by adding them to an Input file. This Input file is run by Advanced Control Collect when the data collection process is started.
What is Advanced Control Collect?

**Data extraction**
The data extraction capability of Advanced Control Collect allows extracting all data collected or choosing to extract a specific sample period, tags, and/or the beginning and ending times and dates of extraction. The default values are set for extracting the most amount of data collected.
About data extraction

After the data extraction process is complete, a file is created in which the extracted data is stored. This extraction file is also called a **.clc file**, since it is the extension added to the file name (*filename.clc*).

## **CLC format**

The .clc file contains sections of information derived using the extraction tool. A delimiter (a line of 50 equal signs) will separate the sections of the file.

**Section 1**:
The first section of the .clc file contains header information in the following order:
Line	1.	filename of the Input file
	2.	description from Line 1 of the Input file
	3.	number of tags extracted
	4.	number of tags per section
	5.	beginning time of extraction (MM-DD-YYYY(blank)hh:mm:ss)
	6.	sample period of extraction
	7.	number of samples extracted

**Section 2**:

The second section contains a list of the extraction tags. Each extraction tag will be listed with its corresponding model tag, description, and engineering units, using the following format:

>Model tag\~\~\~Collect tag\~\~\~Tag description\~\~\~Engineering units

where:
	Model tag is a unique name, up to twelve characters, all capital letters.

>**Note:** Model tag names are limited to no more than 12 characters, because this is a limitation of the Model (.mdl) file format. Advanced Control Collect and Model enforce this limit. This limitation does not affect the actual DCS tags however, which are called "entities" (in Model) and collection tags (in Advanced Control Collect). This limitation only affects the model tags.

Collect tag is the actual tag read from the Input file.

Tag description is the description for the collect tag (possibly a blank).

Engineering units are the engineering units for the tag (possibly a blank).

**Section 3 to end**:

The last sections contain the extracted numerical data. Due to computer limitations, the number of sections depends on the number of extraction tags. The number of tags per section is listed on line 4 of section 1; the last section will contain the residual. The format of the data will be as follows:

>timestamp,valuefortag1,statusfortag1,valuefortag2,statusfortag2,valuefortag3,statusfortag3,etc.

where:

timestamp is the date and time (**MM-DD-YYYY(blank)hh:mm:ss**) of that sample.

value for tag is the collected data

status is one of the following:

-   **G** – represents a good value
-   **B** – represents a bad value (i.e. -9999)
-   **M** – represents a missed sample (i.e.-10000)
-   **S** – represents a collection time that slipped a little

Example CLC file

## Example CLC file

The following is an example clc file.

	PLUS3
	plus3 sample Input file for Advanced Control Collect
	5
	2
	12/16/1997 12:19
	60
	5
	==========================================
	"PLUSMAINCNTD~~~""""::""PlusMain.CNTDWN"":DBVL:~~~Tag description~~~Engineering unit"
	"PLUSMAINONRE~~~""""::""PlusMain.ONREQ"":ORD:~~~Tag description~~~Engineering unit"
	"PLUSMAINLSTT~~~""""::""PlusMain.LSTTIM"":DBVL:~~~Tag description~~~Engineering unit"
	"DMCF107SP~~~""""::""DMCF107.SP"":DBVL:~~~Tag description~~~Engineering unit"
	"DMCP103SP~~~""""::""DMCP103.SP"":DBVL:~~~Tag description~~~Engineering unit"
	============================================
	12/16/1997 12:19,150,G,0,G
	12/16/1997 12:20,150,G,0,G
	12/16/1997 12:21,150,G,0,G
	12/16/1997 12:22,150,G,0,G
	12/16/1997 12:23,150,G,0,G
	============================================
	12/16/1997 12:19,112502,G,4.795,G
	12/16/1997 12:20,112502,G,4.795,G
	12/16/1997 12:21,112502,G,4.795,G
	12/16/1997 12:22,112502,G,4.795,G
	12/16/1997 12:23,112502,G,4.795,G
	============================================
	12/16/1997 12:19,15,G
	12/16/1997 12:20,15,G 
	12/16/1997 12:21,15,G 
	12/16/1997 12:22,15,G 
	12/16/1997 12:23,15,G 


