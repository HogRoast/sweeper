HTML_HEAD = '''\
<!DOCTYPE html> 
<html> 
<head> 
	<title>Sweeper</title> 
	<meta name="viewport" content="width=device-width, initial-scale=1"> 
	<link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.0-beta.1/jquery.mobile-1.3.0-beta.1.min.css" />
	<script src="http://code.jquery.com/jquery-1.8.3.min.js"></script>
	<script src="http://code.jquery.com/mobile/1.3.0-beta.1/jquery.mobile-1.3.0-beta.1.min.js"></script>

    <style>
        div.sweeper {
            background-color: black;
            background-image: linear-gradient(rgba(0,0,0,.5), rgba(0,0,0,.5)), url("images/code.jpg")
            }
        div.table {
            background-color: rgba(245,245,245,1)
            }
        table {   
            font: xx-small sans-serif;
            table-layout: auto;
            }
        td.m {
            vertical-align: middle;
            }
        caption {   
            font: bold small sans-serif;
            }
        img.logo {
            height: 10%;
            width: 10%;
            }
    </style>
</head> 
'''

HTML_BODY='''\
<body> 
    <div data-role="page" class="sweeper">
        <div data-role="header">
            <img src="images/ball and name no background.png" class="logo">
        </div><!-- /header -->
        <div data-role="content">
        {groups}
        </div><!-- /content -->
    </div><!-- /page -->
</body>
</html>
'''

COLLAPSIBLE_GROUP='''\
            <div data-role="collapsible" data-mini="true">
                <h3>{groupName}</h3>
                <div data-role="collapsible" data-mini="true">
                    <h3>Fixtures and Predictions</h3>
                    <div class="table">
                        <table data-role="table" data-mode="columntoggle" class="table-stripe ui-responsive table-stroke">
                            {fixturesTable}
                        </table>
                    </div><!-- /table -->
                </div><!-- /collapsible -->
                <div data-role="collapsible" data-mini="true">
                    <h3>Form Table</h3>
                    <div class="table">
                        <table data-role="table" data-mode="columntoggle" class="table-stripe ui-responsive table-stroke">
                            {formTable}
                        </table>
                    </div><!-- /table -->
                </div><!-- /collapsible -->
                <div data-role="collapsible" data-mini="true">
                    <h3>League Table</h3>
                    <div class="table">
                        <table data-role="table" data-mode="columntoggle" class="table-stripe ui-responsive table-stroke">
                            {leagueTable}
                        </table>
                    </div><!-- /table -->
                </div><!-- /collapsible -->
            </div><!-- /collapsible -->
'''
