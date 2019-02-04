HTML_HEAD = '''\
<!DOCTYPE html> 
<html> 
<head> 
    <title>Sweeper</title> 
    <meta name="viewport" content="width=device-width, initial-scale=1"> 
    <link rel="stylesheet" href="css/themes/sweeper.min.css" />
    <link rel="stylesheet" href="css/themes/jquery.mobile.icons.min.css" />
    <link rel="stylesheet" href="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css" />
    <link rel="stylesheet" type="text/css" href="css/sweeper.css">
    <script src="http://code.jquery.com/jquery-1.11.1.min.js"></script>
    <script src="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></script>
</head> 
'''

HTML_BODY='''\
<body> 
    <div data-role="page" class="sweeper">
        <div class="ui-bar-b">
            <div class="ui-grid-d">
                <div class="ui-block-a"><a href="index.html"><div class="ui-bar-b"><img src="images/ball and name no background.png" class="logo"></div></a></div>
                <div class="ui-block-b"><div class="ui-bar-b navbar-link"><a href="predictions.html" style="text-decoration:none; color:white">Predictions</a></div></div>
                <div class="ui-block-c"><div class="ui-bar-b navbar-link"><a href="subscribe.html" style="text-decoration:none; color:white">Subscribe</a></div></div>
                <div class="ui-block-d"><div class="ui-bar-b navbar-link"><a href="help.html" style="text-decoration:none; color:white">Data Help</a></div></div>
                <div class="ui-block-e"><div class="ui-bar-b navbar-link"><a href="faq.html" style="text-decoration:none; color:white">FAQ</a></div></div>
            </div><!-- /grid -->
        </div><!-- /bar -->
        <div data-role="content">
            {groups}
        </div><!-- /content -->
    </div><!-- /page -->
</body>
</html>
'''

COLLAPSIBLE_GROUP='''\
            <div data-role="collapsible" data-mini="true" data-theme="{collapsibleTheme}" data-content-theme="false">
                <h3>{groupName}</h3>
                <div data-role="collapsible" data-mini="true" data-theme="{collapsibleTheme}" data-content-theme="false">
                    <h3>Fixtures and Predictions</h3>
                    <div class="table">
                        <table data-role="table" data-mode="columntoggle" class="table-stripe table-stroke fixture-table-priority" id="fixture-table{groupId}">
                            {fixturesTable}
                        </table>
                    </div><!-- /table -->
                </div><!-- /collapsible -->
                <div data-role="collapsible" data-mini="true" data-theme="b" data-content-theme="false">
                    <h3>Form Table</h3>
                    <div class="table">
                        <table data-role="table" data-mode="columntoggle" class="table-stripe ui-responsive table-stroke" id="form-table{groupId}">
                            {formTable}
                        </table>
                    </div><!-- /table -->
                </div><!-- /collapsible -->
                <div data-role="collapsible" data-mini="true" data-theme="b" data-content-theme="false">
                    <h3>League Table</h3>
                    <div class="table">
                        <table data-role="table" data-mode="columntoggle" class="table-stripe ui-responsive table-stroke" id="league-table{groupId}">
                            {leagueTable}
                        </table>
                    </div><!-- /table -->
                </div><!-- /collapsible -->
            </div><!-- /collapsible -->
'''
