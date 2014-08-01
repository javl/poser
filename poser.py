import json, re, requests, os, subprocess

while (1):
    email = None
    real_name = None
    username = raw_input("\nAs which user would you like to commit: ").lower()

    req_userdata = requests.get('https://api.github.com/users/%s' % username)
    req_events = requests.get('https://api.github.com/users/%s/events' % username)

    result_json = json.loads(req_userdata.text)
    try:
        real_name = result_json['name']
    except: pass      
    
    result_json = json.loads(req_events.text)

    if 'message' in result_json:
        if result_json['message'] == 'Not Found':
            print 'There is no user called %s, or can\'t find the needed user date.' % username
        elif result_json['message'][:23] == 'API rate limit exceeded':
            print "API rate limit exceeded; enter your Github credentials at"
            print "the top of the poser script to extend the limit."
            exit()
        else:
            print "Uncaught message: "
            print result_json['message']
            exit()
    else:
        for event in result_json:
            try:
                for commit in event['payload']['commits']:
                    try:
                        if commit['author']['name'] == username or commit['author']['name'] == real_name:
                            email = commit['author']['email']
                            break;
                    except: 
                        pass
            except:
                pass

        if email == None:
            print 'sorry, can\'t find the email for user %s' % username

        else:

            print 'Pushing as user %s with address %s' % (username, email)

            commit_message = raw_input("Enter your commit message: ")

            proc = subprocess.Popen(['git config user.name'], stdout=subprocess.PIPE, shell=True)
            (prev_name, err) = proc.communicate()
            proc = subprocess.Popen(['git config user.email'], stdout=subprocess.PIPE, shell=True)
            (prev_email, err) = proc.communicate()
            os.system('git config user.name "%s"' % username)
            os.system('git config user.email "%s"' % email)
            os.system('git commit -m "%s"' % commit_message)
            os.system('git push -u origin master')

            os.system('git config user.name "%s"' % prev_name.rstrip())
            os.system('git config user.email "%s"' % prev_email.rstrip())
            exit()
