Feature: Shostner Shortner url shortner
    As a web surfer,
    I want to access an url that was given to me,
    So I can get the information that was sent to me.

    As a website owner,
    I want to create links,
    So I can send to my users 

    # Scenario: Link Creation
    #     Given The user is logged in
    #     And the link creation page is displayed
    #     When the user inputs the link "http://jlugao.com" and the alias "jlugao"
    #     Then a new link will be stored with the alias "jlugao" and the url "http://jlugao.com"

    Scenario: User redirection
        Given That the link with alias "jlugao" and url "http://jlugao.com" is saved on the database
        When I enter the url "/jlugao"
        Then I am redirected to "http://jlugao.com"
