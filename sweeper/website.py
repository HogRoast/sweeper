HTML_HEAD = '''\
<!DOCTYPE html> 
<html> 
<head> 
    <title>Sweeper</title> 
    <meta name="viewport" content="width=device-width, initial-scale=1"> 
    <link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.0-beta.1/jquery.mobile-1.3.0-beta.1.min.css" />
    <script src="http://code.jquery.com/jquery-1.8.3.min.js"></script>
    <script src="http://code.jquery.com/mobile/1.3.0-beta.1/jquery.mobile-1.3.0-beta.1.min.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <link rel="stylesheet" type="text/css" href="css/sweeper.css">
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
            <div data-role="collapsible" data-mini="true" data-theme="a">
                <h3>{groupName}</h3>
                <div data-role="collapsible" data-mini="true" data-theme="a">
                    <h3>Fixtures and Predictions</h3>
                    <div class="table">
                        <table data-role="table" data-mode="columntoggle" class="table-stripe ui-responsive table-stroke">
                            {fixturesTable}
                        </table>
                    </div><!-- /table -->
                </div><!-- /collapsible -->
                <div data-role="collapsible" data-mini="true" data-theme="a">
                    <h3>Form Table</h3>
                    <div class="table">
                        <table data-role="table" data-mode="columntoggle" class="table-stripe ui-responsive table-stroke">
                            {formTable}
                        </table>
                    </div><!-- /table -->
                </div><!-- /collapsible -->
                <div data-role="collapsible" data-mini="true" data-theme="a">
                    <h3>League Table</h3>
                    <div class="table">
                        <table data-role="table" data-mode="columntoggle" class="table-stripe ui-responsive table-stroke">
                            {leagueTable}
                        </table>
                    </div><!-- /table -->
                </div><!-- /collapsible -->
            </div><!-- /collapsible -->
'''
