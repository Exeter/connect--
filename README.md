#Connect--
Less is more. A simplified Exeter Connect.
* * *

###For now...
__test_old.py__ gets user data by headlessly mimicking Exeter Connect functionality.

__test.py__ gets user data by circumventing Exeter Connect completely and talking directly to Connect's [backend](https://connect.exeter.edu/student/_vti_bin/UserProfileService.asmx) via [SOAP](http://en.wikipedia.org/wiki/SOAP). Requires python2 and [suds](https://fedorahosted.org/suds/).

test.py is faster and cleaner than test_old.py in every regard, which shows how much faster directly connecting to Connect's backends is.

###Todo
 - document UserProfileSchema as json, not sudsobject
 - port to [javascript(?)](http://javascriptsoapclient.codeplex.com/) for web client? or should interfacing with connect be part of backend (like csserver/schedule deals with lionlinks?)
 - make website frontend
 - Figure out how to get course materials/classlinks
 	- in html of request for a course's PATH/SitePages/CourseMaterials.aspx, look for second instance of iframe for meat of course materials
