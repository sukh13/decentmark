import json
#creating dictionary to put data to fixture.json
data = []
#creating test user sample
user = {
        "model": "auth.user",
        "pk": '2',
        "fields": {
          "password": "pbkdf2_sha256$120000$tExqQ88KMfI0$zeorpkgj/SM85HXNvdrFvZOuTgzCRuHA4437L7BEDac=",
          "last_login": "2018-08-30T18:42:44.813Z",
          "is_superuser": True,
          "username": "happy",
          "first_name": "",
          "last_name": "",
          "email": "test@rgbops.com",
          "is_staff": True,
          "is_active": True,
          "date_joined": "2018-08-30T18:42:15.998Z",
          "groups": [],
          "user_permissions": []
        }
      }


#creating test unit sample
unit =   {
      "model":"decentmark.unit",
      "pk":1,
      "fields":{
         "name":"Happy",
         "start":"2018-08-06T16:00:00Z",
         "end":"2018-08-14T16:00:00Z",
         "description":"test unit",
         "deleted":False
      }
   }

#creating test assignmet sample
assignment =   {
      "model":"decentmark.assignment",
      "pk":1,
      "fields":{
         "unit":1,
         "name":"assignment 1",
         "start":"2018-07-31T16:00:00Z",
         "end":"2018-08-07T16:00:00Z",
         "description":"test assignment",
         "attempts":3,
         "total":3,
         "test":"test",
         "solution":"solution",
         "template":"template",
         "deleted":False
      }
   }
   
#creating test submission sample
submission =  {
      "model":"decentmark.submission",
      "pk":1,
      "fields":{
         "assignment":1,
         "user":1,
         "date":"2018-08-30T20:49:37.585Z",
         "solution":"solution 1",
         "marked":False,
         "mark":-1,
         "feedback":""
      }
   }
#loop to create multiple data
for x in range(1,4):
    #for user
    user['pk'] = x
    user['fields']['username'] = "test" + str(x)
    user_temp = user.copy() 
    user_temp['fields'] = user['fields'].copy()
    #for Unit
    unit['pk'] = x
    unit['fields']['name'] = "unit " + str(x)
    unit_temp = unit.copy() 
    unit_temp['fields'] = unit['fields'].copy()
    for y in range(1,4):
        #for Assignments
        assignment['pk'] = int(str(x)+str(y))
        assignment['fields']['name'] = "assignment " + str(y)
        assignment_temp = assignment.copy() 
        assignment_temp['fields'] = assignment['fields'].copy()
        data.append(assignment_temp)#adding assignment datato list
        for z in range(1,4):
            #for SUbmissions
            submission['pk'] = int(str(x)+str(y)+str(z))
            submission['fields']['assignment'] = int(str(x)+str(y))
            submission['fields']['user'] = x
            submission_temp = submission.copy() 
            submission_temp['fields'] = submission['fields'].copy()
            data.append(submission_temp)#adding submission datato list


    data.append(user_temp)#adding user datato list
    data.append(unit_temp)#adding unit datato list
#writing to file in json format
data = json.dumps(data)
file = open("fixture.json","w")
file.write("%s\n" % data)
file.close()
